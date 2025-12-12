from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Evaluator, Trace, Run, Span, Project
from agentgear.server.app.deps import require_scopes

router = APIRouter(prefix="/api/evaluators", tags=["evaluators"])

class EvaluateRequest(BaseModel):
    trace_id: Optional[str] = None
    run_id: Optional[str] = None # span id if run_id? confusing naming in models. Run=Span container (Trace)?
    # In my model: Run = Trace (renamed in UI?), Span = Step.
    # Actually Trace = container, Run = ? 
    # Let's look at models again. Trace has many Runs? 
    # Trace has Span. Run has Span.
    # Trace seems to be the top level.
    # Let's support trace_id and span_id.

    span_id: Optional[str] = None

@router.post("", response_model=schemas.EvaluatorRead, status_code=status.HTTP_201_CREATED)
def create_evaluator(
    payload: schemas.EvaluatorCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["evaluations.write"])),
):
    settings = get_settings()
    pid = payload.project_id or request.state.project_id
    if not pid:
        raise HTTPException(status_code=400, detail="Project ID required")

    obj = Evaluator(
        project_id=pid,
        name=payload.name,
        prompt_template=payload.prompt_template,
        model=payload.model,
        config=payload.config
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("", response_model=List[schemas.EvaluatorRead])
def list_evaluators(
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["evaluations.read"])),
):
    settings = get_settings()
    pid = request.state.project_id
    query = db.query(Evaluator)
    if not settings.local_mode and pid:
        query = query.filter(Evaluator.project_id == pid)
    return query.all()

@router.post("/{evaluator_id}/run")
async def run_evaluation(
    evaluator_id: str,
    target: EvaluateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["evaluations.write"])),
):
    evaluator = db.query(Evaluator).filter(Evaluator.id == evaluator_id).first()
    if not evaluator:
        raise HTTPException(status_code=404, detail="Evaluator not found")

    # Fetch context
    input_text = ""
    output_text = ""
    
    if target.span_id:
        span = db.query(Span).filter(Span.id == target.span_id).first()
        if not span:
             raise HTTPException(status_code=404, detail="Span not found")
        # Find input/output from span?
        # Span doesn't strictly have input_text/output_text columns in my memory, let's check models.
        # It has request_payload / response_payload.
        # Or I might have added input_text?
        # Checking models.py... Span has request_payload (JSON), response_payload (JSON).
        # We need to extract text.
        input_text = str(span.request_payload)
        output_text = str(span.response_payload)
        
    elif target.trace_id:
        trace = db.query(Trace).filter(Trace.id == target.trace_id).first()
        if not trace:
            raise HTTPException(status_code=404, detail="Trace not found")
        input_text = trace.input_text
        output_text = trace.output_text
    else:
        raise HTTPException(status_code=400, detail="Target trace_id or span_id required")

    # Simple template substitution
    prompt = evaluator.prompt_template.replace("{{input}}", str(input_text)).replace("{{output}}", str(output_text))
    
    # Call LLM
    try:
        from agentgear.server.app.utils.llm import call_llm
        import os
        
        # Simple provider detection
        provider = "openai" 
        # In a real app, looking up LLMModel by name to get provider/key would be better
        # For now, rely on env var
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        messages = [{"role": "user", "content": prompt}]
        
        # call_llm is synchronous currently
        result_text = call_llm(
            provider=provider,
            api_key=api_key,
            model_name=evaluator.model,
            messages=messages,
            config=evaluator.config
        )
        
        # Parse result - expecting JSON? or Score? 
        # For simplicity, let's assume the template asks for a number 0-1 or JSON.
        # We'll try to extract a number.
        score = None
        try:
            import re
            match = re.search(r'\b(0(\.\d+)?|1(\.0+)?)\b', result_text)
            if match:
                score = float(match.group(0))
        except:
            pass

        # Save Evaluation
        from agentgear.server.app.models import Evaluation
        evaluation = Evaluation(
            project_id=evaluator.project_id,
            trace_id=target.trace_id,
            span_id=target.span_id,
            evaluator_type="llm_as_a_judge",
            score=score,
            comments=result_text,
            metadata_={"evaluator_id": evaluator.id, "model": evaluator.model}
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        
        return evaluation
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
