from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from agentgear.server.app.api import auth, metrics, projects, prompts, runs, spans, tokens
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
    app.include_router(auth.router)

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": VersionInfo().version}

    # Serve bundled React build (emitted to agentgear/server/static)
    static_dir = Path(__file__).parent.parent / "static"
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/", include_in_schema=False)
    def serve_index():
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Dashboard not built")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_routes(full_path: str):
        if full_path.startswith(("api", "docs", "openapi.json", "redoc")):
            raise HTTPException(status_code=404, detail="Not found")
        candidate = static_dir / full_path
        if candidate.exists() and candidate.is_file():
            return FileResponse(candidate)
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Dashboard not built")

    return app


app = create_app()
