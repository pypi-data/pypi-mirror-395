import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from agentgear.server.app.db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    prompts = relationship("Prompt", back_populates="project", cascade="all, delete-orphan")
    tokens = relationship("APIKey", back_populates="project", cascade="all, delete-orphan")
    runs = relationship("Run", back_populates="project", cascade="all, delete-orphan")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    key_hash = Column(String, nullable=False, unique=True, index=True)
    scopes = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="tokens")


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project", back_populates="prompts")
    versions = relationship("PromptVersion", back_populates="prompt", cascade="all, delete-orphan")


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(String, primary_key=True, default=_uuid)
    prompt_id = Column(String, ForeignKey("prompts.id"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)  # "metadata" attribute name is reserved
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    prompt = relationship("Prompt", back_populates="versions")


class Trace(Base):
    __tablename__ = "traces"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    prompt_version_id = Column(String, ForeignKey("prompt_versions.id"), nullable=True, index=True)
    name = Column(String, nullable=True)
    status = Column(String, nullable=True)
    input_text = Column(Text, nullable=True)
    output_text = Column(Text, nullable=True)
    model = Column(String, nullable=True)
    request_payload = Column(JSON, nullable=True)
    response_payload = Column(JSON, nullable=True)
    token_input = Column(Integer, nullable=True)
    token_output = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    latency_ms = Column(Float, nullable=True)
    error = Column(Text, nullable=True)
    error_stack = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project")
    prompt_version = relationship("PromptVersion")


class Run(Base):
    __tablename__ = "runs"

    id = Column(String, primary_key=True, default=_uuid)
    trace_id = Column(String, ForeignKey("traces.id"), nullable=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    prompt_version_id = Column(String, ForeignKey("prompt_versions.id"), nullable=True, index=True)
    name = Column(String, nullable=True)
    status = Column(String, nullable=True)
    input_text = Column(Text, nullable=True)
    output_text = Column(Text, nullable=True)
    model = Column(String, nullable=True)
    request_payload = Column(JSON, nullable=True)
    response_payload = Column(JSON, nullable=True)
    token_input = Column(Integer, nullable=True)
    token_output = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    latency_ms = Column(Float, nullable=True)
    error = Column(Text, nullable=True)
    error_stack = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)  # "metadata" attribute name is reserved
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    trace = relationship("Trace")
    project = relationship("Project", back_populates="runs")
    prompt_version = relationship("PromptVersion")
    spans = relationship("Span", back_populates="run", cascade="all, delete-orphan")


class Span(Base):
    __tablename__ = "spans"

    id = Column(String, primary_key=True, default=_uuid)
    trace_id = Column(String, ForeignKey("traces.id"), nullable=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    run_id = Column(String, ForeignKey("runs.id"), nullable=False, index=True)
    parent_id = Column(String, ForeignKey("spans.id"), nullable=True, index=True)
    name = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    latency_ms = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    model = Column(String, nullable=True)
    request_payload = Column(JSON, nullable=True)
    response_payload = Column(JSON, nullable=True)
    token_input = Column(Integer, nullable=True)
    token_output = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    error = Column(Text, nullable=True)
    error_stack = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)  # "metadata" attribute name is reserved

    trace = relationship("Trace")
    run = relationship("Run", back_populates="spans")
    parent = relationship("Span", remote_side=[id])


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    role = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    trace_id = Column(String, ForeignKey("traces.id"), nullable=True, index=True)
    run_id = Column(String, ForeignKey("runs.id"), nullable=True, index=True)
    span_id = Column(String, ForeignKey("spans.id"), nullable=True, index=True)
    evaluator_type = Column(String, nullable=False)  # human, rule, model, etc.
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=True)
    comments = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project")
    trace = relationship("Trace")
    run = relationship("Run")
    span = relationship("Span")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project")
    examples = relationship("DatasetExample", back_populates="dataset", cascade="all, delete-orphan")


class DatasetExample(Base):
    __tablename__ = "dataset_examples"

    id = Column(String, primary_key=True, default=_uuid)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False, index=True)
    input_text = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    dataset = relationship("Dataset", back_populates="examples")


class SMTPSettings(Base):
    __tablename__ = "smtp_settings"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True, index=True)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    encryption = Column(String, nullable=True)  # ssl, tls, starttls
    sender_email = Column(String, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project")


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    metric = Column(String, nullable=False)
    threshold = Column(Float, nullable=False)
    operator = Column(String, nullable=False, default=">")
    window_minutes = Column(Integer, nullable=False, default=5)
    recipients = Column(JSON, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project")


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id = Column(String, primary_key=True, default=_uuid)
    rule_id = Column(String, ForeignKey("alert_rules.id"), nullable=False, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    metric = Column(String, nullable=False)
    value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    traces = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    rule = relationship("AlertRule")
    project = relationship("Project")


class MetricAggregate(Base):
    __tablename__ = "metric_aggregates"

    id = Column(String, primary_key=True, default=_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    metric = Column(String, nullable=False)
    granularity = Column(String, nullable=False)  # e.g., minute, hour, day
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    dimensions = Column(JSON, nullable=True)  # e.g., model, prompt_version, span_type
    values = Column(JSON, nullable=True)  # e.g., avg, p95, p99, count, sum
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project")


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(String, primary_key=True, default=_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
