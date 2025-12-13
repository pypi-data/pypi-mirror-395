"""Configuration and settings management"""

import collections
import functools
import json
import os
import pathlib

import yaml
from pydantic import FilePath, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from oocli.data import DataStore, Environment

CONFIG_PATH = pathlib.Path.home() / ".config" / "o-o"
CONFIG_FILE = CONFIG_PATH / "settings.yaml"

DEFAULT_HOST = "https://o-o.tools"


class Config(BaseSettings):
    """o-o configuration

    Config is loaded from both an `.ooconfig` file in the current working
    directory and from `$HOME/.config/o-o/settings.yaml`. Preference is given
    to `.ooconfig`.
    """

    host: str
    sshkey: FilePath
    project: str
    token: str
    datastores: list[DataStore]
    environments: list[Environment]
    sourcecode: bool = False
    nodeprefix: str = "o-"

    model_config = SettingsConfigDict(yaml_file=[CONFIG_FILE, ".ooconfig"])

    @property
    def apiurl(self):
        return f"{self.host}/api/v0"

    @field_validator("environments", "datastores", mode="after")
    @classmethod
    def check_default(cls, values):
        defaults = [value.name for value in values if value.default]
        if len(defaults) > 1:
            raise ValueError(f"{defaults} set as default, only one default permitted")
        return values

    @field_validator("environments", "datastores", mode="after")
    @classmethod
    def check_unique_name(cls, values):
        counter = collections.Counter(v.name for v in values)
        duplicate_names = [name for name, counts in counter.items() if counts > 1]
        if duplicate_names:
            raise ValueError(
                f"name(s) {duplicate_names} used more than once, names must be unique"
            )
        return values

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, YamlConfigSettingsSource(settings_cls))


@functools.cache
def CachedConfig() -> Config:
    """Cached interface to Config"""
    return Config()


def get_value(setting: str, name: str | None):
    """Get a configured setting with given name, if name is None, return the default"""
    configurations = getattr(CachedConfig(), setting)
    if name is None:
        if len(configurations) == 1:
            return next(iter(configurations))
        try:
            return next(c for c in configurations if c.default)
        except StopIteration:
            raise ValueError(
                f"{setting} has no default, must provide one of: "
                f"{[c.name for c in configurations]}"
            ) from None
    try:
        return next(c for c in configurations if c.name == name)
    except StopIteration:
        raise ValueError(
            f"'{name}' is not one of the configured {setting}: "
            f"{[c.name for c in configurations]}"
        ) from None


def write(**kwargs):
    """Write settings to config file location"""
    if CONFIG_FILE.exists():
        kwargs = yaml.safe_load(CONFIG_FILE.read_text()) | kwargs
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(yaml.dump(kwargs))


@functools.cache
def gcp_credentials():
    """Retreive Google Cloud credentials"""
    credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
    if credentials_file is None:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
        )
    credentials_file = pathlib.Path(credentials_file)
    if not credentials_file.exists():
        raise RuntimeError(
            f"Google application credentials file not found ({credentials_file.as_posix()}). "
        )
    return json.loads(credentials_file.read_text())


@functools.cache
def scaleway_credentials():
    """Retreive Scaleway credentials"""
    required_variables = [
        "SCW_ACCESS_KEY",
        "SCW_SECRET_KEY",
        "SCW_DEFAULT_ORGANIZATION_ID",
    ]
    missing_variables = [v for v in required_variables if v not in os.environ]
    if missing_variables:
        raise RuntimeError(
            f"Scaleway environment variables not set: {', '.join(missing_variables)}"
        )

    return {v: os.environ[v] for v in required_variables}
