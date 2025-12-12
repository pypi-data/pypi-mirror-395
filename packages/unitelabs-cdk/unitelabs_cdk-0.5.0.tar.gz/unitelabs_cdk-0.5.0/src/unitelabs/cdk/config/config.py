import dataclasses
import functools
import json
import pathlib

import pydantic
import pydantic_core
import typing_extensions as typing
from pydantic import Field, model_validator
from pydantic import field_validator as validate_field
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from ruamel.yaml import YAML, CommentedMap

validate_config = functools.partial(model_validator, mode="after")


BasicSerializableType: typing.TypeAlias = typing.Union[str, int, float, bool]
SerializableType: typing.TypeAlias = typing.Union[
    BasicSerializableType,
    None,
    list["SerializableType"],
    dict[str, "SerializableType"],
]
SerializableDict: typing.TypeAlias = dict[str, SerializableType]
DEFAULT_CONFIG_PATHS = [pathlib.Path("./config.json"), pathlib.Path("./config.yaml"), pathlib.Path("./config.yml")]


class UnsupportedConfigFiletype(Exception):
    """The filetype is unsupported for reading/writing config files."""


class ConfigurationError(ValueError):
    """Received an invalid configuration."""


def get_schema_fields(data: pydantic_core.core_schema.CoreSchema) -> list[SerializableDict]:
    """Get the fields from a pydantic core schema."""
    schema = data.get("schema", {})
    if (fields := schema.get("fields")) and isinstance(fields[0], dict):
        return fields
    return get_schema_fields(schema.get("schema", {})) if schema else []


class JsonSchemaGenerator(GenerateJsonSchema):
    """
    Custom JSON Schema generator for compliance with UniteLabs PEP-17: JSON Schema.

    More info about the specification can be found at: https://www.notion.so/unitelabs/JSON-Schema-13403b686b5f8099910cf52b9e1510b5
    """

    def generate(self, schema: pydantic_core.core_schema.CoreSchema, mode: str = "validation") -> JsonSchemaValue:
        json_schema = super().generate(schema, mode)
        json_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        return json_schema

    def bytes_schema(self, schema: pydantic_core.core_schema.BytesSchema) -> JsonSchemaValue:
        byte_schema = super().bytes_schema(schema)
        byte_schema["contentEncoding"] = "base64"
        return byte_schema


def update_yaml(yaml: CommentedMap, data: dict) -> None:
    """
    Recursively update a `ruamel.yaml.CommentedMap` with data from a dictionary.

    Args:
      yaml: The `CommentedMap` to update.
      data: A dictionary with keys matching those contained in `yaml` from which updated values
       will be applied to the `CommentedMap`.
    """
    for key, value in data.items():
        if key not in yaml:
            continue

        if isinstance(value, dict):
            update_yaml(yaml[key], value)
        else:
            current = yaml[key]
            if current != value:
                yaml[key] = value


class MissingDefault:
    def __repr__(self):
        return "MissingDefault"


UNCONFIGURED = MissingDefault()
T = typing.TypeVar("T")


class DelayedDefault(typing.Generic[T]):
    def __init__(self, func: typing.Callable[["Config"], T]):
        self.func = func
        self.resolved = False
        self.value = typing.cast(T, UNCONFIGURED)

    def resolve(self, instance: "Config") -> T:
        if not self.resolved:
            self.value = self.func(instance)
            self.resolved = True
        return self.value


def delayed_default(func: typing.Callable[["Config"], T]) -> typing.Callable[[], T]:
    def factory() -> T:
        return typing.cast(T, DelayedDefault(func))

    return factory


class Config:
    """A pydantic-enabled dataclass that represents a configuration."""

    __pydantic_config__ = pydantic.ConfigDict(
        validate_assignment=True,
        revalidate_instances="always",
        use_attribute_docstrings=True,
        ser_json_bytes="base64",
        val_json_bytes="base64",
    )
    _ignore: typing.ClassVar[set[str]] = {"_source", "_source_path"}
    _source: typing.Union[CommentedMap, SerializableDict, None] = None
    _source_path: typing.Optional[pathlib.Path] = None

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: typing.Self, handler: pydantic.GetCoreSchemaHandler
    ) -> pydantic_core.core_schema.CoreSchema:
        derived_class = handler(cls)

        base = [c for c in cls.__mro__ if dataclasses.is_dataclass(c) and c not in (cls, Config)]

        if not base or len(base) != 1 or len(dataclasses.fields(base[0])) < 1:
            return derived_class

        base_class = handler(base[0])

        base_fields_by_name = {field["name"]: field for field in get_schema_fields(base_class)}

        for derived_field in get_schema_fields(derived_class):
            base_field = base_fields_by_name.get(derived_field["name"], {})
            if not derived_field.get("metadata") and (update := base_field.get("metadata")):
                derived_field["metadata"] = update

        return derived_class

    def __getattribute__(self, name: str):
        value = super().__getattribute__(name)

        if isinstance(value, DelayedDefault):
            try:
                return value.resolve(self)
            except RecursionError:
                msg = (
                    f"The delayed_default value for {self.__class__.__name__}.{name} could not be resolved. "
                    "This is most likely due to a circular dependency between delayed_default values."
                )
                raise ConfigurationError(msg) from None
        return value

    @classmethod
    def to_pydantic_dataclass(cls) -> type[typing.Self]:
        """Create a pydantic dataclass from the Config."""
        subclass = type(cls.__name__, (cls,), {})
        return pydantic.dataclasses.dataclass(subclass)

    @classmethod
    def get_type_adapter(cls) -> pydantic.TypeAdapter:
        """Get a pydantic type adapter for this class."""
        return pydantic.TypeAdapter(cls)

    @classmethod
    def from_dict(cls, data: SerializableDict) -> typing.Self:
        """
        Create a new `Config` instance from a dict, without rejecting unknown fields.

        This function allows arbitrary additional data to be set on the `Config` object
        and therefore does not guarantee validations on setting attributes for all fields, unlike `validate`.

        In this way, this method should only be used in contexts where the derived configuration is not present,
        e.g. `certificate` CLI where app is not loaded and thus the subclass of `ConnectorBaseConfig` cannot be found.

        Args:
          data: A dictionary of configuration values.

        Returns:
          A validated `Config` instance, where only the known fields have been validated.
        """
        fields = [field.name for field in dataclasses.fields(cls)]
        known_fields = {k: v for k, v in data.items() if k in fields}
        unknown_fields = {k: v for k, v in data.items() if k not in known_fields}

        cls.validate(known_fields)

        final = cls(**known_fields)
        for k, v in unknown_fields.items():
            setattr(final, k, v)

        final._source = data

        return final

    def to_dict(self) -> SerializableDict:
        """Get the serializable dictionary representation of the instance."""
        data = json.loads(self.get_type_adapter().dump_json(self))
        if len(dataclasses.fields(self)) < len(self.__dict__.keys()):
            # enables dump when a config has been loaded from_dict
            known_fields = [f.name for f in dataclasses.fields(self)]
            additional_data = {k: v for k, v in self.__dict__.items() if k not in [*known_fields, *self._ignore]}
            for key, value in additional_data.items():
                data[key] = value
        return data

    @classmethod
    def schema(cls) -> dict[str, typing.Any]:
        """Get the JSON Schema for this class."""
        return cls.get_type_adapter().json_schema(schema_generator=JsonSchemaGenerator)

    @classmethod
    def describe(cls, field: typing.Optional[str] = None) -> dict[str, typing.Any]:
        """
        Get a description of the whole configuration or for a field in the configuration.

        Currently only supports fields that are present in the schema at depth 1.

        Args:
          field: The field in the `Config` to get a description for.

        Raises:
          InvalidSchemaFieldError: If the provided `field` is not present in the schema.
        """
        from .schema import InvalidSchemaFieldError, Schema, describe

        schema = Schema(cls.schema())
        description = describe(cls, schema)
        if field is None:
            return description

        if field not in description:
            msg = f"'{field}' is not a valid field in {cls.__name__}."
            raise InvalidSchemaFieldError(msg)
        return description[field].get("values", description[field])

    @classmethod
    def load(cls, path: typing.Optional[pathlib.Path] = None, strict: bool = False) -> typing.Self:
        """
        Load a connector configuration from `path`.

        If no `path` is provided, searches the default config file locations: `./config.json`, `./config.yaml`,
        and `./config.yml` for an existing config file.

        Args:
          path: The path to the configuration file, can be a yaml or json filetype,
            defaults to first found config file in default locations.
          strict: Whether or not to raise an error if the file contains fields not defined in the `Config` dataclass.

        Returns:
          A `Config` instance, where only the known fields have been validated if not `strict`,
            or all fields have been validated if `strict`.

        Raises:
          FileNotFoundError: If no config file is found at the provided `path`.
          UnsupportedConfigFiletype: If the provided `path` is not a yaml or json file.
          ConfigurationError: If the config file contains invalid values.
        """
        path = find_file(path, default_paths=DEFAULT_CONFIG_PATHS)  # call find_file explicitly to resolve source path
        data = read_config_file(path)

        inst: typing.Self
        inst = cls.validate(data) if strict else cls.from_dict(data)
        inst._source = data
        inst._source_path = path

        return inst

    def dump(self, path: pathlib.Path) -> None:
        """
        Write the current configuration to a file.

        Args:
          path: The path at which to write the configuration, may be yaml or json filetype.

        Raises:
          UnsupportedConfigFiletype: If `path` extension is not `.yaml` or `.json`.
        """
        data = self.to_dict()

        if path.suffix == ".json":
            data = json.dumps(data, indent=2)
            with path.open("w") as f:
                f.write(data)
            return
        if path.suffix in [".yaml", ".yml"]:
            yaml = YAML()
            if hasattr(self, "_source_path") and self._source_path and self._source_path.exists():
                # preserve width of source file
                yaml.width = max(map(len, self._source_path.read_text().splitlines()))
            with path.open("w") as f:
                if hasattr(self, "_source") and isinstance(self._source, CommentedMap):
                    update_yaml(self._source, data)
                    data = self._source
                yaml.dump(data, f)

            return
        msg = f"Cannot write file to {path}. Only yaml and json filetypes are supported."
        raise UnsupportedConfigFiletype(msg)

    @classmethod
    def validate(cls, values: typing.Optional[SerializableDict]) -> typing.Self:
        """
        Validate the configuration values.

        Args:
          values: The configuration values to validate.

        Returns:
          A validated `Config` instance, or the default instance if no values are provided.
        """

        values = values if values is not None else {}

        if unknown_fields := [k for k in values if k not in [f.name for f in dataclasses.fields(cls)]]:
            msg = f"Provided field or fields {unknown_fields} are not valid for {cls.__name__} configuration."
            raise ConfigurationError(msg)

        try:
            configuration = cls.to_pydantic_dataclass()(**values)
        except pydantic.ValidationError as e:
            msg = f"Invalid configuration for {cls.__name__}: {e}"
            raise ConfigurationError(msg) from None

        return configuration


def read_config_file(path: typing.Optional[pathlib.Path] = None) -> SerializableDict:
    """
    Read in configuration data from a file.

    Args:
      path: The path to the configuration file, can be a yaml or json file,
        default checks `./config.json`, `./config.yaml`, `./config.yml` paths.

    Returns:
      A serializable dictionary of the configuration data.

    Raises:
      FileNotFoundError: If no file is found at the provided `path`.
      UnsupportedConfigFiletype: If the provided `path` is not a yaml or json file.
    """

    data = {}
    path = find_file(path, default_paths=DEFAULT_CONFIG_PATHS)

    if path.suffix == ".json":
        data = json.loads(path.read_text())
    elif path.suffix in (".yaml", ".yml"):
        yaml = YAML()
        data = yaml.load(path)
    else:
        msg = f"Cannot read file at '{path}'. Only yaml and json filetypes are supported."
        raise UnsupportedConfigFiletype(msg)

    return data


def find_file(
    path: typing.Optional[pathlib.Path] = None,
    default_paths: typing.Optional[list[pathlib.Path]] = None,
) -> pathlib.Path:
    """
    Search for a file at the provided path or in default locations.

    Args:
      path: The path to the file, can be a yaml or json file.
      default_paths: A list of default paths to search if no `path` is provided.

    Returns:
      The absolute path to the file.

    Raises:
      FileNotFoundError: If no file is found at the provided `path` or any of the `default_paths`.
    """

    if path is None:
        default_paths = default_paths or []
        path = get_extant_path(default_paths)
        if not path:
            resolved_paths = [p.resolve() for p in default_paths]
            msg = (
                f"No config was provided and none was found at any of the default paths: {resolved_paths}. "
                "Use the `config create` CLI to create a new configuration file."
            )
            raise FileNotFoundError(msg)

    path = path.resolve()
    if not path.exists():
        msg = f"File at path '{path}' not found."
        raise FileNotFoundError(msg)

    return path


def get_extant_path(paths: list[pathlib.Path]) -> typing.Optional[pathlib.Path]:
    """
    Search for an existing file from a list of paths.

    Args:
      paths: A list of paths, ordered by preference.

    Returns:
      The first absolute path from `paths` that exists or None, if none of the paths exist.
    """
    return next((path.resolve(strict=True) for path in paths if path.resolve().exists()), None)


__all__ = ["Config", "ConfigurationError", "Field", "UnsupportedConfigFiletype", "validate_config", "validate_field"]
