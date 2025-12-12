from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class PipelineStep:
    """Configuration for a single pipeline step."""

    name: str
    enabled: bool
    type: str


@dataclass
class LoggingConfig:
    """Logging configuration."""

    enabled: bool = True
    level: str = "INFO"
    log_dir: str = "logs"
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5


@dataclass
class TracePersistenceConfig:
    """Trace persistence configuration."""

    enabled: bool = False
    db_path: str = "traces.db"


@dataclass
class PolicyConfigData:
    """Policy configuration data (separate from PolicyConfig in policy_engine)."""

    max_chars: int = 500
    forbidden_patterns: List[str] = field(default_factory=list)


@dataclass
class GatewayConfig:
    """
    Complete gateway configuration.

    Can be loaded from JSON files in the configs/ directory.
    """

    pipeline_steps: List[PipelineStep] = field(default_factory=list)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    trace_persistence: TracePersistenceConfig = field(
        default_factory=TracePersistenceConfig
    )
    policy: Optional[PolicyConfigData] = None
    description: str = ""
    config_path: Optional[Path] = None  # where this config came from

    def is_step_enabled(self, step_type: str) -> bool:
        """Check if a specific step type is enabled in the pipeline."""
        for step in self.pipeline_steps:
            if step.type == step_type and step.enabled:
                return True
        return False


DEFAULT_CONFIG_CANDIDATES: List[Path] = [
    Path("configs/minimal.config.json"),
    Path("pipeline.config.json"),
]


def _resolve_config_path(config_path: Path | str | None) -> Optional[Path]:
    """
    Resolve the configuration path.

    If config_path is given, use it directly.
    If not, try default candidates in order.
    """
    if config_path is not None:
        path = Path(config_path)
        return path if path.exists() else None

    for candidate in DEFAULT_CONFIG_CANDIDATES:
        if candidate.exists():
            return candidate

    return None


def load_config(config_path: Path | str | None = None) -> GatewayConfig:
    """
    Load gateway configuration from a JSON file.

    If no path is given, tries known defaults.
    Falls back to an internal minimal configuration if nothing is found.
    """
    path = _resolve_config_path(config_path)

    if path is None:
        logger.warning(
            "No gateway config file found, using internal defaults "
            "(pipeline: policy_check only)."
        )
        return GatewayConfig(
            pipeline_steps=[
                PipelineStep(name="policy_check", enabled=True, type="policy")
            ],
            config_path=None,
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info("KL Exec Gateway config loaded from %s", path.resolve())
    except Exception as exc:
        logger.error(
            "Failed to load gateway config from %s, using internal defaults: %s",
            path,
            exc,
        )
        return GatewayConfig(
            pipeline_steps=[
                PipelineStep(name="policy_check", enabled=True, type="policy")
            ],
            config_path=None,
        )

    # Parse pipeline steps
    steps: List[PipelineStep] = []
    pipeline_data: Dict[str, Any] = data.get("pipeline", {})
    for step_data in pipeline_data.get("steps", []):
        steps.append(
            PipelineStep(
                name=step_data.get("name", "unknown"),
                enabled=step_data.get("enabled", False),
                type=step_data.get("type", "unknown"),
            )
        )

    # Parse logging config
    logging_data: Dict[str, Any] = data.get("logging", {})
    rotation_data: Dict[str, Any] = logging_data.get("rotation", {})
    logging_config = LoggingConfig(
        enabled=logging_data.get("enabled", True),
        level=logging_data.get("level", "INFO"),
        log_dir=logging_data.get("log_dir", "logs"),
        max_bytes=rotation_data.get("max_bytes", 10485760),
        backup_count=rotation_data.get("backup_count", 5),
    )

    # Parse trace persistence config
    trace_data: Dict[str, Any] = data.get("trace_persistence", {})
    trace_config = TracePersistenceConfig(
        enabled=trace_data.get("enabled", False),
        db_path=trace_data.get("db_path", "traces.db"),
    )

    # Parse policy config (if present)
    policy_config: Optional[PolicyConfigData] = None
    if "policy" in data:
        policy_data: Dict[str, Any] = data["policy"]
        policy_config = PolicyConfigData(
            max_chars=policy_data.get("max_chars", 500),
            forbidden_patterns=policy_data.get("forbidden_patterns", []),
        )

    return GatewayConfig(
        pipeline_steps=steps,
        logging=logging_config,
        trace_persistence=trace_config,
        policy=policy_config,
        description=data.get("description", ""),
        config_path=path,
    )
