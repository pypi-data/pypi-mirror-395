from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Project, Prompt, PromptVersion, Run
from agentgear.server.app.deps import require_scopes

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("", response_model=schemas.RunRead, status_code=status.HTTP_201_CREATED)
def create_run(
    payload: schemas.RunCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["runs.write"])),
):
    settings = get_settings()
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not settings.local_mode and request.state.project and request.state.project.id != project.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    prompt_version = None
    if payload.prompt_version_id:
        prompt_version = db.query(PromptVersion).filter(PromptVersion.id == payload.prompt_version_id).first()
        if not prompt_version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt version not found")
        prompt = db.query(Prompt).filter(Prompt.id == prompt_version.prompt_id).first()
        if prompt and prompt.project_id != project.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prompt version mismatch")

    token_input = payload.token_usage.prompt if payload.token_usage else None
    token_output = payload.token_usage.completion if payload.token_usage else None

    run = Run(
        project_id=project.id,
        prompt_version_id=payload.prompt_version_id if prompt_version else None,
        name=payload.name,
        input_text=payload.input_text,
        output_text=payload.output_text,
        token_input=token_input,
        token_output=token_output,
        cost=payload.cost,
        latency_ms=payload.latency_ms,
        error=payload.error,
        metadata=payload.metadata,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@router.get("", response_model=list[schemas.RunRead])
def list_runs(
    project_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Run)
    if project_id:
        query = query.filter(Run.project_id == project_id)
    runs = query.order_by(Run.created_at.desc()).all()
    return runs


@router.get("/{run_id}", response_model=schemas.RunRead)
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return run
