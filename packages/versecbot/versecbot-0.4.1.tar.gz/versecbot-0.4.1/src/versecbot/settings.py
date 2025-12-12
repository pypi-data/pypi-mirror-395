from os import getenv
from typing import Tuple, Type, Optional
from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from versecbot_interface import PluginSettings


DEFAULT_CONFIG_FILE_PATHS = {"container": "/app/config.toml", "local": "./config.toml"}
DEFAULT_ENV_FILE_PATHS = {"container": "/app/.env", "local": "./.env"}


def get_config_path() -> str:
    if specified_path := getenv("VERSECBOT_CONFIG_PATH", None):
        return specified_path

    deploy_env = "container" if getenv("IS_CONTAINER", False) else "local"
    return DEFAULT_CONFIG_FILE_PATHS[deploy_env]


def get_env_path() -> str:
    if specified_path := getenv("VERSECBOT_ENV_PATH", None):
        return specified_path

    deploy_env = "container" if getenv("IS_CONTAINER", False) else "local"
    return DEFAULT_ENV_FILE_PATHS[deploy_env]


@lru_cache()
def get_settings() -> "Settings":
    return Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_path(),
        env_file_encoding="utf-8",
        env_prefix="versecbot_",
        extra="ignore",
        toml_file=get_config_path(),
    )

    api_token: str
    plugins: Optional[dict[str, PluginSettings]]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )
