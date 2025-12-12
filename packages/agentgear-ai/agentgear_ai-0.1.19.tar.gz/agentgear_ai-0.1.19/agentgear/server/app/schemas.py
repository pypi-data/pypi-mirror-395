from datetime import datetime
from typing import Any, List, Optional, Literal

from pydantic import BaseModel, Field

# ... (Previous schemas) ...

class ORMModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


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
        default_factory=lambda: ["runs.write", "prompts.read", "prompts.write", "tokens.manage", "datasets.read", "datasets.write", "evaluations.read", "evaluations.write"]
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
    scope: Optional[str] = "project"
    content: str
    tags: Optional[List[str]] = None
    metadata: Optional[dict[str, Any]] = None


class PromptUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class PromptVersionCreate(BaseModel):
    content: str
    metadata: Optional[dict[str, Any]] = None


class PromptRead(ORMModel):
    id: str
    project_id: str
    name: str
    description: Optional[str] = None
    scope: str
    tags: Optional[List[str]] = None
    created_at: datetime


class PromptVersionRead(ORMModel):
    id: str
    prompt_id: str
    version: int
    content: str
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")
    created_at: datetime


class TokenUsage(BaseModel):
    prompt: Optional[int] = None
    completion: Optional[int] = None
    total: Optional[int] = None


class PromptRunRequest(BaseModel):
    version_id: Optional[str] = None # if None, latest
    inputs: dict[str, str] = {}
    model_config_name: Optional[str] = None # ID or name of LLMModel
    stream: bool = False


class PromptRunResponse(BaseModel):
    output: str
    error: Optional[str] = None
    latency_ms: float
    token_usage: Optional[TokenUsage] = None





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
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")
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
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")


class MetricsSummary(BaseModel):
    runs: int
    spans: int
    prompts: int
    projects: int


class AuthStatus(BaseModel):
    configured: bool
    mode: Literal["none", "env", "db"]
    username: Optional[str] = None
    project_id: Optional[str] = None


class AuthSetup(BaseModel):
    username: str
    password: str


class AuthLogin(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    project_id: str
    username: str
    role: str = "user"


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    project_id: Optional[str] = None
    role: str = "user"


class UserRead(ORMModel):
    id: str
    username: str
    email: Optional[str]
    project_id: Optional[str]
    role: str
    created_at: datetime


class UserPasswordReset(BaseModel):
    password: str


class LLMModelCreate(BaseModel):
    name: str
    provider: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    config: Optional[dict[str, Any]] = None


class LLMModelRead(ORMModel):
    id: str
    name: str
    provider: str
    base_url: Optional[str]
    config: Optional[dict[str, Any]]
    created_at: datetime

# --- NEW SCHEMAS FOR SETTINGS ---

class AlertRuleCreate(BaseModel):
    project_id: str
    metric: str
    threshold: float
    operator: str = ">"
    window_minutes: int = 5
    recipients: List[str]  # List of emails
    enabled: bool = True

class AlertRuleRead(ORMModel):
    id: str
    project_id: str
    metric: str
    threshold: float
    operator: str
    window_minutes: int
    recipients: Optional[List[str]]
    enabled: bool
    created_at: datetime

class SMTPConfig(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    encryption: Optional[str] = None
    sender_email: Optional[str] = None
    enabled: bool = True

class RoleCreate(BaseModel):
    name: str
    permissions: List[str]

class RoleRead(BaseModel):
    id: str
    name: str
    permissions: List[str]


# --- NEW SCHEMAS FOR DATASETS & EVALUATIONS ---

class DatasetCreate(BaseModel):
    project_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict[str, Any]] = None

class DatasetRead(ORMModel):
    id: str
    project_id: str
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")
    created_at: datetime

class DatasetExampleCreate(BaseModel):
    input_text: Optional[str] = None
    expected_output: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

class DatasetExampleRead(ORMModel):
    id: str
    dataset_id: str
    input_text: Optional[str] = None
    expected_output: Optional[str] = None
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")
    created_at: datetime

class EvaluationCreate(BaseModel):
    project_id: str
    trace_id: Optional[str] = None
    run_id: Optional[str] = None
    span_id: Optional[str] = None
    evaluator_type: str = "manual"
    score: Optional[float] = None
    max_score: Optional[float] = None
    passed: Optional[bool] = None
    comments: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

class EvaluationRead(ORMModel):
    id: str
    project_id: str
    trace_id: Optional[str]
    run_id: Optional[str]
    span_id: Optional[str]
    evaluator_type: str
    score: Optional[float]
    max_score: Optional[float]
    passed: Optional[bool]
    comments: Optional[str]
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="metadata_")
    created_at: datetime


class EvaluatorCreate(BaseModel):
    project_id: Optional[str] = None
    name: str
    prompt_template: str
    model: str
    config: Optional[dict[str, Any]] = None

class EvaluatorRead(ORMModel):
    id: str
    project_id: str
    name: str
    prompt_template: str
    model: str
    config: Optional[dict[str, Any]]
    created_at: datetime

