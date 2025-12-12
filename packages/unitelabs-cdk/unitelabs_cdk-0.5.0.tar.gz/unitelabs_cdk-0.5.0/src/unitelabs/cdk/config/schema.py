from dataclasses import fields, is_dataclass

import typing_extensions as typing

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance


class InvalidSchemaFieldError(Exception):
    """The provided key is not present in the Schema."""


class Schema:
    """Wrapper for JSONSchema dictionaries."""

    def __init__(
        self,
        schema: dict[str, typing.Any],
        definitions: typing.Optional[dict[str, typing.Any]] = None,
    ):
        self._schema = schema
        self._schema_definitions = definitions or schema.get("$defs")

    @property
    def definition(self) -> dict[str, str]:
        """Get the JSONSchema definition."""
        return self._schema

    def get(self, field: str) -> "Schema":
        """
        Extract a nested `Schema` object for named `field`.

        Args:
          field: The name of the field in the schema to extract.

        Raises:
          InvalidSchemaKeyError: If the provided `field` is not present in the schema.
        """
        schema = self._schema["properties"].get(field, {})

        valid_fields = list(self._schema["properties"].keys())
        msg = f"{field} is not a valid field or nested schema, valid schemas include: {valid_fields}"

        if "anyOf" in schema and (has_ref := [f for f in schema["anyOf"] if "$ref" in f]):
            if not has_ref or len(has_ref) != 1:
                raise InvalidSchemaFieldError(msg)

            ref = has_ref[0].get("$ref", "").removeprefix("#/$defs/")
            return Schema(self._schema_definitions[ref], self._schema_definitions)

        if not schema:
            raise InvalidSchemaFieldError(msg)

        if ref := schema.get("$ref", "").removeprefix("#/$defs/"):
            return Schema(self._schema_definitions[ref], self._schema_definitions)

        return Schema(schema, self._schema_definitions)


def describe(
    dataclass: type["DataclassInstance"], schema: Schema, default: typing.Optional["DataclassInstance"] = None
) -> dict[str, typing.Any]:
    """
    Build a dict of values describing the keys, their types, descriptions and defaults.

    Args:
      dataclass: The dataclass to describe.
      schema: A wrapped JSONSchema for the dataclass, used for extracting description docstrings.
      default: A default instance of the dataclass to use for extracting default values.
    """
    description = {}
    default = default or dataclass()
    for field in fields(dataclass):
        name = field.name
        field_type = field.type
        field_schema = schema.get(name).definition
        field_default = getattr(default, name)
        data = dict(
            type=get_type_str(field_type),
            description=field_schema.get("description", "").replace("\n", " "),
            default=f"'{field_default}'" if isinstance(field_default, str) else str(field_default),
        )
        if (
            typing.get_origin(field_type) == typing.Union
            and (args := typing.get_args(field_type))
            and any(is_dataclass(arg) for arg in args)
        ):
            field_type = args[0]
        if is_dataclass(field_type):
            data.update(
                default="",
                description=f"For more information use `config show --output {name}`.",
                values=describe(field_type, schema.get(name), field_default),
            )

        description[name] = data

    return description


def get_type_str(type_: typing.Any) -> str:  # noqa: ANN401
    """
    Get a formatted string representation of a type.

    Args:
      type_: The type to get a string representation of.

    Returns:
      A formatted string representation of the type.

    Examples:
      >>> get_type_str(int)
      'int'
      >>> get_type_str(list[int])
      'list[int]'
      >>> get_type_str(list[typing.Union[int, str]])
      'list[int | str]'
      >>> get_type_str(list[dataclass_type])
      'list[dataclass_type]'
    """
    origin = typing.get_origin(type_)
    if args := typing.get_args(type_):
        import typing as t

        if origin == typing.Annotated:
            args = args[:-1]
        if origin in [t.Literal, typing.Literal]:
            args = (
                [f"'{arg}'" for arg in args]
                if all(isinstance(arg, str) for arg in args)
                else [str(arg) for arg in args]
            )
        if origin in [list, set, dict]:
            return f"{origin.__name__}[{', '.join([get_type_str(arg) for arg in args])}]"
        return " | ".join([get_type_str(arg) for arg in args])

    return getattr(type_, "__name__", type_)
