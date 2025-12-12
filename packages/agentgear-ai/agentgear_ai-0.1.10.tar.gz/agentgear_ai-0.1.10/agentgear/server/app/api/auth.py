import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.auth import generate_token, hash_password
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import AdminUser, APIKey, Project

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _ensure_default_project(db: Session) -> Project:
    project = db.query(Project).filter(Project.name == "Default Project").first()
    if project:
        return project
    project = Project(name="Default Project", description="Default project for AgentGear UI")
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def _issue_token(db: Session, project: Project, role: str = "user") -> str:
    raw, hashed = generate_token()
    scopes = ["runs.write", "prompts.read", "prompts.write", "tokens.manage"]
    record = APIKey(project_id=project.id, key_hash=hashed, scopes=scopes, role=role)
    db.add(record)
    db.commit()
    return raw


def _login_success(db: Session, username: str, role: str = "user", project_id: str | None = None) -> schemas.AuthResponse:
    if project_id:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            # Fallback if specific project ID not found (shouldn't happen for valid users, but safety)
            project = _ensure_default_project(db)
    else:
        project = _ensure_default_project(db)
            
    token = _issue_token(db, project, role)
    return schemas.AuthResponse(token=token, project_id=project.id, username=username, role=role)


@router.get("/status", response_model=schemas.AuthStatus)
def auth_status(db: Session = Depends(get_db)):
    settings = get_settings()
    env_mode = bool(settings.admin_username and settings.admin_password)
    stored: Optional[AdminUser] = db.query(AdminUser).first()
    project = db.query(Project).filter(Project.name == "Default Project").first()
    return schemas.AuthStatus(
        configured=env_mode or stored is not None,
        mode="env" if env_mode else ("db" if stored else "none"),
        username=settings.admin_username or (stored.username if stored else None),
        project_id=project.id if project else None,
    )


@router.post("/setup", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def setup_admin(payload: schemas.AuthSetup, db: Session = Depends(get_db)):
    settings = get_settings()
    if settings.admin_username and settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Setup is disabled when admin credentials are provided via environment.",
        )
    existing = db.query(AdminUser).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin already configured")
    salt = secrets.token_hex(8)
    password_hash = hash_password(payload.password, salt)
    admin = AdminUser(username=payload.username, password_hash=password_hash, salt=salt)
    db.add(admin)
    db.commit()
    return _login_success(db, payload.username, role="admin")


@router.post("/login", response_model=schemas.AuthResponse)
def login(payload: schemas.AuthLogin, db: Session = Depends(get_db)):
    settings = get_settings()
    env_mode = settings.admin_username and settings.admin_password
    if env_mode:
        if payload.username != settings.admin_username or payload.password != settings.admin_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return _login_success(db, settings.admin_username, role="admin")

    admin: Optional[AdminUser] = db.query(AdminUser).filter(AdminUser.username == payload.username).first()
    if admin:
        if hash_password(payload.password, admin.salt) == admin.password_hash:
             return _login_success(db, admin.username, role="admin")
    
    # Check standard users
    from agentgear.server.app.models import User
    user: Optional[User] = db.query(User).filter(User.username == payload.username).first()
    if user:
        if hash_password(payload.password, user.salt) == user.password_hash:
            return _login_success(db, user.username, role=user.role, project_id=user.project_id)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
