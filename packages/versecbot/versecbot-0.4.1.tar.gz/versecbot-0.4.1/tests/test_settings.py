from versecbot.settings import (
    DEFAULT_CONFIG_FILE_PATHS,
    get_config_path,
    DEFAULT_ENV_FILE_PATHS,
    get_env_path,
)


def test_get_container_env(monkeypatch) -> None:
    monkeypatch.setenv("IS_CONTAINER", "true")
    assert get_env_path() == DEFAULT_ENV_FILE_PATHS["container"]


def test_get_local_env(monkeypatch) -> None:
    monkeypatch.delenv("IS_CONTAINER", raising=False)
    assert get_env_path() == DEFAULT_ENV_FILE_PATHS["local"]


def test_get_specified_env(monkeypatch) -> None:
    monkeypatch.setenv("VERSECBOT_ENV_PATH", "/custom/path/.env")
    assert get_env_path() == "/custom/path/.env"


def test_get_container_config(monkeypatch) -> None:
    monkeypatch.setenv("IS_CONTAINER", "true")
    assert get_config_path() == DEFAULT_CONFIG_FILE_PATHS["container"]


def test_get_local_config(monkeypatch) -> None:
    monkeypatch.delenv("IS_CONTAINER", raising=False)
    assert get_config_path() == DEFAULT_CONFIG_FILE_PATHS["local"]


def test_get_specified_config(monkeypatch) -> None:
    monkeypatch.setenv("VERSECBOT_CONFIG_PATH", "/custom/path/config.toml")
    assert get_config_path() == "/custom/path/config.toml"
