import os
import tempfile
import unittest
import unittest.mock

import pytest
import yaml

from preheat_open.configuration import (
    CacheConfig,
    CaseConverter,
    ConfigBase,
    ConfigLoader,
    LoggingConfig,
    NeogridApiConfig,
    PersonalConfig,
    RuntimeMode,
    RuntimeModeError,
    UpdateProxy,
    _env_var_name,
    run_if_production_mode,
)

# === Fixtures ===


@pytest.fixture
def clean_env():
    """Fixture to provide a clean environment for tests."""
    old_environ = os.environ.copy()
    os.environ.clear()
    # Ensure runtime mode is set to TEST
    os.environ["PREHEAT_RUNTIME_MODE"] = str(RuntimeMode.TEST.value)
    yield
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as tmp:
        test_config = {
            "personal": {
                "name": "Test User",
                "email": "test@example.com",
                "timezone": "UTC",
            },
            "logging": {"level": 20, "auto_setup": False},  # INFO
            "neogrid_api": {
                "token": "test-token",
                "url": "https://test-api.example.com",
            },
        }
        yaml.dump(test_config, tmp)

    yield tmp.name

    # Clean up
    os.unlink(tmp.name)


@pytest.fixture
def test_config_class():
    """Create a test configuration class."""

    class TestConfig(ConfigBase):
        test_string: str = "default"
        test_int: int = 42
        test_float: float = 3.14
        _sensitive_fields: set[str] = {"test_string"}

    return TestConfig


# === Tests for ConfigBase and its methods ===


def test_config_base_init(clean_env, test_config_class):
    """Test initialization of a ConfigBase class."""
    os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] = "from_env"
    os.environ["PREHEAT_TESTCONFIG_TEST_INT"] = "100"

    config = test_config_class()

    assert config.test_string == "from_env"
    assert config.test_int == 100
    assert config.test_float == 3.14  # unchanged


def test_update_proxy(clean_env, test_config_class):
    """Test UpdateProxy for modifying config and environment variables."""
    config = test_config_class()

    # Test setting a value through the proxy
    config.update.test_string = "updated"

    # Check that both config and environment were updated
    assert config.test_string == "updated"
    assert os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] == "updated"

    # Test the .all() method
    config.test_int = 999  # Directly set attribute (env not updated)
    config.update.all()
    assert os.environ["PREHEAT_TESTCONFIG_TEST_INT"] == "999"

    # Test error on non-existent attribute
    with pytest.raises(AttributeError):
        config.update.nonexistent = "value"


def test_temporary_context(clean_env, test_config_class):
    """Test the temporary context manager for environment variables."""
    # Set initial environment
    os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] = "initial"

    config = test_config_class()
    assert config.test_string == "initial"

    # Modify the config but not the environment
    config.test_string = "modified"
    assert config.test_string == "modified"
    assert os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] == "initial"

    # Use the temporary context
    with config.temporary():
        assert os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] == "modified"
        config.update.test_string = "in_context"
        assert os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] == "in_context"

    # Environment should be restored after context
    assert os.environ["PREHEAT_TESTCONFIG_TEST_STRING"] == "initial"
    # But config object should keep its value
    assert config.test_string == "in_context"


def test_pretty_print(clean_env, test_config_class):
    """Test pretty printing of configuration with/without anonymization."""
    config = test_config_class()
    config.test_string = "sensitive data"

    # Test anonymized printing (default in non-development mode)
    assert "*****" in config.pretty_print()
    assert "sensitive data" not in config.pretty_print()

    # Test non-anonymized printing
    assert "sensitive data" in config.pretty_print(anonymize=False)

    # Test str representation
    assert str(config) == config.pretty_print()


def test_iter_items(clean_env, test_config_class):
    """Test iteration over configuration items."""
    config = test_config_class()

    items = dict(config.iter_items())
    assert "test_string" in items
    assert "test_int" in items
    assert "test_float" in items
    assert "_sensitive_fields" not in items  # Private attributes excluded
    assert "update" not in items  # Properties excluded
    assert "iter_items" not in items  # Methods excluded


# === Tests for specific configuration subclasses ===


def test_personal_config(clean_env):
    """Test PersonalConfig class."""
    os.environ["PREHEAT_PERSONALCONFIG_NAME"] = "John Doe"
    os.environ["PREHEAT_PERSONALCONFIG_EMAIL"] = "john@example.com"

    config = PersonalConfig()

    assert config.name == "John Doe"
    assert config.email == "john@example.com"
    assert "name" in config._sensitive_fields
    assert "email" in config._sensitive_fields


def test_logging_config(clean_env, monkeypatch):
    """Test LoggingConfig class."""
    # Mock the actual logging setup to avoid side effects
    setup_mock = unittest.mock.Mock()
    monkeypatch.setattr(LoggingConfig, "setup_logging", setup_mock)

    # Test without auto_setup
    config = LoggingConfig()
    assert setup_mock.call_count == 0

    # Test with auto_setup
    os.environ["PREHEAT_LOGGINGCONFIG_AUTO_SETUP"] = "True"
    config = LoggingConfig()
    assert setup_mock.call_count == 1


def test_cache_config(clean_env):
    """Test CacheConfig class."""
    os.environ["PREHEAT_CACHECONFIG_SIZE_LIMIT"] = "1000000"
    os.environ["PREHEAT_CACHECONFIG_TIME_TO_LIVE"] = "3600"

    config = CacheConfig()

    assert config.size_limit == 1000000.0
    assert config.time_to_live == 3600


def test_neogrid_api_config(clean_env):
    """Test NeogridApiConfig class."""
    os.environ["PREHEAT_NEOGRIDAPICONFIG_TOKEN"] = "secret-token"
    os.environ["PREHEAT_NEOGRIDAPICONFIG_URL"] = "https://api.example.com"

    config = NeogridApiConfig()

    assert config.token == "secret-token"
    assert config.url == "https://api.example.com"
    assert "token" in config._sensitive_fields


# === Tests for ConfigLoader ===


def test_config_loader_with_file(clean_env, temp_config_file):
    """Test ConfigLoader with a file path."""
    loader = ConfigLoader(path=temp_config_file)

    # Check that environment variables were set correctly
    assert os.environ["PREHEAT_PERSONALCONFIG_NAME"] == "Test User"
    assert os.environ["PREHEAT_PERSONALCONFIG_EMAIL"] == "test@example.com"
    assert os.environ["PREHEAT_LOGGINGCONFIG_LEVEL"] == "20"
    assert os.environ["PREHEAT_NEOGRIDAPICONFIG_TOKEN"] == "test-token"


def test_config_loader_with_data(clean_env):
    """Test ConfigLoader with direct data."""
    test_data = {"personal": {"name": "Data User", "email": "data@example.com"}}

    loader = ConfigLoader(data=test_data)

    # Check that environment variables were set correctly
    assert os.environ["PREHEAT_PERSONALCONFIG_NAME"] == "Data User"
    assert os.environ["PREHEAT_PERSONALCONFIG_EMAIL"] == "data@example.com"


# === Tests for utility functions ===


def test_env_var_name():
    """Test environment variable name generation."""

    class TestConfig(ConfigBase):
        test_param: str = ""

    # Test with class
    assert _env_var_name(TestConfig, "test_param") == "PREHEAT_TESTCONFIG_TEST_PARAM"

    # Test with instance
    config = TestConfig()
    assert _env_var_name(config, "test_param") == "PREHEAT_TESTCONFIG_TEST_PARAM"

    # Test runtime_mode special case
    assert _env_var_name(config, "runtime_mode") == "PREHEAT_RUNTIME_MODE"


def test_case_converter():
    """Test the CaseConverter utility."""
    converter = CaseConverter()

    # Test snake to pascal
    assert converter.snake_to_pascal("test_case") == "TestCase"
    assert converter.snake_to_pascal("multiple_word_case") == "MultipleWordCase"

    # Test pascal to snake
    assert converter.pascal_to_snake("TestCase") == "test_case"
    assert converter.pascal_to_snake("MultipleWordCase") == "multiple_word_case"
    assert converter.pascal_to_snake("ABCTest") == "abc_test"


def test_runtime_mode():
    """Test RuntimeMode enum."""
    # Test equality
    assert RuntimeMode.PRODUCTION == RuntimeMode.PRODUCTION
    assert RuntimeMode.PRODUCTION == 0
    assert RuntimeMode.DEVELOPMENT == 10
    assert RuntimeMode.TEST == 20

    # Test inequality
    assert RuntimeMode.PRODUCTION != RuntimeMode.DEVELOPMENT
    assert RuntimeMode.DEVELOPMENT != RuntimeMode.TEST
    assert RuntimeMode.PRODUCTION != "production"


def test_run_if_production_mode():
    """Test run_if_production_mode function."""
    test_func = unittest.mock.Mock(return_value="executed")

    # Should run in production mode
    result = run_if_production_mode(
        function=test_func,
        runtime_mode=RuntimeMode.PRODUCTION.value,
        arg1="arg1",
        arg2="value",
    )
    assert result == "executed"
    test_func.assert_called_once_with(arg1="arg1", arg2="value")

    test_func.reset_mock()

    # Should not run in other modes
    result = run_if_production_mode(
        function=test_func, runtime_mode=RuntimeMode.DEVELOPMENT.value, arg1="arg1"
    )
    assert result is None
    test_func.assert_not_called()
