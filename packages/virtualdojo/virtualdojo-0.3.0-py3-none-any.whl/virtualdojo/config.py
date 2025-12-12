"""Configuration management for VirtualDojo CLI."""

import os
import sys
from pathlib import Path
from typing import Optional

import keyring
import platformdirs
import tomli_w
from pydantic import BaseModel, Field

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from .exceptions import ConfigurationError, ProfileNotFoundError

# Keyring service name for secure credential storage
KEYRING_SERVICE = "virtualdojo-cli"

APP_NAME = "virtualdojo"
APP_AUTHOR = "Quote-ly"


def get_config_dir() -> Path:
    """Get the configuration directory for the current platform."""
    config_dir = Path(platformdirs.user_config_dir(APP_NAME, APP_AUTHOR))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.toml"


def get_credentials_file() -> Path:
    """Get the path to the credentials file (stored separately for security)."""
    return get_config_dir() / "credentials.toml"


class Profile(BaseModel):
    """A server profile configuration."""

    name: str
    server: str
    tenant: str
    default_limit: int = 100
    output_format: str = "table"


class Credentials(BaseModel):
    """Stored credentials for a profile."""

    profile_name: str
    token_type: str = "jwt"  # "jwt" or "api_key"
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[float] = None
    user_email: Optional[str] = None
    user_id: Optional[str] = None


class Config(BaseModel):
    """Main configuration model."""

    default_profile: Optional[str] = None
    output_format: str = "table"
    default_limit: int = 100
    profiles: dict[str, Profile] = Field(default_factory=dict)


class ConfigManager:
    """Manages CLI configuration and credentials."""

    def __init__(self):
        self._config: Optional[Config] = None
        self._credentials: dict[str, Credentials] = {}

    @property
    def config(self) -> Config:
        """Get the current configuration, loading if necessary."""
        if self._config is None:
            self._load_config()
        return self._config  # type: ignore

    def _load_config(self) -> None:
        """Load configuration from file."""
        config_file = get_config_file()
        if config_file.exists():
            with open(config_file, "rb") as f:
                data = tomllib.load(f)

            # Parse profiles
            profiles = {}
            for name, profile_data in data.get("profiles", {}).items():
                profile_data["name"] = name
                profiles[name] = Profile(**profile_data)

            self._config = Config(
                default_profile=data.get("default_profile"),
                output_format=data.get("output_format", "table"),
                default_limit=data.get("default_limit", 100),
                profiles=profiles,
            )
        else:
            self._config = Config()

    def save_config(self) -> None:
        """Save configuration to file."""
        config_file = get_config_file()
        data = {
            "default_profile": self.config.default_profile,
            "output_format": self.config.output_format,
            "default_limit": self.config.default_limit,
            "profiles": {},
        }

        for name, profile in self.config.profiles.items():
            data["profiles"][name] = {
                "server": profile.server,
                "tenant": profile.tenant,
                "default_limit": profile.default_limit,
                "output_format": profile.output_format,
            }

        with open(config_file, "wb") as f:
            tomli_w.dump(data, f)

    def get_profile(self, name: Optional[str] = None) -> Profile:
        """Get a profile by name, or the default profile."""
        profile_name = name or self.config.default_profile
        if not profile_name:
            raise ConfigurationError(
                message="No profile specified and no default profile set.",
                hint="Run 'vdojo config profile add <name>' or 'vdojo login'.",
            )

        if profile_name not in self.config.profiles:
            raise ProfileNotFoundError(profile_name)

        return self.config.profiles[profile_name]

    def add_profile(self, profile: Profile, set_default: bool = False) -> None:
        """Add or update a profile."""
        self.config.profiles[profile.name] = profile
        if set_default or self.config.default_profile is None:
            self.config.default_profile = profile.name
        self.save_config()

    def remove_profile(self, name: str) -> None:
        """Remove a profile."""
        if name not in self.config.profiles:
            raise ProfileNotFoundError(name)

        del self.config.profiles[name]
        if self.config.default_profile == name:
            self.config.default_profile = (
                next(iter(self.config.profiles.keys()), None)
                if self.config.profiles
                else None
            )
        self.save_config()
        self.remove_credentials(name)

    def set_default_profile(self, name: str) -> None:
        """Set the default profile."""
        if name not in self.config.profiles:
            raise ProfileNotFoundError(name)
        self.config.default_profile = name
        self.save_config()

    def list_profiles(self) -> list[Profile]:
        """List all profiles."""
        return list(self.config.profiles.values())

    # Credentials management

    def _load_credentials(self) -> None:
        """Load credentials from file and keyring."""
        creds_file = get_credentials_file()
        if creds_file.exists():
            with open(creds_file, "rb") as f:
                data = tomllib.load(f)

            for name, cred_data in data.get("credentials", {}).items():
                cred_data["profile_name"] = name

                # Try to load tokens from keyring first
                if cred_data.get("uses_keyring"):
                    try:
                        token = keyring.get_password(KEYRING_SERVICE, f"{name}_token")
                        if token:
                            cred_data["token"] = token
                        refresh_token = keyring.get_password(
                            KEYRING_SERVICE, f"{name}_refresh_token"
                        )
                        if refresh_token:
                            cred_data["refresh_token"] = refresh_token
                    except Exception:
                        # Keyring errors (NoKeyringError, KeyringLocked, etc.)
                        # Token might be lost if keyring was available before but isn't now
                        pass

                # Remove uses_keyring flag before creating Credentials object
                cred_data.pop("uses_keyring", None)
                self._credentials[name] = Credentials(**cred_data)

    def _save_credentials(self) -> None:
        """Save credentials to file and keyring.

        Sensitive tokens are stored in the system keyring when available.
        Non-sensitive metadata is stored in the credentials file.
        """
        creds_file = get_credentials_file()
        data = {"credentials": {}}

        for name, creds in self._credentials.items():
            keyring_available = False

            # Store tokens in keyring (secure storage)
            if creds.token is not None:
                try:
                    keyring.set_password(KEYRING_SERVICE, f"{name}_token", creds.token)
                    # Verify we can read it back (some backends silently fail)
                    if keyring.get_password(KEYRING_SERVICE, f"{name}_token"):
                        keyring_available = True
                except Exception:
                    # Catch all keyring errors: NoKeyringError, PasswordSetError,
                    # KeyringLocked, InitError, etc. Fall back to file storage.
                    pass

            if creds.refresh_token is not None and keyring_available:
                try:
                    keyring.set_password(
                        KEYRING_SERVICE, f"{name}_refresh_token", creds.refresh_token
                    )
                except Exception:
                    pass

            # Store non-sensitive metadata in file
            cred_data = {"token_type": creds.token_type}

            # Only store tokens in file if keyring is not available
            if keyring_available:
                cred_data["uses_keyring"] = True
            else:
                # Keyring not available, store in file
                if creds.token is not None:
                    cred_data["token"] = creds.token
                if creds.refresh_token is not None:
                    cred_data["refresh_token"] = creds.refresh_token

            if creds.expires_at is not None:
                cred_data["expires_at"] = creds.expires_at
            if creds.user_email is not None:
                cred_data["user_email"] = creds.user_email
            if creds.user_id is not None:
                cred_data["user_id"] = creds.user_id
            data["credentials"][name] = cred_data

        # Secure file creation: create with restricted permissions from the start
        creds_file_path = str(creds_file)
        try:
            # Remove existing file if present (to avoid permission issues)
            if creds_file.exists():
                creds_file.unlink()

            # Create file with secure permissions (0o600 = owner read/write only)
            fd = os.open(creds_file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "wb") as f:
                tomli_w.dump(data, f)
        except OSError:
            # Fallback for systems that don't support os.open with mode
            with open(creds_file, "wb") as f:
                tomli_w.dump(data, f)
            creds_file.chmod(0o600)

    def get_credentials(self, profile_name: str) -> Optional[Credentials]:
        """Get credentials for a profile."""
        if not self._credentials:
            self._load_credentials()
        return self._credentials.get(profile_name)

    def save_credentials(self, credentials: Credentials) -> None:
        """Save credentials for a profile."""
        if not self._credentials:
            self._load_credentials()
        self._credentials[credentials.profile_name] = credentials
        self._save_credentials()

    def remove_credentials(self, profile_name: str) -> None:
        """Remove credentials for a profile from file and keyring."""
        if not self._credentials:
            self._load_credentials()

        # Remove from keyring (ignore all errors - keyring may not be available)
        try:
            keyring.delete_password(KEYRING_SERVICE, f"{profile_name}_token")
        except Exception:
            pass
        try:
            keyring.delete_password(KEYRING_SERVICE, f"{profile_name}_refresh_token")
        except Exception:
            pass

        if profile_name in self._credentials:
            del self._credentials[profile_name]
            self._save_credentials()

    def has_credentials(self, profile_name: str) -> bool:
        """Check if credentials exist for a profile."""
        if not self._credentials:
            self._load_credentials()
        creds = self._credentials.get(profile_name)
        return creds is not None and creds.token is not None


# Global config manager instance
config_manager = ConfigManager()


def get_current_profile(name: Optional[str] = None) -> Profile:
    """Get the current profile."""
    return config_manager.get_profile(name)


def get_current_credentials(profile_name: Optional[str] = None) -> Optional[Credentials]:
    """Get credentials for the current or specified profile."""
    profile = get_current_profile(profile_name)
    return config_manager.get_credentials(profile.name)
