import collections.abc
import dataclasses
import datetime
import inspect

import typing_extensions as typing
from sila.server import (
    Binary,
    Boolean,
    Constrained,
    DataType,
    Date,
    Integer,
    List,
    Native,
    Real,
    String,
    Time,
    Timestamp,
    Void,
)

from ..utils import parse_docstring
from .any import Any
from .custom_data_type import CustomDataType
from .structure import Structure

if typing.TYPE_CHECKING:
    from ..common import Feature


def infer(annotation: type, feature: "Feature") -> type[DataType]:
    """
    Infer the SiLA data type from a given python type annotation.

    Args:
      annotation: The python type annotation.
      feature: The feature.

    Returns:
      The corresponding SiLA data type.
    """

    if annotation == inspect._empty:
        return Any

    origin = typing.get_origin(annotation) or annotation

    if origin is None:
        return Void
    if origin is typing.Annotated:
        args = typing.get_args(annotation)
        return Constrained.create(data_type=infer(args[0], feature), constraints=list(args[1:]))
    if origin is typing.Union and annotation is Native:
        return Any
    if origin is typing.Any:
        return Any
    if issubclass(origin, type(None)):
        return Void
    if issubclass(origin, CustomDataType):
        return origin.attach(feature)
    if dataclasses.is_dataclass(origin):
        docstring = parse_docstring(origin, feature=feature)
        data_type = Structure.create(
            elements=docstring.parameters, name=origin.__name__, description=docstring.description
        )
        data_type._class = origin
        return data_type
    if issubclass(origin, DataType):
        return origin
    if issubclass(origin, bool):
        return Boolean
    if issubclass(origin, int):
        return Integer
    if issubclass(origin, float):
        return Real
    if issubclass(origin, str):
        return String
    if issubclass(origin, bytes):
        return Binary
    if issubclass(origin, datetime.datetime):
        return Timestamp
    if issubclass(origin, datetime.date):
        return Date
    if issubclass(origin, datetime.time):
        return Time
    if issubclass(origin, list):
        arg = typing.get_args(annotation)
        if not arg:
            msg = f"Unable to identify SiLA type from annotation '{annotation}'"
            raise TypeError(msg)

        return List.create(data_type=infer(arg[0], feature))
    if issubclass(origin, collections.abc.AsyncIterable):
        arg = typing.get_args(annotation)
        if not arg:
            msg = f"Unable to identify SiLA type from annotation '{annotation}'"
            raise TypeError(msg)

        return infer(arg[0], feature)
    if inspect.isclass(origin):
        docstring = parse_docstring(origin, feature=feature)
        data_type = Structure.create(
            elements=docstring.parameters, name=origin.__name__, description=docstring.description
        )
        data_type._class = origin
        return data_type

    msg = f"Unable to identify SiLA type from annotation '{annotation}'"
    raise TypeError(msg)
