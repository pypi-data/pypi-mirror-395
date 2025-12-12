import typing
import unittest.mock

import pytest
from sila.framework.errors.defined_execution_error import DefinedExecutionError

import sila
from unitelabs.cdk.sila.common.feature import Feature
from unitelabs.cdk.sila.data_types.any import Any
from unitelabs.cdk.sila.property.observable_property import ObservableProperty, Stream


class DefinedError(Exception):
    pass


@pytest.fixture
def feature():
    return Feature(identifier="Feature", name="Feature")


@pytest.fixture
def handler():
    return ObservableProperty(identifier="ObservableProperty", name="Observable Property", errors=[DefinedError])


class TestAttach:
    async def test_should_attach_handler(self, feature: Feature, handler: ObservableProperty):
        # Attach
        attached = handler.attach(feature)

        # Assert that the method returns the correct value
        assert attached is True
        assert feature.properties[handler._identifier] == handler._handler

    async def test_should_ignore_disabled_handler(self, feature: Feature, handler: ObservableProperty):
        # Attach
        handler._enabled = False
        attached = handler.attach(feature)

        # Assert that the method returns the correct value
        assert attached is False
        assert handler._identifier not in feature.properties

    async def test_should_call_enabled_callback(self, feature: Feature, handler: ObservableProperty):
        # Attach
        handler._enabled = unittest.mock.Mock(return_value=True)
        attached = handler.attach(feature)

        # Assert that the method returns the correct value
        assert attached is True
        assert feature.properties[handler._identifier] == handler._handler
        handler._enabled.assert_called_once_with(feature)

    async def test_should_attach_return_annotation(self, feature: Feature, handler: ObservableProperty):
        # Create handler
        def function() -> Stream[int]:
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.ObservableProperty)
        assert handler._handler.data_type == sila.Integer

    async def test_should_attach_missing_return_annotation(self, feature: Feature, handler: ObservableProperty):
        # Create handler
        def function():
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.ObservableProperty)
        assert handler._handler.data_type == Any

    async def test_should_attach_annotated_return(self, feature: Feature, handler: ObservableProperty):
        # Create handler
        def function() -> Stream[typing.Annotated[int, sila.Unit("s", [sila.UnitComponent("Second")])]]:
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.ObservableProperty)
        assert issubclass(handler._handler.data_type, sila.Constrained)
        assert handler._handler.data_type.data_type == sila.Integer
        assert handler._handler.data_type.constraints == [sila.Unit("s", [sila.UnitComponent("Second")])]

    async def test_should_attach_documented_error(self, feature: Feature, handler: ObservableProperty):
        # Create handler
        def function() -> Stream[int]:
            """
            A function that yields an integer.

            Raises:
              RuntimeError: When something goes wrong.
            """
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.ObservableProperty)
        assert len(handler._handler.errors) == 2

        assert handler._handler.errors["DefinedError"].identifier == "DefinedError"
        assert handler._handler.errors["DefinedError"].display_name == "Defined Error"
        assert handler._handler.errors["DefinedError"].description == "Common base class for all non-exit exceptions."

        assert handler._handler.errors["RuntimeError"].identifier == "RuntimeError"
        assert handler._handler.errors["RuntimeError"].display_name == "Runtime Error"
        assert handler._handler.errors["RuntimeError"].description == "When something goes wrong."

    async def test_should_recognize_duplicate_errors(self, feature: Feature, handler: ObservableProperty):
        # Create handler
        def function() -> Stream[int]:
            """
            A function that yields an integer.

            Raises:
              DefinedError: When something goes wrong.
            """
            return unittest.mock.sentinel.response

        handler(function)

        # Attach
        handler.attach(feature)

        # Assert that the method returns the correct value
        assert isinstance(handler._handler, sila.ObservableProperty)
        assert len(handler._handler.errors) == 1
        assert handler._handler.errors["DefinedError"].identifier == "DefinedError"
        assert handler._handler.errors["DefinedError"].display_name == "Defined Error"
        assert handler._handler.errors["DefinedError"].description == "When something goes wrong."


class TestExecute:
    # Execute synchronous function with default parameters.
    async def test_execute_synchronous_default_parameters(self, feature: Feature, handler: ObservableProperty):
        # Initialize the observable property
        callback = unittest.mock.Mock()

        async def function() -> Stream[int]:
            callback()
            yield 1
            yield 2
            yield 3

        handler(function)
        handler.attach(feature)

        # Execute function
        result = handler.execute(metadata={})
        result_0 = await result.__anext__()
        result_1 = await result.__anext__()
        result_2 = await result.__anext__()

        # Assert that the function was called with the correct arguments
        callback.assert_called_once_with()

        # Assert that the method returns the correct value
        assert result_0 == {"ObservableProperty": 1}
        assert result_1 == {"ObservableProperty": 2}
        assert result_2 == {"ObservableProperty": 3}

    # Verify that the method raises an error when the synchronous function raises.
    async def test_raises_when_synchronous_raises(self, feature: Feature, handler: ObservableProperty):
        # Initialize the observable property
        def function() -> Stream[int]:
            msg = "Hello, World!"
            raise Exception(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        result = handler.execute(metadata={})
        with pytest.raises(Exception, match=r"Exception: Hello, World!"):
            await result.__anext__()

    # Verify that the method raises a defined execution error when the synchronous decorator knows the error type.
    async def test_raises_when_synchronous_raises_known_error(self, feature: Feature, handler: ObservableProperty):
        # Initialize the observable property
        def function() -> Stream[int]:
            msg = "Hello, World!"
            raise DefinedError(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        result = handler.execute(metadata={})
        with pytest.raises(DefinedExecutionError) as exc_info:
            await result.__anext__()

        assert exc_info.value.identifier == "DefinedError"
        assert exc_info.value.display_name == "Defined Error"
        assert exc_info.value.description == "Common base class for all non-exit exceptions."
        assert exc_info.value.message == "Hello, World!"

    # Execute asynchronous function with default parameters.
    async def test_execute_asynchronous_default_parameters(self, feature: Feature, handler: ObservableProperty):
        # Initialize the observable property
        callback = unittest.mock.AsyncMock()

        async def function() -> Stream[int]:
            await callback()
            yield 1
            yield 2
            yield 3

        handler(function)
        handler.attach(feature)

        # Execute function
        result = handler.execute(metadata={})
        result_0 = await result.__anext__()
        result_1 = await result.__anext__()
        result_2 = await result.__anext__()

        # Assert that the function was called with the correct arguments
        callback.assert_awaited_once_with()

        # Assert that the method returns the correct value
        assert result_0 == {"ObservableProperty": 1}
        assert result_1 == {"ObservableProperty": 2}
        assert result_2 == {"ObservableProperty": 3}

    # Verify that the method raises an error when the asynchronous function raises.
    async def test_raises_when_asynchronous_raises(self, feature: Feature, handler: ObservableProperty):
        # Initialize the observable property
        async def function() -> Stream[int]:
            msg = "Hello, World!"
            raise Exception(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        result = handler.execute(metadata={})
        with pytest.raises(Exception, match=r"Exception: Hello, World!"):
            await result.__anext__()

    # Verify that the method raises a defined execution error when the asynchronous decorator knows the error type.
    async def test_raises_when_asynchronous_raises_known_error(self, feature: Feature, handler: ObservableProperty):
        # Initialize the observable property
        async def function() -> Stream[int]:
            msg = "Hello, World!"
            raise DefinedError(msg)

        handler(function)
        handler.attach(feature)

        # Execute function
        result = handler.execute(metadata={})
        with pytest.raises(DefinedExecutionError) as exc_info:
            await result.__anext__()

        assert exc_info.value.identifier == "DefinedError"
        assert exc_info.value.display_name == "Defined Error"
        assert exc_info.value.description == "Common base class for all non-exit exceptions."
        assert exc_info.value.message == "Hello, World!"
