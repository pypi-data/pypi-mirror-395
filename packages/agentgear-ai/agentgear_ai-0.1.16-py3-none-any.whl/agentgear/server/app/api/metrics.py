from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Project, Prompt, Run, Span

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/summary", response_model=schemas.MetricsSummary)
def metrics_summary(db: Session = Depends(get_db)):
    runs = db.query(func.count(Run.id)).scalar() or 0
    spans = db.query(func.count(Span.id)).scalar() or 0
    prompts = db.query(func.count(Prompt.id)).scalar() or 0
    projects = db.query(func.count(Project.id)).scalar() or 0
    return schemas.MetricsSummary(runs=runs, spans=spans, prompts=prompts, projects=projects)
