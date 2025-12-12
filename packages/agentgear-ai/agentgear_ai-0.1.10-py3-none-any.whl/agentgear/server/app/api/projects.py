from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.db import get_db
from agentgear.server.app.models import (
    APIKey,
    Dataset,
    Evaluation,
    Prompt,
    PromptVersion,
    Project,
    Run,
    SMTPSettings,
    Span,
    Trace,
    User,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])

SAMPLE_PROMPTS = [
    {
        "name": "retrieval-chat",
        "description": "Answer using retrieved context",
        "content": "You are a helpful assistant. Use the provided context to answer concisely.\\nContext: {context}\\nQuestion: {question}",
    },
    {
        "name": "summarize",
        "description": "Summarize input text",
        "content": "Summarize the following text in three bullet points:\\n{text}",
    },
    {
        "name": "classification",
        "description": "Simple intent classification",
        "content": "Classify the user message into one of [info_request, complaint, chit_chat, other].\\nMessage: {message}",
    },
]


@router.post("", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: schemas.ProjectCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    # RBAC: Only admin can create projects
    if not hasattr(request.state, "role") or request.state.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    existing = db.query(Project).filter(Project.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name exists")
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Clean up dependents first to satisfy FK constraints on SQLite.
    db.query(Evaluation).filter(Evaluation.project_id == project.id).delete(synchronize_session=False)
    db.query(Span).filter(Span.project_id == project.id).delete(synchronize_session=False)
    db.query(Run).filter(Run.project_id == project.id).delete(synchronize_session=False)
    db.query(Trace).filter(Trace.project_id == project.id).delete(synchronize_session=False)
    db.query(SMTPSettings).filter(SMTPSettings.project_id == project.id).delete(synchronize_session=False)
    db.query(APIKey).filter(APIKey.project_id == project.id).delete(synchronize_session=False)
    db.query(User).filter(User.project_id == project.id).delete(synchronize_session=False)

    for dataset in db.query(Dataset).filter(Dataset.project_id == project.id).all():
        db.delete(dataset)  # cascades dataset examples

    for prompt in db.query(Prompt).filter(Prompt.project_id == project.id).all():
        db.delete(prompt)  # cascades prompt versions

    db.delete(project)
    db.commit()


@router.post("/{project_id}/sample-prompts", response_model=list[schemas.PromptVersionRead])
def add_sample_prompts(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    created_versions: list[PromptVersion] = []
    for sample in SAMPLE_PROMPTS:
        prompt = (
            db.query(Prompt)
            .filter(Prompt.project_id == project.id, Prompt.name == sample["name"])
            .first()
        )
        if not prompt:
            prompt = Prompt(
                project_id=project.id, name=sample["name"], description=sample["description"]
            )
            db.add(prompt)
            db.flush()  # ensure prompt.id

        latest_version = (
            db.query(PromptVersion)
            .filter(PromptVersion.prompt_id == prompt.id)
            .order_by(PromptVersion.version.desc())
            .first()
        )
        next_version = (latest_version.version if latest_version else 0) + 1
        version = PromptVersion(
            prompt_id=prompt.id,
            version=next_version,
            content=sample["content"],
            metadata_=sample.get("metadata"),
        )
        db.add(version)
        created_versions.append(version)

    db.commit()
    for v in created_versions:
        db.refresh(v)
    return created_versions
