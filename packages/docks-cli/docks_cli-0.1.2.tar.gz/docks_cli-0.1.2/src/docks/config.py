"""Configuration management for Docks CLI."""

import os
import sys
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


CONFIG_DIR = Path.home() / ".docks"
CONFIG_FILE = CONFIG_DIR / "config.toml"
TOKEN_FILE = CONFIG_DIR / "token"


class Settings(BaseSettings):
    """Docks CLI settings."""

    model_config = SettingsConfigDict(env_prefix="DOCKS_", env_file=".env")

    api_url: str = Field(
        default="https://api.docks.thecontextlab.ai",
        description="Docks API URL",
    )
    tenant_id: Optional[str] = Field(default=None, description="Tenant UUID")
    token: Optional[str] = Field(default=None, description="JWT token")
    profile: str = Field(default="default", description="Config profile name")
    gcs_bucket: str = Field(
        default="gs://izumi-harbor-datasets",
        description="GCS bucket for prebaked images",
    )
    gcp_project: str = Field(default="izumi-479101", description="GCP project ID")
    gcp_region: str = Field(default="us-west2", description="GCP region")
    default_model: str = Field(
        default="claude-sonnet-4-5-20250929",
        description="Default model for evaluation runs",
    )
    default_concurrent: int = Field(
        default=32,
        description="Default max concurrent trials",
    )
    default_attempts: int = Field(
        default=1,
        description="Default attempts per task",
    )
    default_timeout_minutes: int = Field(
        default=30,
        description="Default agent timeout in minutes",
    )


def load_config(profile: str = "default") -> Settings:
    """Load settings from config file and environment."""
    settings = Settings()

    # Override with config file if it exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "rb") as f:
            config = tomllib.load(f)

        if profile in config:
            profile_config = config[profile]
            if "api_url" in profile_config:
                settings.api_url = profile_config["api_url"]
            if "tenant_id" in profile_config:
                settings.tenant_id = profile_config["tenant_id"]
            if "token" in profile_config:
                settings.token = profile_config["token"]
            if "gcs_bucket" in profile_config:
                settings.gcs_bucket = profile_config["gcs_bucket"]
            if "gcp_project" in profile_config:
                settings.gcp_project = profile_config["gcp_project"]
            if "gcp_region" in profile_config:
                settings.gcp_region = profile_config["gcp_region"]

    # Load token from file if not in config
    if not settings.token and TOKEN_FILE.exists():
        settings.token = TOKEN_FILE.read_text().strip()

    return settings


def save_config(
    profile: str,
    api_url: Optional[str] = None,
    tenant_id: Optional[str] = None,
    token: Optional[str] = None,
) -> None:
    """Save settings to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing config or create empty
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "rb") as f:
            config = tomllib.load(f)

    # Update profile
    if profile not in config:
        config[profile] = {}

    if api_url:
        config[profile]["api_url"] = api_url
    if tenant_id:
        config[profile]["tenant_id"] = tenant_id

    # Write config (we need to convert to TOML string manually)
    with open(CONFIG_FILE, "w") as f:
        for section, values in config.items():
            f.write(f"[{section}]\n")
            for key, value in values.items():
                if isinstance(value, str):
                    f.write(f'{key} = "{value}"\n')
                else:
                    f.write(f"{key} = {value}\n")
            f.write("\n")

    # Save token separately (more secure)
    if token:
        TOKEN_FILE.write_text(token)
        TOKEN_FILE.chmod(0o600)


def clear_token() -> None:
    """Remove saved token."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()


def get_headers(settings: Settings) -> dict[str, str]:
    """Get HTTP headers with auth token."""
    headers = {"Content-Type": "application/json"}
    if settings.token:
        # Handle both "Bearer xxx" and raw token
        token = settings.token
        if not token.startswith("Bearer "):
            token = f"Bearer {token}"
        headers["Authorization"] = token
    return headers
