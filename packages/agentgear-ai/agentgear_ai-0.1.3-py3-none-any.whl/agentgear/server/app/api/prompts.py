from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.deps import require_project, require_scopes
from agentgear.server.app.models import Project, Prompt, PromptVersion

router = APIRouter(prefix="/api/prompts", tags=["prompts"])


@router.post("", response_model=schemas.PromptRead, status_code=status.HTTP_201_CREATED)
def create_prompt(
    payload: schemas.PromptCreate,
    db: Session = Depends(get_db),
    request: Request = None,
    _: None = Depends(require_scopes(["prompts.write"])),
):
    settings = get_settings()
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not settings.local_mode and request and request.state.project and request.state.project.id != project.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    prompt = Prompt(project_id=payload.project_id, name=payload.name, description=payload.description)
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    version = PromptVersion(
        prompt_id=prompt.id, version=1, content=payload.content, metadata_=payload.metadata
    )
    db.add(version)
    db.commit()
    return prompt


@router.get("", response_model=list[schemas.PromptRead])
def list_prompts(
    project_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Prompt)
    if project_id:
        query = query.filter(Prompt.project_id == project_id)
    prompts = query.order_by(Prompt.created_at.desc()).all()
    return prompts


@router.get("/{prompt_id}", response_model=schemas.PromptRead)
def get_prompt(prompt_id: str, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return prompt


@router.post("/{prompt_id}/versions", response_model=schemas.PromptVersionRead)
def create_prompt_version(
    prompt_id: str,
    payload: schemas.PromptVersionCreate,
    db: Session = Depends(get_db),
    request: Request = None,
    _: None = Depends(require_scopes(["prompts.write"])),
):
    settings = get_settings()
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    if not settings.local_mode and request and request.state.project and request.state.project.id != prompt.project_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    latest_version = (
        db.query(func.max(PromptVersion.version)).filter(PromptVersion.prompt_id == prompt_id).scalar()
        or 0
    )
    version = PromptVersion(
        prompt_id=prompt_id,
        version=latest_version + 1,
        content=payload.content,
        metadata_=payload.metadata,
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


@router.get("/{prompt_id}/versions", response_model=list[schemas.PromptVersionRead])
def list_prompt_versions(prompt_id: str, db: Session = Depends(get_db)):
    versions = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt_id)
        .order_by(PromptVersion.version.desc())
        .all()
    )
    return versions
