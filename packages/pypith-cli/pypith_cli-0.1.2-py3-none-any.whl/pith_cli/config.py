from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import yaml

DEFAULT_HOME = Path(".pith")

ProviderType = Literal["anthropic", "openai", "ollama", "none"]

# Default models per provider
DEFAULT_MODELS: dict[str, str] = {
    "anthropic": "claude-sonnet-4-20250514",
    "openai": "gpt-4o",
    "ollama": "llama3",
}

# Default API key env vars per provider
DEFAULT_API_KEY_ENVS: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
}


@dataclass
class Config:
    """Global pith configuration."""

    provider: ProviderType = "none"
    model: str | None = None
    api_key_env: str | None = None
    default_depth: int = 2
    timeout: int = 30
    cache_ttl: int = 86400
    hint_prefix: str = "↳"
    run_prefix: str = "run:"


def get_global_config_path() -> Path:
    """Return path to global config file (~/.pith/config.yaml)."""
    return Path.home() / ".pith" / "config.yaml"


def _load_config_from_path(path: Path) -> Config | None:
    """Load config from a specific path, return None if missing or invalid."""
    if not path.exists():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return Config(
            provider=data.get("provider", "none"),
            model=data.get("model"),
            api_key_env=data.get("api_key_env"),
            default_depth=data.get("default_depth", 2),
            timeout=data.get("timeout", 30),
            cache_ttl=data.get("cache_ttl", 86400),
            hint_prefix=data.get("hint_prefix", "↳"),
            run_prefix=data.get("run_prefix", "run:"),
        )
    except Exception:
        return None


def load_global_config() -> Config:
    """Load global config from ~/.pith/config.yaml, return defaults if missing."""
    return _load_config_from_path(get_global_config_path()) or Config()


def get_local_config_path() -> Path:
    """Return path to local config file (.pith/config.yaml in current directory)."""
    return Path.cwd() / ".pith" / "config.yaml"


def load_local_config() -> Config | None:
    """Load local config from .pith/config.yaml, return None if missing."""
    return _load_config_from_path(get_local_config_path())


def merge_config(base: Config, override: Config | None) -> Config:
    """Merge override config into base. Non-default values in override take precedence."""
    if override is None:
        return base

    defaults = Config()
    return Config(
        provider=override.provider
        if override.provider != defaults.provider
        else base.provider,
        model=override.model if override.model is not None else base.model,
        api_key_env=override.api_key_env
        if override.api_key_env is not None
        else base.api_key_env,
        default_depth=override.default_depth
        if override.default_depth != defaults.default_depth
        else base.default_depth,
        timeout=override.timeout
        if override.timeout != defaults.timeout
        else base.timeout,
        cache_ttl=override.cache_ttl
        if override.cache_ttl != defaults.cache_ttl
        else base.cache_ttl,
        hint_prefix=override.hint_prefix
        if override.hint_prefix != defaults.hint_prefix
        else base.hint_prefix,
        run_prefix=override.run_prefix
        if override.run_prefix != defaults.run_prefix
        else base.run_prefix,
    )


def apply_env_overrides(config: Config) -> Config:
    """Override config with PITH_* environment variables."""
    provider = os.environ.get("PITH_PROVIDER")
    model = os.environ.get("PITH_MODEL")

    if provider is None and model is None:
        return config

    return Config(
        provider=provider
        if provider in ("anthropic", "openai", "ollama", "none")
        else config.provider,  # type: ignore[arg-type]
        model=model if model else config.model,
        api_key_env=config.api_key_env,
        default_depth=config.default_depth,
        timeout=config.timeout,
        cache_ttl=config.cache_ttl,
        hint_prefix=config.hint_prefix,
        run_prefix=config.run_prefix,
    )


def load_config() -> Config:
    """Load config with full precedence chain: defaults → global → local → env vars.

    CLI flags (highest priority) are applied by the caller.

    Precedence (highest to lowest):
    1. CLI flags (--provider, --model, etc.) - applied by caller
    2. Environment variables (PITH_PROVIDER, PITH_MODEL)
    3. Local config (.pith/config.yaml in current directory)
    4. Global config (~/.pith/config.yaml)
    5. Built-in defaults
    """
    # Start with global config (includes defaults for missing values)
    config = load_global_config()

    # Override with local config
    local_config = load_local_config()
    config = merge_config(config, local_config)

    # Override with environment variables
    config = apply_env_overrides(config)

    return config


def save_config(config: Config) -> Path:
    """Save config to ~/.pith/config.yaml, creating directory if needed."""
    path = get_global_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Filter out None values for cleaner YAML
    data = {k: v for k, v in asdict(config).items() if v is not None}
    path.write_text(yaml.safe_dump(data, default_flow_style=False), encoding="utf-8")
    return path


def validate_api_key(config: Config) -> bool:
    """Check if the required API key env var is set. Returns True if valid or not needed."""
    if config.provider in ("none", "ollama"):
        return True
    env_var = config.api_key_env or DEFAULT_API_KEY_ENVS.get(config.provider)
    if env_var is None:
        return True
    return os.environ.get(env_var) is not None


def ensure_home(root: Path = DEFAULT_HOME) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "bin").mkdir(parents=True, exist_ok=True)
    (root / "schemas").mkdir(parents=True, exist_ok=True)
    return root


def schema_path(tool: str, root: Path = DEFAULT_HOME) -> Path:
    return root / "schemas" / f"{tool}.pith.json"


def list_wrapped_tools(root: Path = DEFAULT_HOME) -> list[str]:
    if not (root / "schemas").exists():
        return []
    return sorted(
        path.stem.replace(".pith", "")
        for path in (root / "schemas").glob("*.pith.json")
    )


def load_schema(tool: str, root: Path = DEFAULT_HOME) -> str | None:
    path = schema_path(tool, root)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")
