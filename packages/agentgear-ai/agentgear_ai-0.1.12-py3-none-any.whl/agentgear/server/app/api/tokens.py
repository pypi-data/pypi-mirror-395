from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.auth import generate_token, hash_token
from agentgear.server.app.db import get_db
from agentgear.server.app.deps import require_project, require_scopes
from agentgear.server.app.models import APIKey, Project

router = APIRouter(prefix="/api/projects/{project_id}/tokens", tags=["tokens"])


@router.post("", response_model=schemas.TokenWithSecret, status_code=status.HTTP_201_CREATED)
def create_token(
    project_id: str,
    project: Project = Depends(require_project),
    payload: schemas.TokenCreate = None,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["tokens.manage"])),
):
    scopes = payload.scopes if payload else ["runs.write", "prompts.read", "prompts.write", "tokens.manage"]
    raw_token, hashed = generate_token()
    record = APIKey(project_id=project.id, key_hash=hashed, scopes=scopes)
    db.add(record)
    db.commit()
    db.refresh(record)
    return schemas.TokenWithSecret(
        id=record.id,
        project_id=record.project_id,
        scopes=record.scopes,
        created_at=record.created_at,
        revoked=record.revoked,
        last_used_at=record.last_used_at,
        token=raw_token,
    )


@router.get("", response_model=list[schemas.TokenRead])
def list_tokens(
    project_id: str,
    project: Project = Depends(require_project),
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["tokens.manage"])),
):
    tokens = db.query(APIKey).filter(APIKey.project_id == project.id).all()
    return tokens


@router.delete("/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_token(
    project_id: str,
    token_id: str,
    project: Project = Depends(require_project),
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["tokens.manage"])),
):
    token = (
        db.query(APIKey)
        .filter(APIKey.id == token_id, APIKey.project_id == project.id, APIKey.revoked.is_(False))
        .first()
    )
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    token.revoked = True
    db.add(token)
    db.commit()
    return None
