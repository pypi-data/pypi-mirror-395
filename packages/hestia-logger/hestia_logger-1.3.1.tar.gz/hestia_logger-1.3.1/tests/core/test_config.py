import os
import socket
import logging
import importlib
import builtins
import pytest

from hestia_logger.core import config


@pytest.fixture(autouse=True)
def clear_env_and_reload(monkeypatch):
    # Before each test, clear relevant env vars and reload config module
    for var in [
        "ENVIRONMENT",
        "LOG_LEVEL",
        "ELASTICSEARCH_HOST",
        "ENABLE_INTERNAL_LOGGER",
        "LOGS_DIR",
        "APP_VERSION",
        "LOG_ROTATION_TYPE",
        "LOG_ROTATION_WHEN",
        "LOG_ROTATION_INTERVAL",
        "LOG_ROTATION_BACKUP_COUNT",
        "LOG_ROTATION_MAX_BYTES",
    ]:
        monkeypatch.delenv(var, raising=False)
    # Also ensure container detection files are restored to default behavior
    yield
    importlib.reload(config)


def test_app_version_default(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    importlib.reload(config)
    assert config.APP_VERSION == "1.0.0"


def test_app_version_custom(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "2.5.3")
    importlib.reload(config)
    assert config.APP_VERSION == "2.5.3"


def test_detect_container_false(monkeypatch):
    # No /.dockerenv and opening /proc/1/cgroup raises
    monkeypatch.setattr(os.path, "exists", lambda p: False)
    monkeypatch.setattr(
        builtins, "open", lambda *args, **kw: (_ for _ in ()).throw(FileNotFoundError())
    )
    importlib.reload(config)
    assert config.IS_CONTAINER is False


def test_detect_container_true_via_file(monkeypatch, tmp_path):
    # Simulate /.dockerenv existing
    def fake_exists(path):
        if path == "/.dockerenv":
            return True
        return False

    monkeypatch.setattr(os.path, "exists", fake_exists)
    # cgroup read isn't needed if /.dockerenv is True
    importlib.reload(config)
    assert config.IS_CONTAINER is True


def test_container_id_when_container(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "container")  # simulate container env

    def fake_exists(path):
        return True

    cgroup_content = "\n".join(
        [
            "11:hugetlb:/some/thing",
            "10:cpu:/docker/abcd1234efgh",
        ]
    )

    import io

    monkeypatch.setattr(os.path, "exists", fake_exists)
    monkeypatch.setattr(
        builtins, "open", lambda p, *args, **kw: io.StringIO(cgroup_content)
    )

    importlib.reload(config)
    assert config.IS_CONTAINER is True
    assert config.CONTAINER_ID == "abcd1234efgh"


def test_container_id_when_not_container(monkeypatch):
    # Ensure container ID is "N/A" when not in container
    monkeypatch.setenv("ENVIRONMENT", "local")
    monkeypatch.setattr(os.path, "exists", lambda p: False)
    importlib.reload(config)
    assert config.IS_CONTAINER is False
    assert config.CONTAINER_ID == "N/A"


def test_default_environment(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    importlib.reload(config)
    assert config.ENVIRONMENT == "local"


def test_custom_environment(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "PRODUCTION")
    importlib.reload(config)
    assert config.ENVIRONMENT == "production"


def test_log_level_variants(monkeypatch):
    for lvl_str, lvl_const in [
        ("INFO", logging.INFO),
        ("DEBUG", logging.DEBUG),
        ("bad", logging.INFO),
    ]:
        monkeypatch.setenv("LOG_LEVEL", lvl_str)
        importlib.reload(config)
        assert config.LOG_LEVEL == lvl_const


def test_elasticsearch_host(monkeypatch):
    monkeypatch.delenv("ELASTICSEARCH_HOST", raising=False)
    importlib.reload(config)
    assert config.ELASTICSEARCH_HOST == ""
    monkeypatch.setenv("ELASTICSEARCH_HOST", "http://es.local:9200")
    importlib.reload(config)
    assert config.ELASTICSEARCH_HOST == "http://es.local:9200"


def test_enable_internal_logger(monkeypatch):
    monkeypatch.setenv("ENABLE_INTERNAL_LOGGER", "true")
    importlib.reload(config)
    assert config.ENABLE_INTERNAL_LOGGER
    monkeypatch.setenv("ENABLE_INTERNAL_LOGGER", "false")
    importlib.reload(config)
    assert not config.ENABLE_INTERNAL_LOGGER


def test_logs_dir_default_and_override(monkeypatch, tmp_path):
    monkeypatch.delenv("LOGS_DIR", raising=False)
    monkeypatch.setenv("ENVIRONMENT", "local")
    monkeypatch.chdir(tmp_path)

    # Patch `os.path.exists` to return False for /.dockerenv and /proc/self/cgroup
    monkeypatch.setattr("os.path.exists", lambda p: False)
    # Patch `open` to simulate FileNotFoundError for /proc/1/cgroup
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError()),
    )

    importlib.reload(config)

    # Now this will be based on local env and current working dir
    assert config.LOGS_DIR == str(tmp_path / "logs")

    # Test override
    custom = tmp_path / "mylogs"
    monkeypatch.setenv("LOGS_DIR", str(custom))
    importlib.reload(config)
    assert config.LOGS_DIR == str(custom)


def test_log_file_paths(monkeypatch, tmp_path):
    custom = tmp_path / "logs"
    monkeypatch.setenv("LOGS_DIR", str(custom))
    importlib.reload(config)
    assert config.LOG_FILE_PATH_APP.endswith(os.path.join("logs", "app.log"))
    assert config.LOG_FILE_PATH_INTERNAL.endswith(
        os.path.join("logs", "hestia_logger_internal.log")
    )


def test_log_rotation_defaults(monkeypatch):
    importlib.reload(config)
    assert config.LOG_ROTATION_TYPE == "size"
    assert config.LOG_ROTATION_WHEN == "midnight"
    assert config.LOG_ROTATION_INTERVAL == 1
    assert config.LOG_ROTATION_BACKUP_COUNT == 5
    assert config.LOG_ROTATION_MAX_BYTES == 10 * 1024 * 1024


def test_log_rotation_overrides(monkeypatch):
    monkeypatch.setenv("LOG_ROTATION_TYPE", "time")
    monkeypatch.setenv("LOG_ROTATION_WHEN", "H")
    monkeypatch.setenv("LOG_ROTATION_INTERVAL", "3")
    monkeypatch.setenv("LOG_ROTATION_BACKUP_COUNT", "7")
    monkeypatch.setenv("LOG_ROTATION_MAX_BYTES", str(123456))
    importlib.reload(config)
    assert config.LOG_ROTATION_TYPE == "time"
    assert config.LOG_ROTATION_WHEN == "H"
    assert config.LOG_ROTATION_INTERVAL == 3
    assert config.LOG_ROTATION_BACKUP_COUNT == 7
    assert config.LOG_ROTATION_MAX_BYTES == 123456


def test_hostname_is_string_and_nonempty():
    assert isinstance(config.HOSTNAME, str) and config.HOSTNAME
