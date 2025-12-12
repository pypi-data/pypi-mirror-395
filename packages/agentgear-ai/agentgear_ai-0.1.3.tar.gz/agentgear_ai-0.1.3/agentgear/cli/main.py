import subprocess
from typing import List, Optional

import typer

from agentgear.server.app.auth import generate_token
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import Base, SessionLocal, engine
from agentgear.server.app.models import APIKey, Project, Prompt, PromptVersion, Run

app = typer.Typer(help="AgentGear CLI")


@app.command()
def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    typer.echo("Database initialized.")


@app.command()
def create_project(name: str = typer.Option(...), description: Optional[str] = typer.Option(None)):
    """Create a new project."""
    db = SessionLocal()
    try:
        project = Project(name=name, description=description)
        db.add(project)
        db.commit()
        db.refresh(project)
        typer.echo(f"Created project {project.id} ({project.name})")
    finally:
        db.close()


@app.command()
def list_projects():
    """List projects."""
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        for p in projects:
            typer.echo(f"{p.id}\t{p.name}\t{p.created_at}")
    finally:
        db.close()


@app.command()
def create_token(
    project_id: str,
    scopes: List[str] = typer.Option(["runs.write", "prompts.read", "prompts.write", "tokens.manage"]),
):
    """Create an API token for a project."""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            typer.echo("Project not found")
            raise typer.Exit(code=1)
        raw, hashed = generate_token()
        record = APIKey(project_id=project.id, key_hash=hashed, scopes=scopes)
        db.add(record)
        db.commit()
        db.refresh(record)
        typer.echo(f"Token created for project {project.name}")
        typer.echo("Save this token now; it will not be shown again:")
        typer.echo(raw)
    finally:
        db.close()


@app.command()
def demo_data():
    """Seed demo data."""
    db = SessionLocal()
    try:
        project = Project(name="Demo Project", description="Sample project")
        db.add(project)
        db.commit()
        db.refresh(project)

        prompt = Prompt(project_id=project.id, name="greeting", description="Greeting prompt")
        db.add(prompt)
        db.commit()
        db.refresh(prompt)

        pv = PromptVersion(prompt_id=prompt.id, version=1, content="Hello {{name}}")
        db.add(pv)
        db.commit()

        run = Run(
            project_id=project.id,
            prompt_version_id=pv.id,
            name="demo-run",
            input_text="name=Agent",
            output_text="Hello Agent",
            token_input=5,
            token_output=5,
            cost=0.0001,
            latency_ms=120,
        )
        db.add(run)
        db.commit()
        typer.echo("Demo data created.")
        typer.echo(f"Project ID: {project.id}")
    finally:
        db.close()


@app.command()
def ui(host: Optional[str] = None, port: Optional[int] = None, reload: bool = True):
    """Run FastAPI server with uvicorn."""
    settings = get_settings()
    host = host or settings.api_host
    port = port or settings.api_port
    args = ["uvicorn", "agentgear.server.app.main:app", "--host", host, "--port", str(port)]
    if reload:
        args.append("--reload")
    typer.echo(f"Starting AgentGear API on {host}:{port}")
    subprocess.run(args, check=False)


if __name__ == "__main__":
    app()
