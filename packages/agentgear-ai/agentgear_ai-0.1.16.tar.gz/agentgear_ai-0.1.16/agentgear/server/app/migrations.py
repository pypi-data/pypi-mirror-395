"""
Lightweight, in-process schema migrations for SQLite.

This keeps existing local SQLite databases compatible with newer models
without requiring Alembic at runtime. Only additive, backward-compatible
changes are performed here.
"""

from __future__ import annotations

import logging
from typing import Dict, Set

from sqlalchemy import Engine, text

logger = logging.getLogger(__name__)


def _add_column_if_missing(conn, table: str, column: str, ddl: str, cache: Dict[str, Set[str]]):
    cols = cache.get(table)
    if cols is None:
        rows = conn.execute(text(f'PRAGMA table_info("{table}")')).fetchall()
        cols = {row[1] for row in rows}  # row[1] = column name
        cache[table] = cols
    if column in cols:
        return
    logger.info("Adding missing column %s.%s", table, column)
    conn.execute(text(f'ALTER TABLE "{table}" ADD COLUMN \"{column}\" {ddl}'))
    cols.add(column)


def _create_index_if_missing(conn, name: str, table: str, column: str):
    conn.execute(text(f'CREATE INDEX IF NOT EXISTS "{name}" ON "{table}" ("{column}")'))


def apply_migrations(engine: Engine) -> None:
    """Apply minimal forward-only migrations for SQLite databases."""
    if not engine.url.drivername.startswith("sqlite"):
        return

    with engine.begin() as conn:
        cache: Dict[str, Set[str]] = {}

        # Runs: backfill trace + telemetry fields added after initial releases.
        _add_column_if_missing(conn, "runs", "trace_id", "VARCHAR", cache)
        _add_column_if_missing(conn, "runs", "status", "VARCHAR", cache)
        _add_column_if_missing(conn, "runs", "model", "VARCHAR", cache)
        _add_column_if_missing(conn, "runs", "request_payload", "JSON", cache)
        _add_column_if_missing(conn, "runs", "response_payload", "JSON", cache)
        _add_column_if_missing(conn, "runs", "error_stack", "TEXT", cache)
        _add_column_if_missing(conn, "runs", "tags", "JSON", cache)
        _create_index_if_missing(conn, "ix_runs_trace_id", "runs", "trace_id")

        # Spans: backfill trace linkage + telemetry fields.
        _add_column_if_missing(conn, "spans", "trace_id", "VARCHAR", cache)
        _add_column_if_missing(conn, "spans", "status", "VARCHAR", cache)
        _add_column_if_missing(conn, "spans", "model", "VARCHAR", cache)
        _add_column_if_missing(conn, "spans", "request_payload", "JSON", cache)
        _add_column_if_missing(conn, "spans", "response_payload", "JSON", cache)
        _add_column_if_missing(conn, "spans", "token_input", "INTEGER", cache)
        _add_column_if_missing(conn, "spans", "token_output", "INTEGER", cache)
        _add_column_if_missing(conn, "spans", "cost", "FLOAT", cache)
        _add_column_if_missing(conn, "spans", "error", "TEXT", cache)
        _add_column_if_missing(conn, "spans", "error_stack", "TEXT", cache)
        _add_column_if_missing(conn, "spans", "tags", "JSON", cache)
        _add_column_if_missing(conn, "spans", "tags", "JSON", cache)
        _create_index_if_missing(conn, "ix_spans_trace_id", "spans", "trace_id")

        # Prompts: add scope and tags
        _add_column_if_missing(conn, "prompts", "scope", "VARCHAR", cache)
        _add_column_if_missing(conn, "prompts", "tags", "JSON", cache)

        # APIKeys: add role
        _add_column_if_missing(conn, "api_keys", "role", "VARCHAR", cache)

        # Evaluators
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS evaluators (
                id VARCHAR PRIMARY KEY,
                project_id VARCHAR NOT NULL,
                name VARCHAR NOT NULL,
                prompt_template TEXT NOT NULL,
                model VARCHAR NOT NULL,
                config JSON,
                created_at DATETIME DEFAULT (datetime('now', 'localtime')) NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        """))
