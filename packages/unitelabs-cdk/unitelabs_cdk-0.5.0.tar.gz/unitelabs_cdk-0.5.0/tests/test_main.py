import asyncio
import signal
import unittest.mock

import pytest

from unitelabs.cdk.connector import Connector
from unitelabs.cdk.main import init, load, run, signal_handler


@pytest.fixture
async def app():
    return Connector()


class TestRun:
    async def test_should_run_with_factory(self, app: Connector):
        app.start = unittest.mock.AsyncMock()
        app.wait_for_termination = unittest.mock.AsyncMock()
        app.stop = unittest.mock.AsyncMock()

        async def app_factory() -> Connector:
            return app

        # Run
        await run(app_factory)

        # Assert that the method returns the correct value
        app.start.assert_called_once_with()
        app.stop.assert_called_once_with()

    async def test_should_run_with_instance(self, app: Connector):
        app.start = unittest.mock.AsyncMock()
        app.wait_for_termination = unittest.mock.AsyncMock()
        app.stop = unittest.mock.AsyncMock()

        # Run
        await run(app)

        # Assert that the method returns the correct value
        app.start.assert_called_once_with()
        app.stop.assert_called_once_with()


class TestSignalHandler:
    async def test_signal_handler_exists_with_signum(self):
        app = unittest.mock.Mock(_shutdown=asyncio.Event())

        signal_handler(signum=signal.SIGINT, frame=None, app=app)

        assert app._shutdown.is_set()


class TestLoad:
    async def test_should_load_factory(self):
        # Load
        result = await load("unitelabs.cdk.main:load")

        # Assert that the method returns the correct value
        assert result == load

    async def test_should_raise_on_invalid_format(self):
        # Load
        with pytest.raises(ValueError, match=r"Entrypoint 'unitelabs' must be in format '<module>:<attribute>'\."):
            await load("unitelabs")

    async def test_should_raise_on_unknown_module(self):
        # Load
        with pytest.raises(ValueError, match=r"Could not import module 'module': Module not found\."):
            await load("module:attribute")

    async def test_should_raise_on_unknown_attribute(self):
        # Load
        with pytest.raises(ValueError, match=r"Attribute 'attribute' not found in module 'unitelabs.cdk.main'\."):
            await load("unitelabs.cdk.main:attribute")

    async def test_should_raise_on_non_connector(self):
        # Load
        with pytest.raises(
            ValueError, match=r"Attribute 'T' in module 'unitelabs.cdk.main' is must be app instance or factory\."
        ):
            await load("unitelabs.cdk.main:T")


class TestInit:
    async def test_should_init_function(self, app: Connector):
        # Create factory
        def factory():
            return app

        # Init
        result = await init(factory)

        # Assert that the method returns the correct value
        assert result == app
        assert not result._shutdown_handlers

    async def test_should_init_async_function(self, app: Connector):
        # Create factory
        async def factory():
            return app

        # Init
        result = await init(factory)

        # Assert that the method returns the correct value
        assert result == app
        assert not result._shutdown_handlers

    async def test_should_init_generator(self, app: Connector):
        # Create factory
        def factory():
            yield app

        # Init
        result = await init(factory)

        # Assert that the method returns the correct value
        assert result == app

    async def test_should_init_async_generator(self, app: Connector):
        # Create factory
        async def factory():
            yield app

        # Init
        result = await init(factory)

        # Assert that the method returns the correct value
        assert result == app

    async def test_should_register_shutdown_handler(self, app: Connector):
        # Create factory
        callback = unittest.mock.Mock()

        async def factory():
            yield app
            callback()

        # Init
        result = await init(factory)
        await result.stop()

        # Assert that the method returns the correct value
        callback.assert_called_once_with()

    async def test_should_register_async_shutdown_handler(self, app: Connector):
        # Create factory
        callback = unittest.mock.Mock()

        async def factory():
            yield app
            callback()

        # Init
        result = await init(factory)
        await result.stop()

        # Assert that the method returns the correct value
        callback.assert_called_once_with()

    async def test_should_register_terminate_on_multiple_yields(self, app: Connector):
        # Create factory
        callback = unittest.mock.Mock()

        async def factory():
            yield app
            yield
            callback()

        # Init
        result = await init(factory)
        await result.stop()

        # Assert that the method returns the correct value
        callback.assert_called_once_with()

    async def test_should_raise_on_empty_generator(self):
        # Create factory
        def factory():
            return
            yield

        # Init
        with pytest.raises(ValueError, match=r"Unable to create app: `create_app` did not yield a value\."):
            await init(factory)

    async def test_should_raise_on_non_connector(self):
        # Create factory
        def factory():
            return object()

        # Init
        with pytest.raises(ValueError, match=r"Expected app to be of type 'Connector', received 'object'\."):
            await init(factory)  # type: ignore
