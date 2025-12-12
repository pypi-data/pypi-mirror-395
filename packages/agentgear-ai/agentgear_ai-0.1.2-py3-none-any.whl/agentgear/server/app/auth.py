import hashlib
import secrets
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from agentgear.server.app.config import get_settings
from agentgear.server.app.db import SessionLocal
from agentgear.server.app.models import APIKey, Project

HEADER_NAME = "X-AgentGear-Key"


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, hash_token(raw)


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()

    async def dispatch(self, request: Request, call_next):
        token_value = request.headers.get(HEADER_NAME)
        request.state.project = None
        request.state.token_scopes = []

        if not token_value:
            if self.settings.local_mode:
                response = await call_next(request)
                return response
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

        token_hash = hash_token(token_value)
        db = SessionLocal()
        try:
            api_key: Optional[APIKey] = db.query(APIKey).filter(APIKey.key_hash == token_hash).first()
            if not api_key or api_key.revoked:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

            project: Optional[Project] = (
                db.query(Project).filter(Project.id == api_key.project_id).first()
                if api_key
                else None
            )
            if not project:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Project not found")

            api_key.last_used_at = datetime.utcnow()
            db.add(api_key)
            db.commit()
            request.state.project = project
            request.state.token_scopes = api_key.scopes or []
        finally:
            db.close()

        response = await call_next(request)
        return response
