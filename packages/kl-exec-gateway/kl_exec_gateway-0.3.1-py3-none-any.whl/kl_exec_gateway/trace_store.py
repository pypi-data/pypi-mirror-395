# src/kl_exec_gateway/trace_store.py

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .models import GatewayTrace
from .pipeline_types import StepTrace


class TraceStore:
    """
    SQLite-based persistent storage for GatewayTrace objects.

    Provides:
    - Full trace persistence for audit and compliance
    - Query by trace_id, policy decision, date range
    - Opt-in: only enabled if explicitly configured
    """

    def __init__(self, db_path: Path | str = Path("traces.db")) -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Create database schema if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            # Main traces table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS traces (
                    trace_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    raw_model_response TEXT NOT NULL,
                    effective_chat_response TEXT NOT NULL,
                    policy_allowed INTEGER NOT NULL,
                    policy_code TEXT,
                    policy_reason TEXT,
                    policy_rule_id TEXT,
                    kernel_trace_json TEXT,
                    transform_details TEXT
                )
                """
            )
            
            # New: Step-by-step traces table (Phase 2)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trace_steps (
                    trace_id TEXT NOT NULL,
                    sequence_index INTEGER NOT NULL,
                    step_id TEXT NOT NULL,
                    step_type TEXT NOT NULL,
                    input_json TEXT NOT NULL,
                    output_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (trace_id, sequence_index),
                    FOREIGN KEY (trace_id) REFERENCES traces(trace_id)
                )
                """
            )

            # Index for common queries
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON traces(created_at)
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_policy_allowed 
                ON traces(policy_allowed)
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_policy_code 
                ON traces(policy_code)
                """
            )

            conn.commit()

    def save_trace(
        self, trace: GatewayTrace, transform_details: Optional[str] = None
    ) -> None:
        """
        Persist a GatewayTrace to the database.

        Args:
            trace: The GatewayTrace object to save
            transform_details: Optional JSON string with transformation details
        """
        with sqlite3.connect(self.db_path) as conn:
            # Serialize kernel trace if present
            kernel_trace_json = None
            if trace.kernel_policy_trace:
                try:
                    kernel_trace_json = json.dumps(asdict(trace.kernel_policy_trace))
                except Exception:
                    # If serialization fails, store None
                    pass

            conn.execute(
                """
                INSERT OR REPLACE INTO traces (
                    trace_id, created_at, user_message, raw_model_response,
                    effective_chat_response, policy_allowed, policy_code,
                    policy_reason, policy_rule_id, kernel_trace_json,
                    transform_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trace.trace_id,
                    trace.created_at.isoformat(),
                    trace.user_message.content,
                    trace.raw_model_response,
                    trace.effective_chat_response,
                    1 if trace.policy_decision.allowed else 0,
                    trace.policy_decision.code,
                    trace.policy_decision.reason,
                    trace.policy_decision.rule_id,
                    kernel_trace_json,
                    transform_details,
                ),
            )
            conn.commit()
    
    def save_step_trace(
        self,
        trace_id: str,
        sequence_index: int,
        step_trace: StepTrace,
    ) -> None:
        """
        Save a single step trace entry (Phase 2).
        
        Args:
            trace_id: ID of the parent trace
            sequence_index: Order of this step in the pipeline
            step_trace: StepTrace object to save
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO trace_steps (
                    trace_id, sequence_index, step_id, step_type,
                    input_json, output_json, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trace_id,
                    sequence_index,
                    step_trace.step_id,
                    step_trace.step_type,
                    json.dumps(step_trace.input_snapshot),
                    json.dumps(step_trace.output_snapshot),
                    json.dumps(step_trace.metadata),
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()
    
    def get_step_traces(self, trace_id: str) -> List[dict]:
        """
        Retrieve all step traces for a given trace ID (Phase 2).
        
        Returns list of step trace dicts ordered by sequence_index.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM trace_steps 
                WHERE trace_id = ? 
                ORDER BY sequence_index
                """,
                (trace_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_trace(self, trace_id: str) -> Optional[dict]:
        """
        Retrieve a trace by its ID.

        Returns a dict representation or None if not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM traces WHERE trace_id = ?", (trace_id,)
            )
            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

    def query_by_policy_code(
        self, code: str, limit: int = 100
    ) -> List[dict]:
        """
        Find all traces with a specific policy code.

        Useful for finding all DENY_LENGTH or DENY_PATTERN traces.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM traces 
                WHERE policy_code = ? 
                ORDER BY created_at DESC 
                LIMIT ?
                """,
                (code, limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def query_denied_traces(self, limit: int = 100) -> List[dict]:
        """
        Find all traces where policy denied the response.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM traces 
                WHERE policy_allowed = 0 
                ORDER BY created_at DESC 
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def query_by_date_range(
        self, start_date: datetime, end_date: datetime, limit: int = 1000
    ) -> List[dict]:
        """
        Find traces within a date range.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM traces 
                WHERE created_at >= ? AND created_at <= ?
                ORDER BY created_at DESC 
                LIMIT ?
                """,
                (start_date.isoformat(), end_date.isoformat(), limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> dict:
        """
        Get summary statistics about stored traces.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT 
                    COUNT(*) as total_traces,
                    SUM(CASE WHEN policy_allowed = 1 THEN 1 ELSE 0 END) as allowed,
                    SUM(CASE WHEN policy_allowed = 0 THEN 1 ELSE 0 END) as denied,
                    MIN(created_at) as first_trace,
                    MAX(created_at) as last_trace
                FROM traces
                """
            )
            row = cursor.fetchone()

            return {
                "total_traces": row[0] or 0,
                "allowed": row[1] or 0,
                "denied": row[2] or 0,
                "first_trace": row[3],
                "last_trace": row[4],
            }
    
    def get_session_summary(self, session_id: str) -> dict:
        """
        Get session-level Shadow State (SS) from persistent traces.
        
        This aggregates governance data across all requests in a session.
        Implements session-level SS from KL Execution Theory.
        
        Args:
            session_id: Unique session identifier (prefix of correlation_id)
        
        Returns:
            dict: Session summary with counts, timestamps, and governance stats
        
        Note:
            TODO: Add correlation_id column to traces table for proper session tracking.
            For now, this returns empty results for any session_id.
        """
        with sqlite3.connect(self.db_path) as conn:
            # Get request-level stats
            # TODO: Once correlation_id is added to schema, this query will work
            # For now, we use a placeholder that returns 0 for unknown sessions
            try:
                cursor = conn.execute(
                    """
                    SELECT 
                        COUNT(*) as total_requests,
                        SUM(CASE WHEN policy_allowed = 1 THEN 1 ELSE 0 END) as allowed,
                        SUM(CASE WHEN policy_allowed = 0 THEN 1 ELSE 0 END) as denied,
                        MIN(created_at) as session_start,
                        MAX(created_at) as session_end
                    FROM traces
                    WHERE trace_id LIKE ?
                    """,
                    (f"{session_id}%",)
                )
            except sqlite3.OperationalError:
                # correlation_id column doesn't exist yet
                # Return empty summary
                cursor = conn.execute(
                    """
                    SELECT 
                        0 as total_requests,
                        0 as allowed,
                        0 as denied,
                        NULL as session_start,
                        NULL as session_end
                    """
                )
            request_row = cursor.fetchone()
            
            # Get step-level stats
            # TODO: Once correlation_id is added, use it for filtering
            try:
                cursor = conn.execute(
                    """
                    SELECT 
                        step_type,
                        COUNT(*) as count
                    FROM trace_steps ts
                    JOIN traces t ON ts.trace_id = t.trace_id
                    WHERE t.trace_id LIKE ?
                    GROUP BY step_type
                    """,
                    (f"{session_id}%",)
                )
                step_stats = {row[0]: row[1] for row in cursor.fetchall()}
            except sqlite3.OperationalError:
                step_stats = {}
            
            # Calculate session duration
            session_duration_ms = None
            if request_row[3] and request_row[4]:  # session_start and session_end
                try:
                    from datetime import datetime
                    start = datetime.fromisoformat(request_row[3])
                    end = datetime.fromisoformat(request_row[4])
                    session_duration_ms = int((end - start).total_seconds() * 1000)
                except Exception:
                    pass
            
            return {
                "session_id": session_id,
                "total_requests": request_row[0] or 0,
                "policy_allowed": request_row[1] or 0,
                "policy_denied": request_row[2] or 0,
                "session_start": request_row[3],
                "session_end": request_row[4],
                "session_duration_ms": session_duration_ms,
                "step_stats": {
                    "llm_calls": step_stats.get("llm", 0),
                    "policy_checks": step_stats.get("policy", 0),
                    "transforms": step_stats.get("transform", 0),
                    "finalizations": step_stats.get("finalize", 0),
                },
                "governance_metrics": {
                    "denial_rate": round(request_row[2] / request_row[0], 3) if request_row[0] > 0 else 0.0,
                    "avg_llm_calls_per_request": round(step_stats.get("llm", 0) / request_row[0], 2) if request_row[0] > 0 else 0.0,
                }
            }

