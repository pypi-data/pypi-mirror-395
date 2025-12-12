import dataclasses
import json
import pathlib
import re
import unittest.mock

import pydantic
import pytest
import typing_extensions as typing
from ruamel.yaml import YAML

from unitelabs.cdk.config import (
    Config,
    ConfigurationError,
    ConnectorBaseConfig,
    Field,
    InvalidSchemaFieldError,
    UnsupportedConfigFiletype,
    delayed_default,
    read_config_file,
    validate_config,
    validate_field,
)


class TestGetPydanticCoreSchema:
    def test_should_merge_base_class_descriptions(self):
        @dataclasses.dataclass
        class BaseConfig(Config):
            static: str = "DEFAULT"
            """Static string."""
            modified: int = 0
            """The old value."""

        BASE_CONFIG_SCHEMA = {
            "type": "object",
            "title": "BaseConfig",
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "properties": {
                "modified": {
                    "type": "integer",
                    "default": 0,
                    "title": "Modified",
                    "description": "The old value.",
                },
                "static": {
                    "type": "string",
                    "default": "DEFAULT",
                    "title": "Static",
                    "description": "Static string.",
                },
            },
        }

        assert BaseConfig.schema() == BASE_CONFIG_SCHEMA

        @dataclasses.dataclass
        class DerivedConfig(BaseConfig):
            modified: int = 100
            """The new value."""

        derived_schema = BASE_CONFIG_SCHEMA.copy()
        derived_schema["title"] = "DerivedConfig"
        derived_schema["properties"]["modified"]["default"] = 100
        derived_schema["properties"]["modified"]["description"] = "The new value."
        assert DerivedConfig.schema() == derived_schema


class TestToPydanticDataclass:
    def test_should_not_alter_class(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        pydantic_dataclass = ExampleConfig.to_pydantic_dataclass()
        assert pydantic.dataclasses.is_pydantic_dataclass(pydantic_dataclass)
        assert not pydantic.dataclasses.is_pydantic_dataclass(ExampleConfig)

    def test_returned_pydantic_dataclass_creates_instances_of_class(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        pydantic_dataclass = ExampleConfig.to_pydantic_dataclass()
        instance = pydantic_dataclass()
        assert isinstance(instance, ExampleConfig)


class TestDelayedDefault:
    def test_should_call_set_value(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = dataclasses.field(default_factory=delayed_default(lambda self: 1))

        example = ExampleConfig()
        assert example.value == 1

    def test_should_allow_use_of_other_fields(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0
            derived_value: int = dataclasses.field(default_factory=delayed_default(lambda self: self.value + 1))

        example = ExampleConfig()
        assert example.value == 0
        assert example.derived_value == 1

    def test_should_call_method(self):
        method = unittest.mock.Mock()
        method.return_value = 1

        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0
            derived_value: int = dataclasses.field(default_factory=delayed_default(lambda self: method(self)))

        example = ExampleConfig()
        assert example.value == 0
        assert example.derived_value == 1
        method.assert_called_once_with(example)

    @pytest.mark.parametrize(
        "entrypoint,expand",
        [
            pytest.param("validate", False, id="validate"),
            pytest.param("from_dict", False, id="from_dict"),
            pytest.param("cls", True, id="from constructor"),
        ],
    )
    def test_should_allow_override(self, entrypoint, expand):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            type: typing.Literal["a", "b"] = "a"
            value: str = dataclasses.field(default_factory=delayed_default(lambda self: f"{self.type} value"))

        test_method = ExampleConfig if entrypoint == "cls" else getattr(ExampleConfig, entrypoint)

        # Test default value
        config = test_method(type="b") if expand else test_method({"type": "b"})
        assert config.type == "b"
        assert config.value == "b value"

        # Test custom override
        custom_value = "custom value"
        config = (
            test_method(type="a", value=custom_value) if expand else test_method({"type": "a", "value": custom_value})
        )
        assert config.type == "a"
        assert config.value == custom_value

    def test_should_allow_partial_override(self):
        @dataclasses.dataclass
        class NestedConfig(Config):
            type: typing.Literal["A", "B"] = "A"
            name: str = dataclasses.field(default_factory=delayed_default(lambda self: f"{self.type} name"))

        @dataclasses.dataclass
        class MyConfig(Config):
            nested: NestedConfig = dataclasses.field(default_factory=NestedConfig)
            nested_name: str = dataclasses.field(default_factory=delayed_default(lambda self: self.nested.name))

        config = MyConfig.validate({})
        assert config.nested.type == "A"
        assert config.nested_name == config.nested.name

        config = MyConfig.validate({"nested_name": "custom name"})
        assert config.nested.type == "A"
        assert config.nested.name == "A name"
        assert config.nested_name == "custom name"

        config = MyConfig.validate({"nested": {"type": "B"}})
        assert config.nested.type == "B"
        assert config.nested.name == config.nested_name == "B name"

    def test_should_catch_circular_usages(self):
        @dataclasses.dataclass
        class AConfig(Config):
            type: typing.Literal["A1", "A2"] = dataclasses.field(
                default_factory=delayed_default(lambda self: "A1" if "A" in self.name else "A2")
            )
            name: str = dataclasses.field(default_factory=delayed_default(lambda self: f"{self.type} name"))

        a = AConfig()
        match = (
            r"The delayed_default value for AConfig.(type|name) could not be resolved. "
            "This is most likely due to a circular dependency between delayed_default values."
        )  # does not consistently resolve to type or name
        with pytest.raises(ConfigurationError, match=match):
            a.type

        with pytest.raises(ConfigurationError, match=match):
            a.name


class TestFromDict:
    def test_should_allow_partial_set(self):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            a: int = 0
            b: int = 1

        config = ExampleConfig.from_dict({"a": 10})
        assert config
        assert config.a == 10
        assert config.b == 1

    def test_should_raise_ConfigurationError_on_invalid_field(self):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            value: int = 0

        with pytest.raises(
            ConfigurationError,
            match="Invalid configuration for ExampleConfig: 1 validation error for ExampleConfig"
            "\nvalue"
            "\n  Input should be a valid integer",
        ):
            ExampleConfig.from_dict({"value": "not an int"})

    def test_should_allow_arbitrary_fields(self):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            value: int = 0

        config = ExampleConfig.from_dict({"value": 0, "arbitrary_field": True})
        assert config
        assert config.value == 0
        assert config.arbitrary_field

    def test_should_not_raise_ConfigurationError_on_invalid_field_set(self):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            value: int = 0

        example = ExampleConfig.from_dict({"value": 0})
        example.value = "not an int"

        assert example.value == "not an int"

    def test_should_set_source(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config = ExampleConfig.from_dict({"value": 0})
        assert config._source == {"value": 0}
        assert config._source_path is None


class TestToDict:
    def test_should_return_dict(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        default = ExampleConfig().to_dict()
        assert isinstance(default, dict)
        assert default == {"value": 0}

    def test_should_allow_arbitrary_fields(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config = ExampleConfig.from_dict({"value": 0, "arbitrary_field": True})
        data = config.to_dict()
        assert isinstance(data, dict)
        assert data == {"value": 0, "arbitrary_field": True}


class TestDefault:
    def test_should_return_dict(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        default = ExampleConfig().to_dict()
        assert isinstance(default, dict)
        assert default == {"value": 0}

    def test_added_keys_included(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            a: int = 0
            b: float = 0.0
            c: str = ""
            d: bool = True
            e: list[str] = dataclasses.field(default_factory=list)
            f: dict[str, int] = dataclasses.field(default_factory=dict)

        assert ExampleConfig().to_dict() == {"a": 0, "b": 0.0, "c": "", "d": True, "e": [], "f": {}}


class TestDescribe:
    def test_should_return_dict(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0
            """The value."""

        default = ExampleConfig().describe()
        assert isinstance(default, dict)
        assert default == {"value": {"type": "int", "default": "0", "description": "The value."}}

    def test_should_return_dict_for_nested_field(self):
        @dataclasses.dataclass
        class NestedConfig(Config):
            value: int = 0
            """The value."""

        @dataclasses.dataclass
        class ExampleConfig(Config):
            nested: NestedConfig = dataclasses.field(default_factory=NestedConfig)
            """The nested config."""

        default = ExampleConfig().describe()
        assert isinstance(default, dict)
        FULL_DATA = {
            "nested": {
                "values": {"value": {"type": "int", "default": "0", "description": "The value."}},
                "description": "For more information use `config show --output nested`.",
                "type": "NestedConfig",
                "default": "",
            }
        }
        assert default == FULL_DATA
        assert ExampleConfig().describe("nested") == FULL_DATA["nested"]["values"]

    def test_should_raise_invalid_schema_field_error(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        with pytest.raises(
            InvalidSchemaFieldError,
            match="'non_existent_field' is not a valid field in ExampleConfig.",
        ):
            ExampleConfig.describe("non_existent_field")


class TestLoad:
    @pytest.mark.parametrize("ext", ["toml", "ini"])
    def test_should_raise_unsupported_filetype(self, tmp_path, ext):
        config_file_path = tmp_path / f"config.{ext}"
        config_file_path.touch()
        with pytest.raises(
            UnsupportedConfigFiletype,
            match=f"Cannot read file at '{config_file_path.resolve()}'. Only yaml and json filetypes are supported.",
        ):
            ConnectorBaseConfig.load(config_file_path)

    @pytest.mark.parametrize("ext", ["json", "yaml"])
    def test_should_set_source_and_source_path(self, tmp_path, ext):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config_path = tmp_path / f"config.{ext}"
        config = ExampleConfig().dump(config_path)

        config = ExampleConfig.load(config_path)
        assert config._source == {"value": 0}
        assert config._source_path == config_path


class TestDump:
    def test_should_dump_to_json(self, tmp_path):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config = ExampleConfig()
        config_path = tmp_path / "config.json"
        config.dump(config_path)

        with config_path.open("r") as f:
            data = json.load(f)

        assert data == {"value": 0}

    def test_should_dump_to_yaml(self, tmp_path):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config = ExampleConfig()
        config_path = tmp_path / "config.yaml"
        config.dump(config_path)

        yaml = YAML(typ="safe")
        with config_path.open("r") as f:
            data = yaml.load(f)

        assert data == {"value": 0}

    def test_should_preserve_yaml_comments(self, tmp_path):
        sample_yaml = """# before comment\nvalue: 0 # comment\n"""

        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        in_config_path = tmp_path / "config.yaml"

        with in_config_path.open("w") as f:
            f.write(sample_yaml)

        config = ExampleConfig.load(in_config_path)
        assert config.value == 0

        out_config_path = tmp_path / "out_config.yaml"
        config.dump(out_config_path)

        with out_config_path.open("r") as f:
            data = f.read()
            assert data == sample_yaml

    def test_should_allow_arbitrary_fields(self, tmp_path):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config = ExampleConfig.from_dict({"value": 0, "arbitrary_field": True})
        config_path = tmp_path / "config.json"
        config.dump(config_path)

        with config_path.open("r") as f:
            data = json.load(f)

        assert data == {"value": 0, "arbitrary_field": True}


class TestFieldValidation_Basic:
    def test_should_format_configuration_errors_raised_in_post_init(self):
        msg = "value must be greater than 1."

        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

            def __post_init__(self):
                if not self.value > 1:
                    raise ConfigurationError(msg)

        with pytest.raises(
            ConfigurationError,
            match=(
                f"Invalid configuration for ExampleConfig: 1 validation error for ExampleConfig\n  Value error, {msg}"
            ),
        ):
            ExampleConfig.validate({"value": 0})

    def test_should_not_raise_ValidationError_from_post_init_validation_on_field_set(self):
        msg = "value must be greater than 1."

        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

            def __post_init__(self):
                if not self.value > 0:
                    raise ConfigurationError(msg)

        config = ExampleConfig.validate({"value": 2})
        assert config.value == 2

        config.value = 0

    def test_should_validate_types(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        with pytest.raises(
            ConfigurationError,
            match="Invalid configuration for ExampleConfig: "
            "1 validation error for ExampleConfig\n"
            "value\n  "
            "Input should be a valid integer, unable to parse string as an integer",
        ):
            ExampleConfig.validate({"value": "string"})

    def test_should_raise_ValidationError_for_invalid_type_on_field_set(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: int = 0

        config = ExampleConfig.validate({"value": 2})
        assert config.value == 2

        with pytest.raises(
            pydantic.ValidationError,
            match="1 validation error for ExampleConfig\nvalue\n  Input should be a valid integer",
        ):
            config.value = "string"

    def test_should_raise_for_invalid_field_name(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            value: bool = False

        with pytest.raises(
            ConfigurationError,
            match=re.escape(
                "Provided field or fields ['invalid_field'] are not valid for ExampleConfig configuration."
            ),
        ):
            ExampleConfig.validate({"invalid_field": True, "value": True})


class TestFieldValidation_FieldAnnotation:
    def test_should_validate_with_field_annotation(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            large_int: typing.Annotated[int, Field(gt=9000)] = 9001

        default = ExampleConfig().to_dict()
        assert ExampleConfig.validate(default)

        default.update({"large_int": 29})
        with pytest.raises(
            ConfigurationError,
            match="Invalid configuration for ExampleConfig: 1 validation error for ExampleConfig"
            "\nlarge_int"
            "\n  Input should be greater than 9000",
        ):
            ExampleConfig.validate(default)

    def test_should_raise_ValidationError_on_invalid_field_set(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            large_int: typing.Annotated[int, Field(gt=9000)] = 9001

        config = ExampleConfig.validate({"large_int": 9500})
        assert config.large_int == 9500

        with pytest.raises(
            pydantic.ValidationError,
            match="1 validation error for ExampleConfig\nlarge_int\n  Input should be greater than 9000",
        ):
            config.large_int = 29


class TestFieldValidation_ValidateFieldDecorator:
    def test_should_validate_with_field_decorator(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            simple: bool = False

            @validate_field("simple")
            @classmethod
            def must_be_true(cls, value: bool) -> bool:
                if not value:
                    msg = "simple must be True."
                    raise ConfigurationError(msg)
                return value

        default = ExampleConfig().to_dict()
        with pytest.raises(
            ConfigurationError,
            match="Invalid configuration for ExampleConfig: 1 validation error for ExampleConfig"
            "\nsimple"
            "\n  Value error, simple must be True.",
        ):
            ExampleConfig.validate(default)

        default.update({"simple": True})
        example = ExampleConfig.validate(default)
        assert example.simple

    def test_should_raise_ValidationError_on_invalid_field_set(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            simple: bool = False

            @validate_field("simple")
            @classmethod
            def must_be_true(cls, value: bool) -> bool:
                if not value:
                    msg = "simple must be True."
                    raise ConfigurationError(msg)
                return value

        example = ExampleConfig.validate({"simple": True})
        with pytest.raises(pydantic.ValidationError):
            example.simple = False


class TestConfigValidation_ValidateConfigDecorator:
    def test_should_validate_with_validate_config_decorator(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            complex: bool = False
            """Whether or not the complex configuration is enabled."""
            complex_name: typing.Optional[str] = ""
            """The name of the complex configuration."""

            @validate_config()
            def must_be_named(self) -> typing.Self:
                if self.complex and not self.complex_name:
                    msg = "complex configuration requires additional 'complex_name' value."
                    raise ConfigurationError(msg)
                return self

        default = ExampleConfig().to_dict()
        config = ExampleConfig.validate(default)

        assert hasattr(config, "complex")
        assert hasattr(config, "complex_name")

        with pytest.raises(
            ConfigurationError,
            match="Invalid configuration for ExampleConfig: 1 validation error for ExampleConfig"
            "\n  Value error, complex configuration requires additional 'complex_name' value.",
        ):
            default.update({"complex": True})
            ExampleConfig.validate(default)

    def test_should_validate_with_mulitiple_validate_config_decorators(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            complex: bool = False
            complex_name: typing.Optional[str] = ""

            @validate_config()
            def must_be_named(self) -> typing.Self:
                if self.complex and not self.complex_name:
                    msg = "complex configuration requires additional 'complex_name' value."
                    raise ConfigurationError(msg)
                return self

            @validate_config()
            def must_contain_substring(self) -> typing.Self:
                if (self.complex and self.complex_name) and not self.complex_name.startswith("A"):
                    msg = "'complex_name' must start with 'A'."
                    raise ConfigurationError(msg)
                return self

        default = ExampleConfig().to_dict()
        config = ExampleConfig.validate(default)

        assert hasattr(config, "complex")
        assert hasattr(config, "complex_name")

        with pytest.raises(
            ConfigurationError,
            match="Invalid configuration for ExampleConfig: 1 validation error for ExampleConfig"
            "\n  Value error, 'complex_name' must start with 'A'.",
        ):
            default.update({"complex": True, "complex_name": "this"})
            ExampleConfig.validate(default)

    def test_should_raise_ValidationError_on_invalid_field_set(self):
        @dataclasses.dataclass
        class ExampleConfig(Config):
            complex: bool = False
            complex_name: typing.Optional[str] = ""

            @validate_config()
            def must_be_named(self) -> typing.Self:
                if self.complex and not self.complex_name:
                    msg = "complex configuration requires additional 'complex_name' value."
                    raise ConfigurationError(msg)
                return self

        config = ExampleConfig.validate({"complex": False, "complex_name": ""})
        with pytest.raises(
            pydantic.ValidationError,
            match="1 validation error for ExampleConfig\n  Value error, complex configuration requires additional 'complex_name' value.",
        ):
            config.complex = True


class TestReadConfigFile:
    def test_should_raise_if_default_not_found(self):
        with pytest.raises(
            FileNotFoundError, match="No config was provided and none was found at any of the default paths:"
        ):
            read_config_file()

    def test_should_raise_if_file_not_found(self):
        path = pathlib.Path("config.json")
        with pytest.raises(FileNotFoundError, match=f"File at path '{path.resolve()}' not found."):
            read_config_file(path)

    @pytest.mark.parametrize("ext", ["json", "yaml"])
    def test_should_read_all_data(self, tmp_path, ext):
        config_path = tmp_path / f"config.{ext}"

        @dataclasses.dataclass
        class ExampleConfig(Config):
            name: typing.Annotated[str, Field(min_length=1)] = "Default"
            """The name of the example."""
            must_be_set: typing.Annotated[int, Field(ge=0, le=10)] = -1
            """A value with an invalid default."""

        config = ExampleConfig(name="Example", must_be_set=1)
        config.dump(config_path)

        reloaded = read_config_file(config_path)
        assert reloaded == config.to_dict()
