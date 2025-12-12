import typing
import unittest.mock

import pytest
from sila.framework.errors.defined_execution_error import DefinedExecutionError

import sila
from unitelabs.cdk.sila.common.feature import Feature
from unitelabs.cdk.sila.data_types.any import Any
from unitelabs.cdk.sila.property.unobservable_property import UnobservableProperty


class DefinedError(Exception):
    pass


@pytest.fixture
def feature():
    return Feature(identifier="Feature", name="Feature")


@pytest.fixture
def handler():
    return UnobservableProperty(identifier="UnobservableProperty", name="Unobservable Property", errors=[DefinedError])


class TestAttach:
    async def test_should_attach_handler(self, feature: Feature, handler: UnobservableProperty):
        # Attach
        attached = handler.attach(feature)

        # Assert that the method returns the correct value
        assert attached is True
        assert feature.properties[handler._identifier] == handler._handler

    async def test_should_ignore_disabled_handler(self, feature: Feature, handler: UnobservableProperty):
        # Attach
        handler._enabled = False
        attached = handler.attach(feature)

        # Assert that the method returns the correct value
        assert attached is False
        assert handler._identifier not in feature.properties

    async def test_should_call_enabled_callback(self, feature: Feature, handler: UnobservableProperty):
        # Attach
        handler._enabled = unittest.mock.Mock(return_value=True)
        attached = handler.attach(feature)

        # Assert that the method returns the correct value
        assert attached is True
        assert feature.properties[handler._identifier] == handler._handler
        handler._enabled.assert_called_once_with(feature)

    async def test_should_attach_return_annotation(self, feature: Feature, handler: UnobservableProperty):
        # Create handler
        def function() -> int:
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.UnobservableProperty)
        assert handler._handler.data_type == sila.Integer

    async def test_should_attach_missing_return_annotation(self, feature: Feature, handler: UnobservableProperty):
        # Create handler
        def function():
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.UnobservableProperty)
        assert handler._handler.data_type == Any

    async def test_should_attach_annotated_return(self, feature: Feature, handler: UnobservableProperty):
        # Create handler
        def function() -> typing.Annotated[int, sila.Unit("s", [sila.UnitComponent("Second")])]:
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.UnobservableProperty)
        assert issubclass(handler._handler.data_type, sila.Constrained)
        assert handler._handler.data_type.data_type == sila.Integer
        assert handler._handler.data_type.constraints == [sila.Unit("s", [sila.UnitComponent("Second")])]

    async def test_should_attach_documented_error(self, feature: Feature, handler: UnobservableProperty):
        # Create handler
        def function() -> int:
            """
            A function that returns an integer.

            Raises:
              RuntimeError: When something goes wrong.
            """
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.UnobservableProperty)
        assert len(handler._handler.errors) == 2

        assert handler._handler.errors["DefinedError"].identifier == "DefinedError"
        assert handler._handler.errors["DefinedError"].display_name == "Defined Error"
        assert handler._handler.errors["DefinedError"].description == "Common base class for all non-exit exceptions."

        assert handler._handler.errors["RuntimeError"].identifier == "RuntimeError"
        assert handler._handler.errors["RuntimeError"].display_name == "Runtime Error"
        assert handler._handler.errors["RuntimeError"].description == "When something goes wrong."

    async def test_should_recognize_duplicate_errors(self, feature: Feature, handler: UnobservableProperty):
        # Create handler
        def function() -> int:
            """
            A function that returns an integer.

            Raises:
              DefinedError: When something goes wrong.
            """
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.UnobservableProperty)
        assert len(handler._handler.errors) == 1
        assert handler._handler.errors["DefinedError"].identifier == "DefinedError"
        assert handler._handler.errors["DefinedError"].display_name == "Defined Error"
        assert handler._handler.errors["DefinedError"].description == "When something goes wrong."


class TestExecute:
    # Execute synchronous function with default parameters.
    async def test_execute_synchronous_default_parameters(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        callback = unittest.mock.Mock()

        def function():
            callback()
            return unittest.mock.sentinel.response

        handler(function)
        handler.attach(feature)

        # Execute function
        result = await handler.execute(metadata={})

        # Assert that the function was called with the correct arguments
        callback.assert_called_once_with()

        # Assert that the method returns the correct value
        assert result == {"UnobservableProperty": unittest.mock.sentinel.response}

    # Execute synchronous function with no return value.
    async def test_execute_synchronous_returns_any(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        callback = unittest.mock.Mock()

        def function():
            callback()

        handler(function)
        handler.attach(feature)

        # Execute function
        result = await handler.execute(metadata={})

        # Assert that the method returns the correct value
        callback.assert_called_once_with()
        assert result == {"UnobservableProperty": None}

    # Verify that the method raises an error when the synchronous function raises.
    async def test_raises_when_synchronous_raises(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        def function():
            msg = "Hello, World!"
            raise Exception(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        with pytest.raises(Exception, match=r"Exception: Hello, World!"):
            await handler.execute(metadata={})

    # Verify that the method raises a defined execution error when the synchronous decorator knows the error type.
    async def test_raises_when_synchronous_raises_known_error(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        def function():
            msg = "Hello, World!"
            raise DefinedError(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        with pytest.raises(DefinedExecutionError) as exc_info:
            await handler.execute(metadata={})

        assert exc_info.value.identifier == "DefinedError"
        assert exc_info.value.display_name == "Defined Error"
        assert exc_info.value.description == "Common base class for all non-exit exceptions."
        assert exc_info.value.message == "Hello, World!"

    # Execute asynchronous function with default parameters.
    async def test_execute_asynchronous_default_parameters(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        callback = unittest.mock.AsyncMock()

        async def function():
            await callback()
            return unittest.mock.sentinel.response

        handler(function)
        handler.attach(feature)

        # Execute function
        result = await handler.execute(metadata={})

        # Assert that the function was called with the correct arguments
        callback.assert_awaited_once_with()

        # Assert that the method returns the correct value
        assert result == {"UnobservableProperty": unittest.mock.sentinel.response}

    # Execute asynchronous function with no return value.
    async def test_execute_asynchronous_returns_any(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        callback = unittest.mock.AsyncMock()

        async def function():
            await callback()

        handler(function)
        handler.attach(feature)

        # Execute function
        result = await handler.execute(metadata={})

        # Assert that the method returns the correct value
        callback.assert_awaited_once_with()
        assert result == {"UnobservableProperty": None}

    # Verify that the method raises an error when the asynchronous function raises.
    async def test_raises_when_asynchronous_raises(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        async def function():
            msg = "Hello, World!"
            raise Exception(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        with pytest.raises(Exception, match=r"Exception: Hello, World!"):
            await handler.execute(metadata={})

    # Verify that the method raises a defined execution error when the asynchronous decorator knows the error type.
    async def test_raises_when_asynchronous_raises_known_error(self, feature: Feature, handler: UnobservableProperty):
        # Initialize the unobservable property
        async def function():
            msg = "Hello, World!"
            raise DefinedError(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        with pytest.raises(DefinedExecutionError) as exc_info:
            await handler.execute(metadata={})

        assert exc_info.value.identifier == "DefinedError"
        assert exc_info.value.display_name == "Defined Error"
        assert exc_info.value.description == "Common base class for all non-exit exceptions."
        assert exc_info.value.message == "Hello, World!"
