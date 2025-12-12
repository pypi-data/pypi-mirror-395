"""
sai_akruti: Centralized Settings Loader for Python Apps.

This package includes:
- Settings: Base settings management using pydantic-settings.
- Sources: Custom sources for loading from dotenv files, AWS SSM, and Secrets Manager.
"""

from .settings import Settings
from .sources import (
    MultiDotEnvSettingsSource,
    SSMSettingsSource,
    SecretsManagerSettingsSource
)

__all__ = [
    "Settings",
    "MultiDotEnvSettingsSource",
    "SSMSettingsSource",
    "SecretsManagerSettingsSource",
]
