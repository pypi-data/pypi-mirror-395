from typing import Callable, Iterable, Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Project


def require_project(
    request: Request, db: Session = Depends(get_db), project_id: Optional[str] = None
) -> Project:
    settings = get_settings()
    state_project_id = getattr(request.state, "project_id", None)
    if state_project_id:
        project = db.query(Project).filter(Project.id == state_project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Project not found")
        if project_id and project.id != project_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")
        return project

    if settings.local_mode:
        if not project_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project required")
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def require_scopes(required: Iterable[str]) -> Callable:
    required_set = set(required)

    def dependency(request: Request):
        settings = get_settings()
        if settings.local_mode:
            return
        token_scopes = set(getattr(request.state, "token_scopes", []) or [])
        if not required_set.issubset(token_scopes):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope")

    return dependency
