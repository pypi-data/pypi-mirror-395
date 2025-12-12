from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.deps import require_project, require_scopes
from agentgear.server.app.models import Project, Prompt, PromptVersion

router = APIRouter(prefix="/api/prompts", tags=["prompts"])


@router.post("", response_model=schemas.PromptRead, status_code=status.HTTP_201_CREATED)
def create_prompt(
    payload: schemas.PromptCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["prompts.write"])),
):
    settings = get_settings()
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # RBAC: Only admin can create global prompts
    if payload.scope == "global":
        # Check if user is admin (simple check: if request has user info and role='admin')
        # For now, relying on TokenAuthMiddleware to set state or implicit trust for this version
        pass 

    if not settings.local_mode and request and request.state.project_id and request.state.project_id != project.id:
         # Unless it's a global prompt creation (which might be allowed depending on exact policy, but strictly project-scoped tokens shouldn't create cross-project unless admin)
         if payload.scope != "global":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    prompt = Prompt(
        project_id=payload.project_id, 
        name=payload.name, 
        description=payload.description,
        scope=payload.scope or "project",
        tags=payload.tags
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    version = PromptVersion(
        prompt_id=prompt.id, version=1, content=payload.content, metadata_=payload.metadata
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return prompt


@router.put("/{prompt_id}", response_model=schemas.PromptRead)
def update_prompt(
    prompt_id: str,
    payload: schemas.PromptUpdate,
    db: Session = Depends(get_db),
    request: Request = None,
    _: None = Depends(require_scopes(["prompts.write"])),
):
    settings = get_settings()
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")

    if not settings.local_mode and request and request.state.project_id and request.state.project_id != prompt.project_id:
        # Implicitly allow global prompt modification if admin (future check), but strictly block cross-project
        if prompt.scope != "global":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    if payload.name:
        prompt.name = payload.name
    if payload.description:
        prompt.description = payload.description
    if payload.tags is not None:
        prompt.tags = payload.tags
    
    db.commit()
    db.refresh(prompt)
    return prompt


@router.get("", response_model=list[schemas.PromptRead])
def list_prompts(
    project_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Prompt)
    
    # Filter by project OR global scope
    if project_id:
        # If project_id provided, show prompts for that project + global prompts
        from sqlalchemy import or_
        query = query.filter(or_(Prompt.project_id == project_id, Prompt.scope == "global"))
    
    prompts = query.order_by(Prompt.created_at.desc()).all()
    return prompts


@router.get("/{prompt_id}", response_model=schemas.PromptRead)
def get_prompt(prompt_id: str, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return prompt


@router.post("/{prompt_id}/versions", response_model=schemas.PromptVersionRead)
def create_prompt_version(
    prompt_id: str,
    payload: schemas.PromptVersionCreate,
    db: Session = Depends(get_db),
    request: Request = None,
    _: None = Depends(require_scopes(["prompts.write"])),
):
    settings = get_settings()
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    if not settings.local_mode and request and request.state.project_id and request.state.project_id != prompt.project_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    latest_version = (
        db.query(func.max(PromptVersion.version)).filter(PromptVersion.prompt_id == prompt_id).scalar()
        or 0
    )
    version = PromptVersion(
        prompt_id=prompt_id,
        version=latest_version + 1,
        content=payload.content,
        metadata_=payload.metadata,
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


@router.get("/{prompt_id}/versions", response_model=list[schemas.PromptVersionRead])
def list_prompt_versions(prompt_id: str, db: Session = Depends(get_db)):
    versions = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt_id)
        .order_by(PromptVersion.version.desc())
        .all()
    )
    return versions


@router.post("/{prompt_id}/run", response_model=schemas.PromptRunResponse)
def run_prompt(
    prompt_id: str,
    payload: schemas.PromptRunRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["runs.write"])),
):
    import time
    from agentgear.server.app.utils.llm import call_llm
    from agentgear.server.app.models import LLMModel

    # 1. Get Prompt Version
    if payload.version_id:
        version = db.query(PromptVersion).filter(PromptVersion.id == payload.version_id).first()
    else:
        version = (
            db.query(PromptVersion)
            .filter(PromptVersion.prompt_id == prompt_id)
            .order_by(PromptVersion.version.desc())
            .first()
        )
    
    if not version:
        raise HTTPException(status_code=404, detail="Prompt version not found")

    # 2. Prepare Config
    api_key = None
    provider = "openai"
    model_name = "gpt-3.5-turbo"
    
    if payload.model_config_name:
        # Try finding by ID first
        llm_model = db.query(LLMModel).filter(LLMModel.id == payload.model_config_name).first()
        if not llm_model:
             # Try finding by name
             llm_model = db.query(LLMModel).filter(LLMModel.name == payload.model_config_name).first()
        
        if llm_model:
            api_key = llm_model.api_key
            provider = llm_model.provider
            if llm_model.config and "model" in llm_model.config:
                model_name = llm_model.config["model"]
    
    # Fallback env support if no model selected or key missing (for dev)
    if not api_key:
         # In a real app, we might fallback to env vars or error out. 
         # For this demo, let's assume if no model is picked, we might error or try a default if env is set.
         # For safety, let's raise if we can't find a key.
         settings = get_settings()
         # If user provided a "secret_key" maybe but that's for auth. 
         # We'll just check if we have an LLMModel "default" or similar.
         pass

    if not api_key:
        raise HTTPException(status_code=400, detail="No valid LLM Model configuration found (missing API Key)")

    # 3. Interpolate
    content = version.content
    for k, v in payload.inputs.items():
        content = content.replace(f"{{{k}}}", str(v))
    
    # 4. Call LLM
    try:
        start = time.time()
        output = call_llm(provider, api_key, model_name, [{"role": "user", "content": content}])
        duration = (time.time() - start) * 1000
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return schemas.PromptRunResponse(
        output=output,
        latency_ms=duration,
        token_usage=None # TODO: calculate
    )
