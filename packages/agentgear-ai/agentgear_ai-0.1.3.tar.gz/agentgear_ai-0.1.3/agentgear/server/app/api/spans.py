from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Project, Run, Span
from agentgear.server.app.deps import require_scopes

router = APIRouter(prefix="/api/spans", tags=["spans"])


@router.post("", response_model=schemas.SpanRead, status_code=status.HTTP_201_CREATED)
def create_span(
    payload: schemas.SpanCreate,
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

    run = db.query(Run).filter(Run.id == payload.run_id, Run.project_id == project.id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    span = Span(
        project_id=project.id,
        run_id=payload.run_id,
        parent_id=payload.parent_id,
        name=payload.name,
        start_time=payload.start_time or run.created_at,
        end_time=payload.end_time,
        latency_ms=payload.latency_ms,
        metadata_=payload.metadata,
    )
    db.add(span)
    db.commit()
    db.refresh(span)
    return span


@router.get("", response_model=list[schemas.SpanRead])
def list_spans(
    run_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Span)
    if run_id:
        query = query.filter(Span.run_id == run_id)
    spans = query.order_by(Span.start_time.desc()).all()
    return spans
