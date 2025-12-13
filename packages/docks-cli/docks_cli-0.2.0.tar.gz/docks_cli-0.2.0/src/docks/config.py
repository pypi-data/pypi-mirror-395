"""Configuration management for Docks CLI.

Token Storage:
    Tokens are stored securely using the OS keyring by default:
    - macOS: Keychain
    - Linux: Secret Service (GNOME Keyring, KDE Wallet)
    - Windows: Windows Credential Manager

    Falls back to file-based storage (~/.docks/token) if keyring is unavailable.

Environment Variables:
    DOCKS_USE_KEYRING: Set to "false" to disable keyring (default: true)
    DOCKS_TOKEN: Override token via environment variable
"""

import logging
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

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".docks"
CONFIG_FILE = CONFIG_DIR / "config.toml"
TOKEN_FILE = CONFIG_DIR / "token"  # Legacy fallback

# Keyring configuration
KEYRING_SERVICE = "docks-cli"
KEYRING_AVAILABLE = False

# Try to import keyring
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    keyring = None  # type: ignore


def _use_keyring() -> bool:
    """Check if keyring should be used."""
    if not KEYRING_AVAILABLE:
        return False
    return os.getenv("DOCKS_USE_KEYRING", "true").lower() != "false"


def _get_keyring_key(profile: str) -> str:
    """Get the keyring key for a profile."""
    return f"token-{profile}"


def save_token_secure(token: str, profile: str = "default") -> bool:
    """Save token to secure storage (keyring or file).

    Args:
        token: The JWT token to save
        profile: Config profile name

    Returns:
        True if saved to keyring, False if saved to file
    """
    if _use_keyring():
        try:
            keyring.set_password(KEYRING_SERVICE, _get_keyring_key(profile), token)
            logger.debug(f"Token saved to keyring for profile '{profile}'")
            # Remove file-based token if it exists (migration)
            if TOKEN_FILE.exists():
                TOKEN_FILE.unlink()
                logger.debug("Migrated from file-based token to keyring")
            return True
        except Exception as e:
            logger.warning(f"Failed to save token to keyring: {e}")

    # Fallback to file-based storage
    CONFIG_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    TOKEN_FILE.write_text(token)
    TOKEN_FILE.chmod(0o600)
    logger.debug("Token saved to file (keyring unavailable)")
    return False


def load_token_secure(profile: str = "default") -> Optional[str]:
    """Load token from secure storage (keyring or file).

    Args:
        profile: Config profile name

    Returns:
        The JWT token or None if not found
    """
    # Check environment variable first
    env_token = os.getenv("DOCKS_TOKEN")
    if env_token:
        return env_token

    # Try keyring
    if _use_keyring():
        try:
            token = keyring.get_password(KEYRING_SERVICE, _get_keyring_key(profile))
            if token:
                logger.debug(f"Token loaded from keyring for profile '{profile}'")
                return token
        except Exception as e:
            logger.warning(f"Failed to load token from keyring: {e}")

    # Fallback to file-based storage
    if TOKEN_FILE.exists():
        logger.debug("Token loaded from file (legacy)")
        return TOKEN_FILE.read_text().strip()

    return None


def clear_token_secure(profile: str = "default") -> None:
    """Clear token from all storage locations.

    Args:
        profile: Config profile name
    """
    # Clear from keyring
    if _use_keyring():
        try:
            keyring.delete_password(KEYRING_SERVICE, _get_keyring_key(profile))
            logger.debug(f"Token cleared from keyring for profile '{profile}'")
        except Exception:
            pass  # Ignore if not found

    # Clear file-based token
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        logger.debug("Token file removed")


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

    # Load token from secure storage if not in config
    if not settings.token:
        settings.token = load_token_secure(profile)

    return settings


def save_config(
    profile: str,
    api_url: Optional[str] = None,
    tenant_id: Optional[str] = None,
    token: Optional[str] = None,
) -> bool:
    """Save settings to config file.

    Args:
        profile: Config profile name
        api_url: API URL to save
        tenant_id: Tenant UUID to save
        token: JWT token to save securely

    Returns:
        True if token was saved to keyring, False otherwise
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

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
    CONFIG_FILE.chmod(0o600)

    # Save token to secure storage
    if token:
        return save_token_secure(token, profile)
    return False


def clear_token(profile: str = "default") -> None:
    """Remove saved token from all storage locations.

    Args:
        profile: Config profile name
    """
    clear_token_secure(profile)


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
