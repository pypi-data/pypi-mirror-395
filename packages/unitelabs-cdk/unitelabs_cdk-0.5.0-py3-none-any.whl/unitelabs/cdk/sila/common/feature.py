import collections.abc
import dataclasses
import functools
import inspect
import warnings

import typing_extensions as typing
from sila.server import Server

import sila

from ..metadata import Metadatum
from ..utils import to_display_name, to_identifier
from .decorator import Decorator

if typing.TYPE_CHECKING:
    from ...connector import Connector


@dataclasses.dataclass
class Feature(sila.framework.Feature):
    """
    A feature describes a specific behavior of the server.

    Use the docstring of your feature class to provide a detailed,
    human-readable description of the use of your feature.
    """

    def __init__(
        self,
        *args,
        identifier: typing.Optional[str] = None,
        display_name: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        metadata: typing.Optional[collections.abc.Sequence[type[Metadatum]]] = None,
        **kwargs,
    ):
        if display_name is not None:
            msg = "Using `display_name` is deprecated, use `name` instead."
            warnings.warn(msg, stacklevel=2)
            name = display_name

        name = name or to_display_name(self.__class__.__name__)
        identifier = identifier or to_identifier(name)
        description = description or next((inspect.getdoc(cls) for cls in inspect.getmro(type(self))), "") or ""

        super().__init__(*args, identifier=identifier, display_name=name, description=description, **kwargs)

        self._metadata: dict[str, type[Metadatum]] = {}
        for metadatum in metadata or []:
            self._metadata[metadatum._identifier] = metadatum
            metadatum.attach(self).add_to_feature(self)

        self._handlers: dict[str, Decorator] = {}
        self._app: typing.Optional["Connector"] = None

    def attach(self) -> bool:
        """
        Attach all handlers to this feature.

        Returns:
          Whether at least one handler was attached.
        """

        attached = False
        abc_methods = {}
        for m in inspect.getmro(type(self)):
            if "unitelabs.cdk.features" in m.__module__:
                abc_methods = dict(inspect.getmembers(m, predicate=inspect.isfunction))
                break
        if abc_methods:
            for name, function in inspect.getmembers(type(self), predicate=inspect.isfunction):
                # move handlers from ABCs to overrides
                if hasattr(function, "__override__") and getattr(function, "__override__", False):
                    abc_method = abc_methods.get(name)
                    if abc_method and (handler := getattr(abc_method, "__handler", None)):
                        setattr(function, "__handler", handler)

        for name, function in inspect.getmembers(type(self), predicate=inspect.isfunction):
            if (handler := getattr(function, "__handler", None)) and isinstance(handler, Decorator):
                handler = handler.clone()

                method = getattr(self, name).__func__
                method = functools.partial(method, self)
                handler._function = functools.wraps(function)(method)

                attached = handler.attach(self) or attached

                if handler._identifier in self._handlers:
                    prev_func = self._handlers[handler._identifier]._function

                    msg = (
                        f"Duplicate handler identifier '{handler._identifier}' detected for feature "
                        f"'{self.__class__.__name__}'. "
                        f"Existing: {self.__class__.__name__}.{prev_func.__name__}. "
                        f"New: {self.__class__.__name__}.{name} (will override). "
                        "To avoid unintended overrides, set a unique 'identifier' in your decorator or "
                        "rename one of the methods."
                    )
                    warnings.warn_explicit(
                        msg,
                        category=UserWarning,
                        filename=inspect.getfile(inspect.unwrap(function)),
                        lineno=inspect.getsourcelines(inspect.unwrap(function))[1],
                    )

                self._handlers[handler._identifier] = handler

        return attached or bool(self.metadata)

    @property
    def app(self) -> "Connector":
        """The connector app this feature is registered with."""

        if not self._app:
            raise RuntimeError

        return self._app

    @property
    def server(self) -> Server:
        """The server this feature is registered with."""

        if not isinstance(self.context, Server):
            raise RuntimeError

        return self.context
