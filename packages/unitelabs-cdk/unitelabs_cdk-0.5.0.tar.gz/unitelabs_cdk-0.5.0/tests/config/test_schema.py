import dataclasses
import typing

import pytest

from unitelabs.cdk.config import Config
from unitelabs.cdk.config.schema import InvalidSchemaFieldError, Schema, describe, get_type_str


@dataclasses.dataclass
class NestedRef(Config):
    test_ref_value: str = "REF_VALUE"
    """A nested property."""


@dataclasses.dataclass
class DescribableConfig(Config):
    test_ref_a: NestedRef = dataclasses.field(default_factory=NestedRef)
    test_ref_b: typing.Optional[NestedRef] = dataclasses.field(default_factory=NestedRef)
    """A nested config object."""
    test_property: str = "PROPERTY_VALUE"
    """A string property."""


TEST_SCHEMA = {
    "properties": {
        "test_ref_a": {"$ref": "#/$defs/NestedRef"},
        "test_ref_b": {"anyOf": [{"$ref": "#/$defs/NestedRef"}, {"type": "null"}]},
        "test_property": {
            "type": "string",
            "default": "PROPERTY_VALUE",
            "title": "Test Property",
            "description": "A string property.",
        },
    },
    "$defs": {
        "NestedRef": {
            "properties": {
                "test_ref_value": {
                    "type": "string",
                    "default": "REF_VALUE",
                    "title": "Test Ref Value",
                    "description": "A nested property.",
                }
            },
            "type": "object",
            "title": "NestedRef",
        },
    },
    "type": "object",
    "title": "DescribableConfig",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
}


class TestGet:
    @pytest.mark.parametrize("reference", ["test_ref_a", "test_ref_b"])
    def test_should_get_valid_reference(self, reference):
        schema = Schema(TEST_SCHEMA)
        test_ref = schema.get(reference)
        assert isinstance(test_ref, Schema)
        assert test_ref.definition == {
            "properties": {
                "test_ref_value": {
                    "type": "string",
                    "default": "REF_VALUE",
                    "title": "Test Ref Value",
                    "description": "A nested property.",
                }
            },
            "type": "object",
            "title": "NestedRef",
        }
        assert test_ref._schema == TEST_SCHEMA["$defs"]["NestedRef"]

    def test_should_get_valid_property(self):
        schema = Schema(TEST_SCHEMA)
        test_value = schema.get("test_property")
        assert isinstance(test_value, Schema)
        assert test_value.definition == {
            "type": "string",
            "default": "PROPERTY_VALUE",
            "title": "Test Property",
            "description": "A string property.",
        }
        assert test_value._schema == TEST_SCHEMA["properties"]["test_property"]

    def test_should_raise_invalid_schema_field_error(self):
        schema = Schema(TEST_SCHEMA)
        with pytest.raises(InvalidSchemaFieldError):
            schema.get("invalid_field")


class TestDescribe:
    def test_should_describe_config(self):
        schema = DescribableConfig.schema()
        data = describe(DescribableConfig, Schema(schema))
        assert data == {
            "test_ref_a": {
                "default": "",
                "type": "NestedRef",
                "description": "For more information use `config show --output test_ref_a`.",
                "values": {
                    "test_ref_value": {
                        "type": "str",
                        "description": "A nested property.",
                        "default": "'REF_VALUE'",
                    }
                },
            },
            "test_ref_b": {
                "default": "",
                "type": "NestedRef | NoneType",
                "description": "For more information use `config show --output test_ref_b`.",
                "values": {
                    "test_ref_value": {
                        "type": "str",
                        "description": "A nested property.",
                        "default": "'REF_VALUE'",
                    }
                },
            },
            "test_property": {"type": "str", "description": "A string property.", "default": "'PROPERTY_VALUE'"},
        }


class TestGetTypeStr:
    @pytest.mark.parametrize(
        (
            "type_",
            "expected",
        ),
        [
            pytest.param(int, "int", id="int"),
            pytest.param(str, "str", id="str"),
            pytest.param(list[int], "list[int]", id="list[int]"),
            pytest.param(list[str], "list[str]", id="list[str]"),
            pytest.param(dict[str, int], "dict[str, int]", id="dict[str, int]"),
            pytest.param(dict[str, str], "dict[str, str]", id="dict[str, str]"),
            pytest.param(set[int], "set[int]", id="set[int]"),
            pytest.param(set[str], "set[str]", id="set[str]"),
            pytest.param(list[DescribableConfig], "list[DescribableConfig]", id="list[DescribableConfig]"),
            pytest.param(set[DescribableConfig], "set[DescribableConfig]", id="set[DescribableConfig]"),
            pytest.param(
                list[typing.Union[DescribableConfig, int]],
                "list[DescribableConfig | int]",
                id="list[DescribableConfig | int]",
            ),
            pytest.param(typing.Annotated[int, "test"], "int", id="int"),
            pytest.param(typing.Literal[1, 2, 3], "1 | 2 | 3", id="Literal[1, 2, 3]"),
            pytest.param(typing.Literal["a", "b", "c"], "'a' | 'b' | 'c'", id="Literal['a', 'b', 'c']"),
        ],
    )
    def test_should_get_type_str(self, type_, expected):
        assert get_type_str(type_) == expected
