from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Evaluation, Project, Trace
from agentgear.server.app.deps import require_scopes

router = APIRouter(prefix="/api/scores", tags=["evaluations"])

@router.post("", response_model=schemas.EvaluationRead, status_code=status.HTTP_201_CREATED)
def create_score(
    payload: schemas.EvaluationCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["evaluations.write"])),
):
    settings = get_settings()
     # RBAC check
    if not settings.local_mode and request.state.project_id and request.state.project_id != payload.project_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    # Validate target exists (logic can be expanded)
    if payload.trace_id:
        trace = db.query(Trace).filter(Trace.id == payload.trace_id).first()
        if not trace:
             raise HTTPException(status_code=404, detail="Trace not found")

    evaluation = Evaluation(
        project_id=payload.project_id,
        trace_id=payload.trace_id,
        run_id=payload.run_id,
        span_id=payload.span_id,
        evaluator_type=payload.evaluator_type,
        score=payload.score,
        max_score=payload.max_score,
        passed=payload.passed,
        comments=payload.comments,
        metadata_=payload.metadata
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation

@router.get("", response_model=List[schemas.EvaluationRead])
def list_scores(
    trace_id: str | None = Query(default=None),
    project_id: str | None = Query(default=None),
    request: Request = None,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["evaluations.read"])),
):
    settings = get_settings()
    query = db.query(Evaluation)
    
    # Filter by user's project if strict mode
    if not settings.local_mode and request.state.project_id:
        query = query.filter(Evaluation.project_id == request.state.project_id)
    elif project_id:
        query = query.filter(Evaluation.project_id == project_id)
        
    if trace_id:
        query = query.filter(Evaluation.trace_id == trace_id)
        
    return query.order_by(Evaluation.created_at.desc()).all()
