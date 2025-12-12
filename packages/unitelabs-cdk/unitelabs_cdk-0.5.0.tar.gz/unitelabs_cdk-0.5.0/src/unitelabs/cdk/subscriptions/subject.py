import contextlib
import types
import weakref

import typing_extensions as typing

from .default import _DEFAULT_VALUE, Default
from .subscription import Subscription

IN = typing.TypeVar("IN")
OUT = typing.TypeVar("OUT", default=IN)
T = typing.TypeVar("T")


PipeFunction = typing.Callable[[IN], OUT]


class Subject(typing.Generic[IN, OUT], contextlib.AbstractContextManager):
    """
    An observable that can be updated externally and subscribed to by multiple observers.

    Args:
      maxsize: The maximum number of messages to track in `Subscription` queues created by `subscribe`.
    """

    _pipe: PipeFunction[IN, OUT]

    def __init__(self, maxsize: int = 0, pipe: typing.Optional[PipeFunction[IN, OUT]] = None) -> None:
        self._maxsize = maxsize
        self._value: typing.Union[OUT, Default] = _DEFAULT_VALUE

        self._total_subscribers = 0
        self._subscribers: list["Subscription[OUT]"] = []
        self._children: list[Subject[OUT, typing.Any]] = []
        self._parent: typing.Optional["Subject"] = None
        self._is_temporary = False
        self._context: typing.Optional["Subscription[OUT]"] = None

        def default_pipe(x: IN) -> OUT:
            return typing.cast(OUT, x)

        self._pipe = pipe or default_pipe

    def __repr__(self) -> str:
        name = self.__class__.__name__
        identifier = str(id(self))
        pipe = self._pipe.__name__ if hasattr(self._pipe, "__name__") else self._pipe
        n_subs, n_children = len(self.subscribers), len(self._children)
        return f"{name}({identifier}, {pipe=}, {self.current=}, subscribers=({n_subs}), children=({n_children}))"

    @property
    def current(self) -> typing.Union[OUT, Default]:
        """The current value."""
        return self._value

    @property
    def subscribers(self) -> list["Subscription[OUT]"]:
        """All `Subscription`s listening to this `Subject`."""
        return self._subscribers

    @property
    def has_subscribers(self) -> bool:
        """Whether any `Subject` listens to this `Subscription`."""
        return self._total_subscribers > 0

    def subscribe(self) -> "Subscription[OUT]":
        """Add a `Subscription` that will be notified on `update`."""

        subscription = Subscription[OUT](self._maxsize, self)
        self._on_subscribe(subscription)

        self.subscribers.append(subscription)

        return subscription

    def on_subscribe(self) -> None:
        """
        Emit an event when the first subscription is added.

        Override this method to start external listeners or resources
        when the first subscriber begins listening.
        """

    def _on_subscribe(self, subscription: Subscription) -> None:
        """Emit an event when `subscribe` is called."""
        if not self.has_subscribers:
            self.on_subscribe()
        self._total_subscribers += 1
        if self._parent is not None:
            self._parent._on_subscribe(subscription)

    def unsubscribe(self, subscriber: "Subscription[typing.Any]") -> None:
        """Remove a `Subscription`."""
        if subscriber in self.subscribers:
            subscriber.cancel()
            self.subscribers.remove(subscriber)
            self._on_unsubscribe()
            return

        for child in self._children:
            with contextlib.suppress(ValueError):
                child.unsubscribe(subscriber)
                return

        msg = "Subscription not found in subscribers or children."
        raise ValueError(msg)

    def on_unsubscribe(self) -> None:
        """
        Emit an event when the last subscription is removed.

        Override this method to perform cleanup or release resources when
        there are no active subscribers.
        """

    def _on_unsubscribe(self) -> None:
        """Emit an event when `unsubscribe` is called."""
        self._total_subscribers -= 1
        if not self.has_subscribers:
            self.on_unsubscribe()
        if self._parent is not None:
            if self._is_temporary and not self.subscribers and not self._children:
                self._parent._children.remove(self)
            self._parent._on_unsubscribe()

    def notify(self) -> None:
        """Propagate the current value to all listening `Subscription`s."""
        value = self._value
        if not isinstance(value, Default):
            value = typing.cast(OUT, value)
            for child in self._children:
                child.update(value)
            for subscriber in self.subscribers:
                subscriber.update(value)

    def update(self, value: IN) -> None:
        """Update the current value and `notify` all listening `Subscription`s."""

        self._value = self._pipe(value)
        self.notify()

    def pipe(self, func: typing.Callable[[OUT], T], temporary: bool = False) -> "Subject[OUT, T]":
        """
        Create a new `Subject` with `func` added to the list of pipes that are applied to values recieved from `notify`.

        Args:
          func: The callable that should be applied to all values seen by the new `Subject`.
          temporary: Whether or not the pipe should be pruned from its parent on `unsubscribe`.

        Returns:
          A new `Subject` with the pipe function added.

        Examples:
          Chain multiple pipe functions:
          >>> def first_pipe(x: str) -> str:
          ...     return x.upper()
          >>> def second_pipe(x: str) -> dict[str, str]:
          ...     return {"value": x}
          >>> subject = Subject[str]()
          >>> piped = subject.pipe(first_pipe).pipe(second_pipe)
          >>> async for value in piped.subscribe():
          ...     print(value)
          Here a `value` received from `piped.subscribe()` is equivalent to `second_pipe(first_pipe(x))`
          where `x` is the value received from `Subject.update`.

          Create multiple subjects with different pipes that are simultaneously updated:
          >>> subject = Subject[int]()
          >>> plus_one = subject.pipe(lambda x: x + 1)
          >>> times_two = subject.pipe(lambda x: x * 2)
          >>> subject.update(3)
          >>> await plus_one.get()  # 4
          >>> await times_two.get()  # 6
        """
        if not temporary and self._is_temporary:
            msg = (
                "Cannot create a non-temporary `Subject` from a temporary `Subject`, use pipe() with `temporary=True` "
                "or adjust the current `Subject` to be non-temporary."
            )
            raise RuntimeError(msg)

        new_subject = Subject[OUT, T](maxsize=self._maxsize, pipe=func)
        self._children.append(new_subject)
        new_subject._parent = weakref.proxy(self)
        new_subject._is_temporary = temporary
        return new_subject

    def filter(
        self, predicate: typing.Callable[[OUT], typing.Union[bool, typing.Any]], temporary: bool = False
    ) -> "Subject[OUT, OUT]":
        """
        Create a new `Subject` that is only notified when the item passes the `predicate`.

        Args:
          predicate: A filter predicate to apply.
          temporary: Whether the not the filter should be pruned from its parent on `unsubscribe`.

        Returns:
          A new `Subject` with the filter applied.

        Examples:
          Filter a subject
          >>> subject = Subject[int]()
          >>> filtered = subject.filter(lambda x: x > 5)
          >>> async for value in filtered.subscribe():
          ...     print(value)
          Here `filtered` only receives updates of numbers greater than 5.
        """

        def pipe(item: OUT) -> OUT:
            if bool(predicate(item)):
                return item

            return typing.cast(OUT, _DEFAULT_VALUE)

        return self.pipe(pipe, temporary=temporary)

    @typing.override
    def __enter__(self) -> "Subscription[OUT]":
        """
        Return a new `Subscription` upon entering the runtime context.

        Returns:
          The newly created `Subscription`.

        Examples:
          Subscribe to `my_subject`:
          >>> with my_subject as subscription:
          ...     async for value in subscription:
          ...         print(value)
          When leaving the runtime context, `subscription` is unsubscribed from `my_subject`.
        """
        if self._context is not None:
            msg = (
                "This Subject is already entered in a context. "
                "You cannot enter the same Subject multiple times simultaneously. "
                "Use the existing subscription or exit the previous context first."
            )
            raise RuntimeError(msg)

        self._context = self.subscribe()
        return self._context

    @typing.override
    def __exit__(
        self,
        exc_type: typing.Optional[type[BaseException]] = None,
        exc_value: typing.Optional[BaseException] = None,
        traceback: typing.Optional[types.TracebackType] = None,
    ) -> bool:
        if self._context:
            self.unsubscribe(self._context)
            self._context = None

        return False
