import asyncio
import collections.abc
import functools
import importlib
import inspect
import signal
import sys
import types

import typing_extensions as typing

from .connector import Connector

T = typing.TypeVar("T")


Generator = typing.Union[
    collections.abc.Generator[T, None, None],
    collections.abc.AsyncGenerator[T, None],
]


AppFactory = collections.abc.Callable[
    ...,
    typing.Union[
        Connector,
        collections.abc.Awaitable[Connector],
        Generator,
    ],
]


async def run(app: typing.Union[str, AppFactory, Connector], /, config: typing.Optional[dict] = None) -> None:
    """
    Run the given application.

    Args:
      app: Either an entrypoint reference (e.g. `unitelabs.awesome_instrument:create_app`),
        an app factory method or the app instance directly.
      config: Optional configuration to pass to the app factory.
    """

    if isinstance(app, str):
        app = await load(app)

    if callable(app):
        if "config" in inspect.signature(app).parameters:
            from unitelabs.cdk.config import get_connector_config

            configuration = get_connector_config().validate(config)
            app = functools.partial(app, config=configuration)

        app = await init(app_factory=app)

    for signum in (signal.SIGTERM, signal.SIGINT):
        if sys.platform == "win32":
            signal.signal(signum, functools.partial(signal_handler, app=app))
        else:
            asyncio.get_running_loop().add_signal_handler(
                signum, functools.partial(signal_handler, signum, None, app=app)
            )

    try:
        await app.start()
        await app.wait_for_termination()
    finally:
        await app.stop()


async def load(entrypoint: str) -> typing.Union[AppFactory, Connector]:
    """
    Dynamically import an app instance or factory from the given entrypoint.

    Args:
      entrypoint: Where to find the app factory formatted as "module:name",
        (e.g. `unitelabs.awesome_instrument:create_app`)

    Returns:
      The app instance or factory at the given entrypoint.
    """

    module_name, _, factory_name = entrypoint.partition(":")

    if not module_name or not factory_name:
        msg = f"Entrypoint '{entrypoint}' must be in format '<module>:<attribute>'."
        raise ValueError(msg)

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        msg = f"Could not import module '{module_name}': Module not found."
        raise ValueError(msg) from None

    instance = module
    try:
        for attr in factory_name.split("."):
            instance = getattr(instance, attr)
    except AttributeError:
        msg = f"Attribute '{factory_name}' not found in module '{module_name}'."
        raise ValueError(msg) from None

    if callable(instance):
        return typing.cast(AppFactory, instance)

    if isinstance(instance, Connector):
        return instance

    msg = f"Attribute '{factory_name}' in module '{module_name}' is must be app instance or factory."
    raise ValueError(msg)


def signal_handler(signum: int, frame: typing.Optional[types.FrameType], app: Connector) -> None:  # noqa: ARG001
    """
    Gracefully handle received signals.

    Args:
      signum: The received signal number.
      frame: The current stack frame.
      app: The running connector application.
    """

    app.logger.info("Received signal %s. Shutting down...", signal.Signals(signum).name)
    if sys.platform == "win32":
        signal.signal(signum, signal.SIG_DFL)
    else:
        loop = asyncio.get_running_loop()
        loop.remove_signal_handler(signum)
    app._shutdown.set()


async def init(app_factory: AppFactory) -> Connector:
    """
    Use the provided factory method to init a new `Connector`.

    Args:
      app_factory: The factory method to call.

    Returns:
      The initialized `Connector` which shutdown handlers attached.

    Raises:
      ValueError: If `app_factory` does not follow the required
        interface.
    """

    app = None

    if inspect.isasyncgenfunction(app_factory) or inspect.isgeneratorfunction(app_factory):
        generator: Generator[Connector] = app_factory()
        generator = _sync_to_async_gen(generator)

        try:
            app = await generator.__anext__()
        except (StopAsyncIteration, StopIteration):
            msg = "Unable to create app: `create_app` did not yield a value."
            raise ValueError(msg) from None

        shutdown_handler = functools.partial(_shutdown_yield, generator)
        app.on_shutdown(handler=shutdown_handler)

    elif inspect.iscoroutinefunction(app_factory):
        app = await app_factory()

    elif inspect.isfunction(app_factory):
        app = app_factory()

    if app is None:
        msg = f"Invalid `create_app`: '{app_factory}'. Provide a callable function that returns a Connector."
        raise ValueError(msg)

    if not isinstance(app, Connector):
        msg = f"Expected app to be of type 'Connector', received '{app.__class__.__name__}'."
        raise ValueError(msg) from None

    return app


async def _shutdown_yield(generator: collections.abc.AsyncGenerator[T, None]) -> None:
    """
    Execute the shutdown of a factory function.

    Achieved by advancing the iterator after the yield to
    ensure the iteration ends (if not it means there is
    more than one yield in the function).

    Args:
      generator: The factory function to create the app.
    """

    try:
        await generator.__anext__()
    except (StopAsyncIteration, StopIteration):
        pass
    else:
        await _shutdown_yield(generator)


async def _sync_to_async_gen(generator: Generator[T]) -> collections.abc.AsyncGenerator[T, None]:
    """
    Wrap any generator into an async generator.

    Args:
      generator: The generator to wrap as async.

    Returns:
      The async generator.
    """

    if inspect.isasyncgen(generator):
        async for item in generator:
            yield item

        return

    if inspect.isgenerator(generator):
        while True:
            try:
                yield next(generator)
            except StopIteration:
                return
