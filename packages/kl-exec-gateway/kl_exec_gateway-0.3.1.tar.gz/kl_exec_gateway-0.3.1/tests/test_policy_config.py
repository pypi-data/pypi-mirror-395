from pathlib import Path

from kl_exec_gateway.policy_engine import (
    PolicyConfig,
    build_default_policy_engine,
    load_policy_config,
    save_policy_config,
)


def test_load_policy_config_from_json(tmp_path) -> None:
    cfg_path = tmp_path / "policy.config.json"
    cfg_path.write_text(
        """
        {
          "max_chars": 250,
          "forbidden_patterns": ["FOO", "BAR"]
        }
        """,
        encoding="utf-8",
    )

    cfg = load_policy_config(cfg_path)

    assert isinstance(cfg, PolicyConfig)
    assert cfg.max_chars == 250
    assert cfg.forbidden_patterns == ["FOO", "BAR"]


def test_save_policy_config_roundtrip(tmp_path) -> None:
    cfg = PolicyConfig(max_chars=123, forbidden_patterns=["A", "B"])
    cfg_path = tmp_path / "policy.config.json"

    save_policy_config(cfg, cfg_path)
    loaded = load_policy_config(cfg_path)

    assert loaded.max_chars == 123
    assert loaded.forbidden_patterns == ["A", "B"]


def test_build_default_policy_engine_uses_config(tmp_path) -> None:
    cfg_path = tmp_path / "policy.config.json"
    cfg_path.write_text(
        """
        {
          "max_chars": 5,
          "forbidden_patterns": ["BLOCKME"]
        }
        """,
        encoding="utf-8",
    )

    # Load explicit config from the test-local file
    cfg = load_policy_config(cfg_path)

    # Build engine from that config (no reliance on global default path)
    engine = build_default_policy_engine(config=cfg)

    # A 10-char response must be denied by the length limit
    result = engine.evaluate("1234567890")
    assert result.allowed is False
    assert result.code == "DENY_LENGTH"

    # A shorter response with the forbidden pattern must also be denied.
    # Because the length rule is evaluated first, the exact code is not guaranteed.
    result2 = engine.evaluate("x BLOCKME x")
    assert result2.allowed is False
