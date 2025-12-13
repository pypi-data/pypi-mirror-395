"""Centralized logging initialization for all entry points.

Provides a single source of truth for lib_log_rich runtime configuration,
eliminating duplication between module entry (__main__.py) and console script
(cli.py) while ensuring initialization happens exactly once.

Contents:
    * :class:`LoggingConfig` – Pydantic model for logging configuration.
    * :func:`init_logging` – idempotent logging initialization with layered config.
    * :func:`_build_runtime_config` – constructs RuntimeConfig from layered sources.

System Role:
    Lives in the adapters/platform layer. All entry points (module execution,
    console scripts, tests) delegate to this module for logging setup, ensuring
    consistent runtime behavior across invocation paths.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

import lib_log_rich.config
import lib_log_rich.runtime

from . import __init__conf__
from .config import get_config


class LoggingConfig(BaseModel):
    """Pydantic model for logging configuration with defaults.

    Provides validated logging configuration with sensible defaults for
    the application. Maps directly to lib_log_rich.runtime.RuntimeConfig
    parameters.

    Attributes:
        service: Service name for log identification.
        environment: Environment label (e.g., "prod", "dev").

    Note:
        Additional fields from lib_log_rich are passed through via model_extra.
    """

    model_config = ConfigDict(extra="allow", frozen=True)

    service: str
    environment: str = "prod"


# Module-level storage for the runtime configuration
# Set during init_logging() for potential future use
_runtime_config: lib_log_rich.runtime.RuntimeConfig | None = None


def _load_logging_config() -> LoggingConfig:
    """Load and validate logging configuration from layered sources.

    Loads configuration from the [lib_log_rich] section and validates it
    through the LoggingConfig Pydantic model, providing defaults for
    required fields.

    Returns:
        Validated logging configuration with defaults applied.
    """
    config = get_config()
    log_config_raw: Any = config.get("lib_log_rich", default={})

    # Ensure we have a dict-like structure
    log_config_dict: dict[str, Any] = dict(log_config_raw) if log_config_raw else {}

    # Provide default for required 'service' field if not present
    if "service" not in log_config_dict:
        log_config_dict["service"] = __init__conf__.name

    return LoggingConfig.model_validate(log_config_dict)


def _build_runtime_config() -> lib_log_rich.runtime.RuntimeConfig:
    """Build RuntimeConfig from layered configuration sources.

    Centralizes the mapping from lib_layered_config to lib_log_rich
    RuntimeConfig, ensuring all configuration sources (defaults, app,
    host, user, dotenv, env) are respected. Loads configuration via
    get_config() and extracts the [lib_log_rich] section, validating
    through LoggingConfig Pydantic model.

    Returns:
        Fully configured runtime settings ready for lib_log_rich.init().

    Note:
        Configuration is read from the [lib_log_rich] section. All parameters
        documented in defaultconfig.toml can be specified. Unspecified values
        use lib_log_rich's built-in defaults. The service and environment
        parameters default to package metadata when not configured.
    """
    logging_config = _load_logging_config()

    # Build RuntimeConfig using Pydantic's model_dump for conversion
    # model_dump() exports all fields including extra fields
    return lib_log_rich.runtime.RuntimeConfig(**logging_config.model_dump())


def init_logging() -> None:
    """Initialize lib_log_rich runtime with layered configuration if not already done.

    All entry points need logging configured, but the runtime should only
    be initialized once regardless of how many times this function is called.
    Loads .env files (to make LOG_* variables available), checks if lib_log_rich
    is already initialized, and configures it with settings from layered
    configuration sources (defaults → app → host → user → dotenv → env).
    Bridges standard Python logging to lib_log_rich for domain code compatibility.

    Side Effects:
        Loads .env files into the process environment on first invocation.
        May initialize the global lib_log_rich runtime on first invocation.
        Subsequent calls have no effect.

    Note:
        This function is safe to call multiple times. The first call loads .env
        and initializes the runtime; subsequent calls check the initialization
        state and return immediately if already initialized.

        The .env loading enables lib_log_rich to read LOG_* environment variables
        from .env files in the current directory or parent directories. This
        provides the highest precedence override mechanism for logging configuration.

        The logger_level for attach_std_logging is derived from the console_level
        configuration to ensure standard logging uses the same threshold.
    """

    if not lib_log_rich.runtime.is_initialised():
        global _runtime_config

        # Enable .env file discovery and loading before runtime initialization
        # This allows LOG_* variables from .env files to override configuration
        lib_log_rich.config.enable_dotenv()

        _runtime_config = _build_runtime_config()
        lib_log_rich.runtime.init(_runtime_config)
        lib_log_rich.runtime.attach_std_logging()


__all__ = [
    "init_logging",
]
