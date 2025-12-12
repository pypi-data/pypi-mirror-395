"""
Helpers for loading and persisting agent configuration.
"""

from __future__ import annotations

import os
import sys
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import uuid


try:  # Python 3.11+
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - fallback for 3.10
    import tomli as tomllib  # type: ignore[no-redef]


CONFIG_ENV_VAR = "FLOWHIVE_AGENT_CONFIG"
DEFAULT_CONFIG_HOME = Path.home() / ".config" / "flowhive-agent" / "config.toml"
SYSTEM_CONFIG_PATH = Path("/etc/flowhive-agent/config.toml")


def _get_default_label() -> str:
    """Get default label from computer hostname."""
    try:
        return platform.node()
    except Exception:
        return "unknown"


@dataclass
class AgentConfig:
    """Runtime settings required to connect to the control plane."""

    agent_id: str
    control_base_url: str
    account_username: Optional[str] = None
    account_email: Optional[str] = None
    account_password: Optional[str] = None
    api_key: Optional[str] = None
    log_dir: str = "agent_logs"
    max_parallel: int = 2
    event_buffer: int = 512
    label: Optional[str] = None


def _candidate_paths(explicit: Optional[str]) -> Iterable[Path]:
    if explicit:
        yield Path(explicit).expanduser()
    env_value = os.environ.get(CONFIG_ENV_VAR)
    if env_value:
        yield Path(env_value).expanduser()
    yield DEFAULT_CONFIG_HOME
    yield SYSTEM_CONFIG_PATH


def load_config(path: Optional[str] = None) -> AgentConfig:
    """
    Load configuration from disk, searching common paths unless overridden.
    """

    for candidate in _candidate_paths(path):
        if not candidate or not candidate.is_file():
            continue
        data = tomllib.loads(candidate.read_text(encoding="utf-8"))
        try:
            return AgentConfig(
                account_email=data.get("account_email"),
                account_password=data.get("account_password"),
                account_username=data.get("account_username"),
                api_key=data.get("api_key"),
                agent_id=data["agent_id"],
                control_base_url=data["control_base_url"],
                log_dir=data.get("log_dir", "agent_logs"),
                max_parallel=int(data.get("max_parallel", 2)),
                event_buffer=int(data.get("event_buffer", 512)),
                label=data.get("label") or _get_default_label(),
            )
        except KeyError as exc:
            raise KeyError(f"Missing mandatory config key: {exc} in {candidate}") from exc
    raise FileNotFoundError(
        f"Agent config not found. Provide --config or set {CONFIG_ENV_VAR}."
    )


def dump_config(config: AgentConfig, path: Optional[str] = None) -> Path:
    """
    Persist configuration to disk.
    """

    target = Path(path or os.environ.get(CONFIG_ENV_VAR) or DEFAULT_CONFIG_HOME).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    contents = [
        f'account_username = "{config.account_username}"',
        f'account_email = "{config.account_email}"',
        f'account_password = "{config.account_password}"',
        f'api_key = "{config.api_key}"',
        f'agent_id = "{config.agent_id}"',
        f'control_base_url = "{config.control_base_url}"',
        f'log_dir = "{config.log_dir}"',
        f"max_parallel = {int(config.max_parallel)}",
        f"event_buffer = {int(config.event_buffer)}",
        f'label = "{config.label}"',
        "",
    ]
    target.write_text("\n".join(contents), encoding="utf-8")
    try:
        os.chmod(target, 0o600)
    except PermissionError:  # pragma: no cover - Windows
        pass
    return target


def apply_overrides(config: AgentConfig, *, args: Optional[object] = None) -> AgentConfig:
    """
    Produce a new config with argparse overrides applied (if provided).
    """

    if not args:
        return config
    account_username = getattr(args, "account_username", None) or config.account_username
    account_email = getattr(args, "account_email", None) or config.account_email
    account_password = getattr(args, "account_password", None) or config.account_password
    api_key = getattr(args, "api_key", None) or config.api_key
    agent_id = getattr(args, "agent_id", None) or config.agent_id
    control_base_url = getattr(args, "control_base_url", None) or config.control_base_url
    log_dir = getattr(args, "log_dir", None) or config.log_dir
    max_parallel = getattr(args, "max_parallel", None) or config.max_parallel
    event_buffer = getattr(args, "event_buffer", None) or config.event_buffer
    label = getattr(args, "label", None) or config.label
    return AgentConfig(
        account_username=account_username,
        account_email=account_email,
        account_password=account_password,
        api_key=api_key,
        agent_id=agent_id,
        control_base_url=control_base_url,
        log_dir=log_dir,
        max_parallel=int(max_parallel),
        event_buffer=int(event_buffer),
        label=label,
    )


# Mapping from user-friendly keys to config fields
KEY_MAPPING = {
    "user.username": "account_username",
    "user.email": "account_email",
    "user.password": "account_password",
    "api_key": "api_key",
    "agent_id": "agent_id",
    "control_base_url": "control_base_url",
    "log_dir": "log_dir",
    "max_parallel": "max_parallel",
    "event_buffer": "event_buffer",
    "label": "label",
}

FIELD_MAPPING = {
    "account_username": "user.username",
    "account_email": "user.email",
    "account_password": "user.password",
    "api_key": "api_key",
    "control_base_url": "control_base_url",
    "log_dir": "log_dir",
    "max_parallel": "max_parallel",
    "event_buffer": "event_buffer",
    "label": "label",
}


def get_config_value(key: str, path: Optional[str] = None) -> Optional[str]:
    """
    Get a configuration value by key (supports both user-friendly keys and direct keys).
    """
    try:
        config = load_config(path)
    except FileNotFoundError:
        return None
    
    field_name = KEY_MAPPING.get(key, key)
    if hasattr(config, field_name):
        value = getattr(config, field_name)
        return str(value) if value is not None else None
    return None


def set_config_value(key: str, value: str, global_: bool = False, path: Optional[str] = None) -> Path:
    """
    Set a configuration value by key (supports both user-friendly keys and direct keys).
    """
    field_name = KEY_MAPPING.get(key, key)
    
    # Load existing config or create new one
    try:
        config = load_config(path)
    except FileNotFoundError:
        # Create a minimal config with defaults
        config = AgentConfig(
            account_username=None,
            account_email=None,
            account_password=None,
            api_key=None,
            agent_id=str(uuid.uuid4()),
            control_base_url="https://flowhive.wangzixi.top",
            label=_get_default_label(),
        )
    
    # Update the field
    if hasattr(config, field_name):
        # Handle type conversion for numeric fields
        if field_name in ("max_parallel", "event_buffer"):
            setattr(config, field_name, int(value))
        else:
            setattr(config, field_name, value)
    else:
        raise ValueError(f"Unknown configuration key: {key}")
    
    # Determine target path
    if global_ or path is None:
        target_path = None  # Will use default
    else:
        target_path = path
    
    return dump_config(config, target_path)


def list_config(path: Optional[str] = None) -> tuple[dict[str, str], Optional[Path]]:
    """
    List all configuration values.
    Returns a tuple of (config_dict, config_file_path).
    config_dict maps user-friendly keys to values.
    config_file_path is the Path to the loaded config file, or None if not found.
    """
    loaded_path = None
    try:
        # Find which config file was actually loaded
        for candidate in _candidate_paths(path):
            if candidate and candidate.is_file():
                loaded_path = candidate
                break
        config = load_config(path)
    except FileNotFoundError:
        return {}, None
    
    result = {}
    
    for field_name in ["account_username", "account_email", "account_password", "api_key", "agent_id", "control_base_url", "log_dir", "max_parallel", "event_buffer", "label"]:
        value = getattr(config, field_name, None)
        if value is not None:
            key = FIELD_MAPPING.get(field_name, field_name)
            # Mask sensitive values
            if field_name == "api_key":
                # result[key] = "***" if value else ""
                result[key] = str(value)
            else:
                result[key] = str(value)
    
    return result, loaded_path


