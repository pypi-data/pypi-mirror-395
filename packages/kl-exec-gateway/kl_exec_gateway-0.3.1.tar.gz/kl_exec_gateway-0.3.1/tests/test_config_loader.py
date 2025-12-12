"""Tests for configuration loading."""

from pathlib import Path

import pytest

from kl_exec_gateway.config_loader import (
    GatewayConfig,
    LoggingConfig,
    PipelineStep,
    TracePersistenceConfig,
    load_config,
)


def test_load_config_default_when_missing() -> None:
    """Test that default config is returned when file is missing."""
    config = load_config(Path("non-existent-file.json"))

    assert isinstance(config, GatewayConfig)
    assert len(config.pipeline_steps) == 1
    assert config.pipeline_steps[0].type == "policy"


def test_load_config_from_file(tmp_path: Path) -> None:
    """Test loading configuration from JSON file."""
    config_file = tmp_path / "test.config.json"
    config_file.write_text(
        """
        {
          "description": "Test config",
          "pipeline": {
            "steps": [
              {"name": "policy", "enabled": true, "type": "policy"},
              {"name": "sanitize", "enabled": true, "type": "sanitize"}
            ]
          },
          "logging": {
            "enabled": true,
            "level": "DEBUG",
            "log_dir": "test_logs",
            "rotation": {
              "max_bytes": 5242880,
              "backup_count": 3
            }
          },
          "trace_persistence": {
            "enabled": true,
            "db_path": "test_traces.db"
          },
          "policy": {
            "max_chars": 1000,
            "forbidden_patterns": ["SECRET", "PASSWORD"]
          }
        }
        """
    )

    config = load_config(config_file)

    assert config.description == "Test config"
    assert len(config.pipeline_steps) == 2
    assert config.pipeline_steps[0].name == "policy"
    assert config.pipeline_steps[1].type == "sanitize"

    assert config.logging.enabled is True
    assert config.logging.level == "DEBUG"
    assert config.logging.log_dir == "test_logs"
    assert config.logging.max_bytes == 5242880
    assert config.logging.backup_count == 3

    assert config.trace_persistence.enabled is True
    assert config.trace_persistence.db_path == "test_traces.db"

    assert config.policy is not None
    assert config.policy.max_chars == 1000
    assert config.policy.forbidden_patterns == ["SECRET", "PASSWORD"]


def test_is_step_enabled() -> None:
    """Test checking if a pipeline step is enabled."""
    config = GatewayConfig(
        pipeline_steps=[
            PipelineStep(name="policy", enabled=True, type="policy"),
            PipelineStep(name="sanitize", enabled=True, type="sanitize"),
            PipelineStep(name="format", enabled=False, type="format"),
        ]
    )

    assert config.is_step_enabled("policy") is True
    assert config.is_step_enabled("sanitize") is True
    assert config.is_step_enabled("format") is False
    assert config.is_step_enabled("nonexistent") is False


def test_load_minimal_config() -> None:
    """Test loading minimal config file."""
    # Use the actual minimal config template
    config = load_config(Path("configs/minimal.config.json"))

    assert isinstance(config, GatewayConfig)
    assert config.is_step_enabled("policy") is True
    assert config.is_step_enabled("sanitize") is False
    assert config.logging.enabled is True
    assert config.trace_persistence.enabled is False


def test_load_production_config() -> None:
    """Test loading production config file."""
    config = load_config(Path("configs/production.config.json"))

    assert isinstance(config, GatewayConfig)
    assert config.is_step_enabled("policy") is True
    assert config.is_step_enabled("sanitize") is True
    assert config.is_step_enabled("format") is True
    assert config.logging.enabled is True
    assert config.trace_persistence.enabled is True


def test_load_compliance_gdpr_config() -> None:
    """Test loading GDPR compliance config file."""
    config = load_config(Path("configs/compliance-gdpr.config.json"))

    assert isinstance(config, GatewayConfig)
    assert config.is_step_enabled("sanitize") is True
    assert config.trace_persistence.enabled is True
    assert config.logging.level == "DEBUG"

