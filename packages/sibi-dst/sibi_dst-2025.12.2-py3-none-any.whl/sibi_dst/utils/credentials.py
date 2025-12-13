from typing import Dict, Any, List, Optional, Type, cast
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DynamicConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")


class ConfigManager:
    def __init__(self):
        self._models: Dict[str, Type[BaseSettings]] = {}
        self._instances: Dict[str, BaseSettings] = {}

    def _build_model_class(
        self,
        name: str,
        prefix: str,
        fields: Dict[str, Field],
    ) -> Type[BaseSettings]:

        namespace: Dict[str, Any] = {
            "model_config": SettingsConfigDict(
                env_prefix=f"{prefix}_",
                extra="ignore",
            )
        }

        annotations: Dict[str, Any] = {}

        for field_name, field_def in fields.items():
            annotations[field_name] = Any
            namespace[field_name] = field_def

        namespace["__annotations__"] = annotations

        model_cls = type(name, (DynamicConfig,), namespace)

        return cast(Type[BaseSettings], model_cls)

    def add_config(
        self,
        name: str,
        prefix: str,
        keys: List[str],
        defaults: Optional[Dict[str, Any]] = None,
    ) -> None:

        defaults = defaults or {}
        model_fields = {}

        for key in keys:
            lower = key.lower()
            default = defaults.get(lower, None)
            model_fields[lower] = Field(default=default)

        model_cls = self._build_model_class(
            name=name.capitalize() + "Settings",
            prefix=prefix,
            fields=model_fields,
        )

        self._models[name] = model_cls
        self._instances[name] = model_cls()

    def get_config(self, name: str) -> Dict[str, Any]:
        inst = self._instances.get(name)
        return inst.model_dump() if inst else {}

    def reload(self, name: Optional[str] = None) -> None:
        if name:
            cls = self._models.get(name)
            if cls:
                self._instances[name] = cls()
        else:
            for name, cls in self._models.items():
                self._instances[name] = cls()

# import os
#
#
# class ConfigLoader:
#     def __init__(self, prefix, keys, defaults=None):
#         """
#         Initialize a ConfigLoader instance.
#
#         :param prefix: The prefix for the environment variables.
#         :param keys: A list of keys to extract.
#         :param defaults: A dictionary of default values if environment variables are not set.
#         """
#         self.prefix = prefix
#         self.keys = keys
#         self.defaults = defaults or {}
#
#     def load(self):
#         """
#         Load the configuration from environment variables.
#
#         :return: A dictionary of configuration values.
#         """
#         config = {}
#         for key in self.keys:
#             env_var = f"{self.prefix}_{key}"
#             config[key.lower()] = os.environ.get(env_var, self.defaults.get(key.lower(), ''))
#         return config
#
#
# class ConfigManager:
#     """
#     A class to manage and load multiple configurations.
#     """
#
#     def __init__(self):
#         self.configurations = {}
#
#     def add_config(self, name, prefix, keys, defaults=None):
#         """
#         Add a configuration to the manager.
#
#         :param name: The name of the configuration.
#         :param prefix: The prefix for the environment variables.
#         :param keys: A list of keys to extract.
#         :param defaults: A dictionary of default values if environment variables are not set.
#         """
#         loader = ConfigLoader(prefix, keys, defaults)
#         self.configurations[name] = loader.load()
#
#     def get_config(self, name):
#         """
#         Get a specific configuration by name.
#
#         :param name: The name of the configuration.
#         :return: The configuration dictionary.
#         """
#         return self.configurations.get(name, {})
