"""Configurations.

This module provides classes to represent settings and configurations.
"""

from typing import Any, Dict, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from src.common.constants import CommonPaths
from src.core.utils import FileUtil


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """A simple settings source class that loads variables from a YAML file at the project's root."""

    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        """Get field value from "app_config.yml" file.

        :param field:
        :param field_name:
        :return:
        """
        config_name = "app_config.yml"
        resources_dir_path = CommonPaths.resource_path
        file_path = resources_dir_path.joinpath(config_name)

        file_content_yaml = FileUtil.read_yaml_file(file_path)
        field_value = file_content_yaml.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        """Override prepare_field_value method."""
        return value

    def __call__(self) -> Dict[str, Any]:
        """Override build-in method __call__. To make call class as function."""
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            if field_value is not None:
                d[field_key] = field_value

        return d


class Settings(BaseSettings):
    """Setting class."""

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    host: str
    port: int
    loggerConfiguration: dict

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Settings customise sources. Order of loaded settings."""
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )
