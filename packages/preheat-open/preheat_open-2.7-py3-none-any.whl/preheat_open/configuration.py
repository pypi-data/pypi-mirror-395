# pylint: disable=E1101
from __future__ import annotations

import logging
import os
import re
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Generator, Generic, Optional, Type, TypeVar, Union

import yaml

logger = logging.getLogger(__name__)

_USUAL_CONFIG_PATHS = [
    "~/.preheat",
    "/etc/opt/preheat",
    "/etc/preheat",
]

_ENV_PREFIX = "PREHEAT_"


def _env_var_name(obj: ConfigBase | Type[ConfigBase], parameter: str) -> str:
    """Generate environment variable name for a given parameter.

    Args:
        obj (ConfigBase): The configuration object
        parameter (str): The parameter name

    Returns:
        str: The environment variable name
    """
    class_name = obj.__name__ if isinstance(obj, type) else obj.__class__.__name__
    if parameter == "runtime_mode":
        return f"{_ENV_PREFIX}RUNTIME_MODE"
    return f"{_ENV_PREFIX}{class_name.upper()}_{parameter.upper()}"


class UpdateProxy:
    """Proxy object that allows updating environment variables for configuration properties."""

    def __init__(self, config_obj):
        self._config_obj: ConfigBase = config_obj

    def all(self) -> None:
        """Update all environment variables to match the current configuration object."""
        for key, value in self._config_obj.iter_items():
            if not key.startswith("_") and not callable(getattr(self._config_obj, key)):
                os.environ[_env_var_name(self._config_obj, key)] = str(value)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_config_obj":
            # Allow setting the internal reference
            super().__setattr__(name, value)
            return

        if (
            hasattr(self._config_obj, name)
            and not name.startswith("_")
            and not callable(getattr(self._config_obj, name))
        ):
            # Update environment variable
            os.environ[_env_var_name(self._config_obj, name)] = str(value)
            # Update the actual attribute
            setattr(self._config_obj, name, value)
        else:
            raise AttributeError(
                f"{self._config_obj.__class__.__name__} has no attribute '{name}'"
            )


T = TypeVar("T", bound="ConfigBase")


class ConfigBase:
    """Base class for all configuration objects.

    This class provides common functionality for all configuration classes,
    including environment variable access and sensitive data handling.

    Attributes:
        runtime_mode (int): The current runtime mode
    """

    runtime_mode: int = 10
    _sensitive_fields: set[str] = set()

    def __init__(self):
        """Initialize configuration from environment variables."""
        self._update_proxy = UpdateProxy(self)
        self._load_from_env()

    @property
    def update(self) -> UpdateProxy:
        """Get a proxy object to update configuration attributes and environment variables."""
        return self._update_proxy

    def iter_items(self) -> Generator[tuple[str, Any], None, None]:
        """Iterate over all attributes of the configuration object.

        Yields:
            tuple[str, Any]: A tuple of attribute name and value
        """
        for key in dir(self):
            if (
                not key.startswith("_")
                and not callable(getattr(self, key))
                and key != "update"
            ):
                yield key, getattr(self, key)

    class TempContext(Generic[T]):
        """Context manager for temporarily setting environment variables."""

        def __init__(self, config_obj: T):
            self.config_obj = config_obj
            self.original_env = {}

        def __enter__(self) -> T:
            # Save original environment variable values
            for key, value in self.config_obj.iter_items():
                env_var = _env_var_name(self.config_obj, key)
                self.original_env[env_var] = os.environ.get(env_var)

            # Update environment variables with current config values
            self.config_obj.update.all()
            return self.config_obj

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Restore original environment variables
            for env_var, value in self.original_env.items():
                if value is None:
                    if env_var in os.environ:
                        del os.environ[env_var]
                else:
                    os.environ[env_var] = value

    def temporary(self: T) -> TempContext[T]:
        """Return a context manager that temporarily sets environment variables.

        Usage:
            with config.temporary():
                # Environment variables reflect config values here
            # Original environment variables restored here

        Returns:
            TempContext: A context manager that preserves the specific config type
        """
        return self.TempContext(self)

    def _load_from_env(self):
        """Load configuration values from environment variables."""

        for key, value in self.iter_items():
            type_ = type(value)

            env_value = os.environ.get(_env_var_name(self, key))
            if env_value is not None:
                setattr(self, key, type_(env_value))

        logger.debug("Loaded configuration: %s", self.pretty_print())

    def __str__(self) -> str:
        return self.pretty_print()

    def pretty_print(self, anonymize: bool | None = None) -> str:
        """Create a string representation with sensitive fields masked.

        Returns:
            str: String representation of the configuration
        """
        anonymize = (
            self.runtime_mode != RuntimeMode.DEVELOPMENT.value
            if anonymize is None
            else anonymize
        )
        attrs = [
            f"{key}={'*****' if key in self._sensitive_fields and anonymize else value}"
            for key, value in self.iter_items()
        ]

        return f"{self.__class__.__name__}({', '.join(attrs)})"


class PersonalConfig(ConfigBase):
    """Personal configuration settings.

    Holds personal identification and preferences information.

    Attributes:
        name (str): The user's name
        email (str): The user's email address
        timezone (str): The user's timezone
        runtime_mode (int): The current runtime mode
    """

    name: str = ""
    email: str = ""
    timezone: str = ""
    _sensitive_fields: set[str] = {"name", "email"}


class LoggingConfig(ConfigBase):
    """Logging configuration settings.

    Controls the application's logging behavior.

    Attributes:
        level (int): The logging level (corresponds to standard logging levels)
        format (str): The format string for log messages
        auto_setup (bool): Whether to automatically set up logging on initialization
        directory (str): Path to the log directory
        library_name (str): Name of the library for logger namespace
        runtime_mode (int): The current runtime mode
    """

    level: int = logging.INFO
    format: str = "%(asctime)-23s  %(levelname)-8s  %(name)-32s  %(message)-80s"
    auto_setup: bool = False
    directory: str = "~/.preheat/.logs"

    def __init__(self):
        super().__init__()
        if self.auto_setup:
            self.setup_logging()

    def setup_logging(self) -> None:
        """Set up logging based on the configuration."""
        # Automatically determine the library name from the module structure
        library_name = self._get_library_name()

        # Create log directory if it doesn't exist
        log_dir = Path(self.directory).expanduser()
        log_dir.mkdir(parents=True, exist_ok=True)

        # Get timestamp for log file
        today = datetime.now()
        file_name = f"{library_name}-{today.strftime('%Y-%m-%d %H:%M:%S')}.log"

        # Reset only loggers that belong to our application
        for logger_name in list(logging.root.manager.loggerDict.keys()):
            if logger_name.startswith(library_name):
                logger_instance = logging.getLogger(logger_name)
                # Save the propagate setting to restore it later
                propagate = logger_instance.propagate
                # Remove handlers
                for handler in logger_instance.handlers[:]:
                    logger_instance.removeHandler(handler)
                    handler.close()
                # Set level but don't change propagate setting
                logger_instance.setLevel(self.level)
                logger_instance.propagate = propagate

        # Create handlers
        file_handler = logging.FileHandler(log_dir / file_name)
        stream_handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter(self.format)
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Configure the root logger for our application's modules
        lib_logger = logging.getLogger(library_name)
        lib_logger.setLevel(self.level)
        lib_logger.handlers = []  # Clear any existing handlers
        lib_logger.addHandler(file_handler)
        lib_logger.addHandler(stream_handler)
        lib_logger.propagate = False  # Don't propagate to root logger

        logger.debug(f"Logging configured for {library_name} with level: {self.level}")

    def _get_library_name(self) -> str:
        """Automatically determine the library name from the module structure.

        Returns:
            str: The top-level package name
        """
        # Get the module name of this file (e.g., 'preheat_open.api.configuration')
        module_name = __name__

        # Extract the top-level package name (e.g., 'preheat_open')
        parts = module_name.split(".")
        if len(parts) > 0:
            return parts[0]

        # Fallback to a default name if we can't determine it
        return "preheat_open"


class CacheConfig(ConfigBase):
    """Cache configuration settings.

    Controls how the application caches data.

    Attributes:
        type (str): The cache type to use
        directory (str): Path to the cache directory
        size_limit (float): Maximum size of the cache in bytes
        time_to_live (int): Maximum lifetime of cached items in seconds
        runtime_mode (int): The current runtime mode
    """

    type: str = ""
    directory: str = "~/.preheat/.cache"
    size_limit: float = 5e8  # 500 MB
    time_to_live: int = 60 * 60 * 24  # 1 day


class NeogridApiConfig(ConfigBase):
    """Neogrid API configuration settings.

    Contains credentials and settings for accessing the Neogrid API.

    Attributes:
        token (str): API access token
        url (str): Base URL for API requests
        runtime_mode (int): The current runtime mode
    """

    token: str = "KVkIdWLKac5XFLCs2loKb7GUitkTL4uJXoSyUFIZkVgWuCk8Uj"
    url: str = "https://api.neogrid.dk/public/api/v1"
    _sensitive_fields: set[str] = {"token"}


class CaseConverter:
    """Convert a string to a case-insensitive version.

    This class is used to convert configuration keys to a specific case
    for easier access and comparison.

    Attributes:
        value (str): The original string value
    """

    def __init__(self):
        self.pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

    def snake_to_pascal(self, value: str) -> str:
        """Convert a snake_case string to PascalCase.

        Args:
            value (str): The snake_case string

        Returns:
            str: The converted PascalCase string
        """
        return "".join(word.capitalize() for word in value.split("_"))

    def pascal_to_snake(self, value: str) -> str:
        """Convert a PascalCase string to snake_case.

        Args:
            value (str): The PascalCase string

        Returns:
            str: The converted snake_case string
        """
        return self.pattern.sub("_", value).lower()


class ConfigLoader:
    """Loads configuration from YAML and sets environment variables.

    Responsible for loading configuration data from a YAML file and setting
    the corresponding environment variables that will be used by configuration classes.

    This loader automatically adapts to any ConfigBase subclasses in the system.
    """

    def __init__(
        self,
        data: dict | None = None,
        path: Optional[str] = None,
        force_reload: bool = True,
    ):
        """Initialize the config loader.

        Args:
            default_config_path (str): Path to the default configuration file
        """
        self.path = path or self.find_config_path()
        self.data = data or {}
        self._config_classes: list[Type] = ConfigBase.__subclasses__()
        if not self.data and self.path:
            self.load_config_file(path=self.path)

        self._set_environment_variables(force_reload=force_reload)

    def find_config_path(self) -> str | None:
        """Find the first available configuration directory and its config file.

        Searches first in private paths, then falls back to public paths.

        Returns:
            str: Path to the configuration file
        """
        for path in _USUAL_CONFIG_PATHS:
            expanded_path = Path(path).expanduser() / "config.yaml"
            if expanded_path.exists():
                return str(expanded_path)
        return None

    def load_config_file(self, path: Optional[Union[str, Path]] = None) -> None:
        """Load configuration from a YAML file.

        Args:
            file_path (Optional[Union[str, Path]]): Path to configuration file.
                If None, the default path will be used.

        Raises:
            FileNotFoundError: If the configuration file doesn't exist
        """
        path = path or self.path

        if path is None:
            raise FileNotFoundError("No configuration file path specified or found")

        path_obj = Path(path).expanduser().resolve()
        if not path_obj.exists():
            raise FileNotFoundError(f"Configuration file not found: {path_obj}")

        with open(path_obj, "r") as f:
            self.data = yaml.safe_load(f)

    def _set_environment_variables(self, force_reload: bool = False) -> None:
        """Set environment variables from loaded configuration."""
        if not self.data:
            return

        # Iterate through each config class
        for config_class in self._config_classes:
            # Determine section name from class name
            section_name = CaseConverter().pascal_to_snake(
                config_class.__name__.removesuffix("Config")
            )

            # Check if this section exists in the config data
            if section_name in self.data and isinstance(self.data[section_name], dict):
                section_data = self.data[section_name]

                # Set environment variables for each key in this section
                for key, value in section_data.items():
                    if value is not None:
                        env_var_name = _env_var_name(config_class, key)
                        if force_reload or env_var_name not in os.environ:
                            os.environ[env_var_name] = str(value)


if not any(
    caller.endswith("import ConfigLoader")
    for caller in sys._getframe(1).f_code.co_names
):
    ConfigLoader(force_reload=False)


class RuntimeMode(Enum):
    """
    Enum representing the runtime mode of the application.

    Attributes:
        PRODUCTION (int): Production mode.
        DEVELOPMENT (int): Development mode.
        TEST (int): Test mode.
    """

    PRODUCTION = 0
    DEVELOPMENT = 10
    TEST = 20

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another object.

        :param other: The object to compare with.
        :type other: object
        :return: True if equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, RuntimeMode):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        return False


def run_if_production_mode(
    function: Callable, runtime_mode: int | None = None, *args, **kwargs
) -> Any:
    """
    Runs a function if the application is in production mode.

    :param configuration: The configuration settings for the application.
    :type configuration: Configuration
    :param function: The function to run.
    :type function: callable
    """
    runtime_mode = (
        runtime_mode if runtime_mode is not None else PersonalConfig().runtime_mode
    )

    if runtime_mode == RuntimeMode.PRODUCTION.value:
        return function(*args, **kwargs)
    else:
        log = f"Function not run because application is not in production mode. Function: {function}({args}, {kwargs})"
        logger.warning(log[:1000])


class RuntimeModeError(Exception):
    """
    Exception raised for errors in the runtime mode.
    """

    pass
