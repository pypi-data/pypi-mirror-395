from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Optional

try:
    import keyring  # type: ignore[import]
    from keyring.errors import KeyringError  # type: ignore[import]
except ImportError:  # pragma: no cover - optional dependency for tests/CI
    keyring = None

    class KeyringError(Exception):
        """Fallback KeyringError when keyring is unavailable."""


SERVICE_NAME = "doclayer-cli"
DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_OUTPUT_FORMAT = "table"


def _default_config_dir() -> Path:
    home = Path.home()
    return home / ".doclayer"


def _default_config_path() -> Path:
    return _default_config_dir() / "config.json"


@dataclass
class Profile:
    name: str
    base_url: str = DEFAULT_BASE_URL
    tenant_id: str | None = None
    default_project: str | None = None
    output_format: str = DEFAULT_OUTPUT_FORMAT
    # Sensitive values are never written to disk, only stored in keyring
    api_key: str | None = field(default=None, repr=False)
    token: str | None = field(default=None, repr=False)


@dataclass
class Config:
    default_profile: str = "default"
    profiles: Dict[str, Profile] = field(default_factory=dict)

    def get_profile(self, name: Optional[str]) -> Optional[Profile]:
        if not name:
            name = self.default_profile
        return self.profiles.get(name)

    def set_profile(self, profile: Profile) -> None:
        self.profiles[profile.name] = profile


def load_config(path: Path | None = None) -> Config:
    """Load configuration from disk and keyring, creating a default config if needed."""
    config_path = path or _default_config_path()

    if not config_path.exists():
        cfg = Config()
        cfg.profiles["default"] = Profile(name="default")
        return cfg

    try:
        raw = json.loads(config_path.read_text())
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse config file {config_path}: {exc}") from exc

    cfg = Config(
        default_profile=raw.get("default_profile") or "default",
        profiles={},
    )

    for name, pdata in (raw.get("profiles") or {}).items():
        profile = Profile(
            name=name,
            base_url=pdata.get("base_url") or DEFAULT_BASE_URL,
            tenant_id=pdata.get("tenant_id"),
            default_project=pdata.get("default_project"),
            output_format=pdata.get("output_format") or DEFAULT_OUTPUT_FORMAT,
        )

        # Load secrets from keyring if available
        if keyring:
            try:
                api_key = keyring.get_password(SERVICE_NAME, f"{name}-apikey")
                token = keyring.get_password(SERVICE_NAME, f"{name}-token")
            except KeyringError:
                api_key = None
                token = None
        else:
            api_key = None
            token = None

        if api_key:
            profile.api_key = api_key
        if token:
            profile.token = token

        cfg.profiles[name] = profile

    if cfg.default_profile not in cfg.profiles and cfg.profiles:
        # Fallback to any existing profile
        cfg.default_profile = sorted(cfg.profiles.keys())[0]

    return cfg


def save_config(cfg: Config, path: Path | None = None) -> None:
    """Persist configuration to disk and keyring."""
    config_path = path or _default_config_path()
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)

    # Persist secrets to keyring, omit them from JSON
    if keyring:
        for name, profile in cfg.profiles.items():
            try:
                if profile.api_key is not None:
                    keyring.set_password(
                        SERVICE_NAME, f"{name}-apikey", profile.api_key
                    )
                if profile.token is not None:
                    keyring.set_password(SERVICE_NAME, f"{name}-token", profile.token)
            except KeyringError:
                # Don't fail the entire save if keyring is unavailable
                pass

    serializable_profiles: Dict[str, dict] = {}
    for name, profile in cfg.profiles.items():
        data = asdict(profile)
        data.pop("api_key", None)
        data.pop("token", None)
        serializable_profiles[name] = data

    payload = {
        "default_profile": cfg.default_profile,
        "profiles": serializable_profiles,
    }

    config_path.write_text(json.dumps(payload, indent=2))


def resolve_profile_name(
    cfg: Config,
    cli_profile: str | None,
    env_profile: str | None = None,
) -> str:
    """Determine which profile name to use, mirroring the Go CLI precedence."""
    if cli_profile:
        return cli_profile
    if env_profile:
        return env_profile
    if cfg.default_profile:
        return cfg.default_profile
    # Fallback to "default" and ensure it exists
    if "default" not in cfg.profiles:
        cfg.profiles["default"] = Profile(name="default")
    cfg.default_profile = "default"
    return "default"


def env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() in {"1", "true", "yes", "on"}
