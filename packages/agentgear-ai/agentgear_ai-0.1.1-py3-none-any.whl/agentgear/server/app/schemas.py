from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ORMModel(BaseModel):
    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectRead(ORMModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime


class TokenCreate(BaseModel):
    scopes: List[str] = Field(
        default_factory=lambda: ["runs.write", "prompts.read", "prompts.write", "tokens.manage"]
    )


class TokenRead(ORMModel):
    id: str
    project_id: str
    scopes: List[str]
    created_at: datetime
    revoked: bool
    last_used_at: Optional[datetime] = None


class TokenWithSecret(TokenRead):
    token: str


class PromptCreate(BaseModel):
    project_id: str
    name: str
    description: Optional[str] = None
    content: str
    metadata: Optional[dict[str, Any]] = None


class PromptVersionCreate(BaseModel):
    content: str
    metadata: Optional[dict[str, Any]] = None


class PromptRead(ORMModel):
    id: str
    project_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime


class PromptVersionRead(ORMModel):
    id: str
    prompt_id: str
    version: int
    content: str
    metadata: Optional[dict[str, Any]] = None
    created_at: datetime


class TokenUsage(BaseModel):
    prompt: Optional[int] = None
    completion: Optional[int] = None
    total: Optional[int] = None


class RunCreate(BaseModel):
    project_id: str
    prompt_version_id: Optional[str] = None
    name: Optional[str] = None
    input_text: Optional[str] = None
    output_text: Optional[str] = None
    token_usage: Optional[TokenUsage] = None
    cost: Optional[float] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class RunRead(ORMModel):
    id: str
    project_id: str
    prompt_version_id: Optional[str]
    name: Optional[str]
    input_text: Optional[str]
    output_text: Optional[str]
    token_input: Optional[int]
    token_output: Optional[int]
    cost: Optional[float]
    latency_ms: Optional[float]
    error: Optional[str]
    metadata: Optional[dict[str, Any]]
    created_at: datetime


class SpanCreate(BaseModel):
    project_id: str
    run_id: str
    parent_id: Optional[str] = None
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    latency_ms: Optional[float] = None
    metadata: Optional[dict[str, Any]] = None


class SpanRead(ORMModel):
    id: str
    project_id: str
    run_id: str
    parent_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime]
    latency_ms: Optional[float]
    metadata: Optional[dict[str, Any]]


class MetricsSummary(BaseModel):
    runs: int
    spans: int
    prompts: int
    projects: int
