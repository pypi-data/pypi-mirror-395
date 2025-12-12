from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agentgear.server.app.api import metrics, projects, prompts, runs, spans, tokens
from agentgear.server.app.auth import TokenAuthMiddleware
from agentgear.server.app.config import VersionInfo, get_settings
from agentgear.server.app.db import Base, engine


def create_app() -> FastAPI:
    settings = get_settings()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="AgentGear", version=VersionInfo().version)
    app.add_middleware(TokenAuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(projects.router)
    app.include_router(tokens.router)
    app.include_router(prompts.router)
    app.include_router(runs.router)
    app.include_router(spans.router)
    app.include_router(metrics.router)

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": VersionInfo().version}

    return app


app = create_app()
