from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from agentgear.server.app.db import get_db
from agentgear.server.app.models import Project, Run, Prompt, PromptVersion, MetricAggregate, AlertRule, User, LLMModel, Trace, Span
from agentgear.server.app.auth import hash_password
import secrets

router = APIRouter(prefix="/api/seed", tags=["seed"])

@router.post("", status_code=201)
def seed_data(db: Session = Depends(get_db)):
    # Check if demo project exists
    existing = db.query(Project).filter(Project.name == "Demo Project").first()
    if existing:
        return {"message": "Demo already exists"}
    
    # 1. Create Project
    project = Project(name="Demo Project", description="A simulated e-commerce chatbot project for demonstration.")
    db.add(project)
    db.commit()
    db.refresh(project)

    # 2. Create Users
    salt = secrets.token_hex(8)
    user = User(
        username="demo_analyst",
        password_hash=hash_password("demo123", salt),
        salt=salt,
        role="user",
        project_id=project.id,
        email="analyst@example.com"
    )
    db.add(user)

    # 3. Create Models
    model = LLMModel(name="gpt-4-demo", provider="openai", config={"temperature": 0.7})
    db.add(model)
    
    # 4. Create Prompts
    prompt = Prompt(project_id=project.id, name="customer_support_agent", description="Main support bot prompt")
    db.add(prompt)
    db.commit()
    
    p_v1 = PromptVersion(prompt_id=prompt.id, version=1, content="You are a helpful assistant.")
    p_v2 = PromptVersion(prompt_id=prompt.id, version=2, content="You are a helpful assistant for Acme Corp. Be polite.")
    db.add(p_v1)
    db.add(p_v2)
    db.commit()

    # 5. Create Alerts
    alert = AlertRule(
        project_id=project.id,
        metric="token_usage",
        threshold=5000,
        recipients=["admin@example.com"],
        enabled=True
    )
    db.add(alert)

    # 6. Create Runs & Traces
    for i in range(5):
        trace = Trace(
            project_id=project.id,
            name=f"Chat Session {i+1}",
            status="success",
            latency_ms=120 + i*10,
            cost=0.002,
            token_input=100,
            token_output=50,
            model="gpt-4-demo",
            prompt_version_id=p_v2.id
        )
        db.add(trace)
        db.commit() # need id

        run = Run(
            project_id=project.id,
            trace_id=trace.id,
            prompt_version_id=p_v2.id,
            name="completion_call",
            status="success",
            input_text="Where is my order?",
            output_text="I can help with that. What is your order ID?",
            token_input=100,
            token_output=50,
            cost=0.002,
            latency_ms=120 + i*10
        )
        db.add(run)
        
        span = Span(
            project_id=project.id,
            run_id=run.id,
            trace_id=trace.id,
            name="llm_call",
            start_time=datetime.utcnow(),
            latency_ms=100,
            status="ok"
        )
        db.add(span)
    
    db.commit()
    return {"message": "Seeded Demo Project with Data"}
