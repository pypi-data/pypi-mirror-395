from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.auth import hash_password
from agentgear.server.app.db import get_db
from agentgear.server.app.models import User
import secrets

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=List[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: schemas.UserCreate, 
    request: Request,
    db: Session = Depends(get_db)
):
    # RBAC: Only admin can create users
    if not hasattr(request.state, "role") or request.state.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    # Check if user exists
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    salt = secrets.token_hex(8)
    password_hash = hash_password(payload.password, salt)
    
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=password_hash,
        salt=salt,
        role=payload.role,
        project_id=payload.project_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Try to send invite email
    try:
        if user.email:
            from agentgear.server.app.models import SMTPSettings
            from agentgear.server.app.utils.email import send_email
            
            # Fetch SMTP settings for this project (or globally if null project_id?)
            # User might be created for specific project.
            # If project_id is None (admin), we might look for a 'default' project or just skip?
            # Or look for *any* SMTP config?
            # Let's try to lookup by project_id first.
            smtp = None
            if payload.project_id:
                smtp = db.query(SMTPSettings).filter(SMTPSettings.project_id == payload.project_id).first()
            
            # Fallback: Find *any* enabled SMTP config (e.g. from admin project) if not found?
            if not smtp:
                smtp = db.query(SMTPSettings).filter(SMTPSettings.enabled == True).first()
            
            if smtp and smtp.enabled:
                subject = "Welcome to AgentGear"
                html = f"""
                <p>Hello {user.username},</p>
                <p>You have been invited to AgentGear.</p>
                <p><strong>Username:</strong> {user.username}</p>
                <p><strong>Password:</strong> {payload.password}</p>
                <p><a href="{request.base_url}">Login here</a></p>
                """
                send_email(smtp, [user.email], subject, html)
    except Exception as e:
        # Log but don't fail the request
        import logging
        logging.error(f"Failed to send invite email: {e}")

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, request: Request, db: Session = Depends(get_db)):
    # RBAC: Only admin
    if not hasattr(request.state, "role") or request.state.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()


@router.put("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user_id: str, payload: schemas.UserPasswordReset, request: Request, db: Session = Depends(get_db)):
    # RBAC: Only admin (implied by requirement "allow admin to... change password")
    if not hasattr(request.state, "role") or request.state.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    salt = secrets.token_hex(8)
    password_hash = hash_password(payload.password, salt)
    user.password_hash = password_hash
    user.salt = salt
    
    db.add(user)
    db.commit()
