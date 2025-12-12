import collections.abc
import dataclasses
import inspect
import re
import warnings

import griffe
import typing_extensions as typing

from sila import DefinedExecutionError, Element, Feature

from .name import to_display_name, to_identifier


@dataclasses.dataclass
class Docstring:
    """A parsed docstring of a function or class."""

    description: str = ""
    parameters: dict[str, Element] = dataclasses.field(default_factory=dict)
    yields: dict[str, Element] = dataclasses.field(default_factory=dict)
    returns: dict[str, Element] = dataclasses.field(default_factory=dict)
    raises: dict[str, DefinedExecutionError] = dataclasses.field(default_factory=dict)


def parse_docstring(functionOrClass: typing.Union[collections.abc.Callable, type], /, feature: Feature) -> Docstring:
    """
    Parse the docstring of a function or class.

    Args:
      functionOrClass: The function or class to parse the docstring of.
      feature: The parent feature of the function or class.

    Returns:
      The parsed docstring.
    """

    signature = inspect.signature(functionOrClass)
    doc = inspect.getdoc(functionOrClass) or ""

    from ..command import Intermediate, Status
    from ..metadata import Metadata

    # Types
    parameters: list[griffe.DocstringParameter] = []
    yields: list[griffe.DocstringYield] = []
    returns: list[griffe.DocstringReturn] = []

    if dataclasses.is_dataclass(functionOrClass):
        parameters = [
            griffe.DocstringParameter(name=field.name, description="", annotation=field.type, value=field.name)
            for field in dataclasses.fields(functionOrClass)
        ]
    elif isinstance(functionOrClass, type):
        parameters = [
            griffe.DocstringParameter(name=name, description="", annotation=annotation, value=name)
            for name, annotation in typing.get_type_hints(functionOrClass).items()
        ]
    else:
        returns = [
            griffe.DocstringReturn(name=f"response_{i}", description="", annotation=return_annotation)
            for i, return_annotation in enumerate(get_types(signature.return_annotation))
        ]

        for i, (name, item) in enumerate(signature.parameters.items()):
            origin = typing.get_origin(item.annotation) or item.annotation

            if origin is Intermediate:
                args = typing.get_args(item.annotation)
                yields = [
                    griffe.DocstringYield(
                        name=f"intermediate_response_{j}", description="", annotation=yield_annotation
                    )
                    for j, yield_annotation in enumerate(get_types(args[0] if args else inspect._empty))
                ]
                continue

            if origin is typing.Annotated and typing.get_args(item.annotation)[0] is Metadata:
                continue

            if item.annotation is Status:
                continue

            if i == 0 and name in ("self", "cls"):
                continue

            parameters.append(
                griffe.DocstringParameter(name=item.name, description="", annotation=item.annotation, value=name)
            )

    # Docstring
    parent = griffe.Function(name=functionOrClass.__name__)
    docstring = griffe.Docstring(doc, parent=parent)

    if ".. parameter::" in doc or ".. yield::" in doc or ".. return::" in doc:
        _warn(
            "Using reStructuredText based docstrings is deprecated. Please use google based formatting instead.",
            functionOrClass,
            category=DeprecationWarning,
        )
        docstring.parent.parameters = griffe.Parameters(*parameters)
        sections = parse_restructured(docstring)
    else:
        sections = griffe.parse(
            docstring, "google", returns_multiple_items=True, returns_named_value=True, warnings=False
        )

    result = Docstring()

    for section in sections:
        if isinstance(section, griffe.DocstringSectionText):
            result.description += section.value

        if isinstance(section, griffe.DocstringSectionExamples):
            result.description += "\n\n"
            for example in section.value:
                result.description += example[1] + "\n"

        if isinstance(section, (griffe.DocstringSectionParameters, griffe.DocstringSectionAttributes)):
            for i, item in enumerate(section.value):
                if len(parameters) <= i:
                    _warn(
                        f"Found documentation '{item.name}: {item.description}' for non-existent parameter.",
                        functionOrClass,
                    )
                    continue

                if item.annotation is not None:
                    _warn(
                        "Using type annotations inside your docstring is not allowed and will be ignored.",
                        functionOrClass,
                    )

                parameters[i].name = item.name or parameters[i].name
                parameters[i].description = item.description

        if isinstance(section, griffe.DocstringSectionYields):
            for i, item in enumerate(section.value):
                if len(yields) <= i:
                    _warn(
                        f"Found documentation '{item.name}: {item.description}' for non-existent yield.",
                        functionOrClass,
                    )
                    continue

                if item.annotation is not None:
                    _warn(
                        "Using type annotations inside your docstring is not allowed and will be ignored.",
                        functionOrClass,
                    )

                yields[i].name = item.name or yields[i].name
                yields[i].description = item.description

        if isinstance(section, griffe.DocstringSectionReturns):
            for i, item in enumerate(section.value):
                if len(returns) <= i:
                    _warn(
                        f"Found documentation '{item.name}: {item.description}' for non-existent return.",
                        functionOrClass,
                    )
                    continue

                if item.annotation is not None:
                    _warn(
                        "Using type annotations inside your docstring is not allowed and will be ignored.",
                        functionOrClass,
                    )

                returns[i].name = item.name or returns[i].name
                returns[i].description = item.description

        if isinstance(section, griffe.DocstringSectionRaises):
            for item in section.value:
                name = to_display_name(str(item.annotation))
                key = name.replace(" ", "_").lower()

                result.raises[key] = DefinedExecutionError.create(
                    identifier=to_identifier(name), display_name=name, description=item.description
                )

    result.parameters = dict(create_element(item, feature) for item in parameters)
    result.yields = dict(create_element(item, feature) for item in yields)
    result.returns = dict(create_element(item, feature) for item in returns)

    return result


def parse_restructured(docstring: griffe.Docstring) -> list[griffe.DocstringSection]:
    """
    Parse documentation strings in reStructuredText format.

    Args:
      docstring: The docstring to parse.

    Returns:
      The parsed docstring.
    """

    sections: list[griffe.DocstringSection] = []
    directives = re.split(r"^\.\. *([^:]+):: *", docstring.value, flags=re.MULTILINE)

    if not isinstance(docstring.parent, griffe.Function):
        return sections

    section = griffe.DocstringSectionText(value=inspect.cleandoc(directives.pop(0)))
    parameters = griffe.DocstringSectionParameters(value=[])
    yields = griffe.DocstringSectionYields(value=[])
    returns = griffe.DocstringSectionReturns(value=[])

    for i in range(0, len(directives), 2):
        key = directives[i]
        params = re.split(r"^ *:([^:]+): *", directives[i + 1], flags=re.MULTILINE)
        name = ""
        description = inspect.cleandoc(params.pop(0)).replace("\n", " ")

        par = {params[i]: params[i + 1] for i in range(0, len(params), 2)}
        for param_k, param_v in par.items():
            if param_k == "name":
                name = inspect.cleandoc(param_v).replace("\n", " ")

        if key == "parameter":
            parameter = docstring.parent.parameters[len(parameters.value)]

            parameters.value.append(
                griffe.DocstringParameter(
                    name=name or to_display_name(parameter.name),
                    description=description,
                )
            )

        if key == "yield":
            yields.value.append(griffe.DocstringYield(name=name.replace(" ", "_"), description=description))

        if key == "return":
            returns.value.append(griffe.DocstringReturn(name=name.replace(" ", "_"), description=description))

    sections.append(section)

    if parameters.value:
        sections.append(parameters)

    if yields.value:
        sections.append(yields)

    if returns.value:
        sections.append(returns)

    return sections


def create_element(
    item: typing.Union[griffe.DocstringParameter, griffe.DocstringYield, griffe.DocstringReturn],
    feature: Feature,
    default: str = "",
) -> tuple[str, Element]:
    """
    Create an element from a docstring item.

    Args:
      item: The docstring item to create an element from.
      feature: The parent feature of the element.
      functionOrClass: The function or class the docstring is from.
      default: The default name of the element.

    Returns:
      The created element.
    """

    from ..data_types import infer

    name = to_display_name(item.name or default)
    key = item.value or name.replace(" ", "_").lower()

    return key, Element(
        identifier=to_identifier(name),
        display_name=name,
        description=item.description,
        data_type=infer(item.annotation, feature),
    )


def _warn(
    msg: str, functionOrClass: typing.Union[collections.abc.Callable, type], category: type[Warning] = UserWarning
) -> None:
    warnings.warn_explicit(
        msg,
        category=category,
        filename=inspect.getfile(inspect.unwrap(functionOrClass)),
        lineno=inspect.getsourcelines(inspect.unwrap(functionOrClass))[1],
    )


def get_types(annotation: type) -> list[type]:
    """
    Get the types from an annotation.

    Args:
      annotation: The annotation to get the types from.

    Returns:
      The types.
    """

    return (
        list(typing.get_args(annotation))
        if (typing.get_origin(annotation) or annotation) is tuple
        else [annotation]
        if annotation is not None and annotation is not type(None)
        else []
    )
