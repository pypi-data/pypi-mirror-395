import unittest.mock

from unitelabs.cdk.sila.common.decorator import Decorator


class TestCall:
    def test_should_call_decorator(self):
        # Create decorator
        decorator = Decorator(
            identifier="Identifier",
            name="Name",
            errors=[Exception],
            enabled=True,
        )

        # Call decorator
        function = unittest.mock.Mock()
        decorator(function)

        # Assert that the method returns the correct value
        assert decorator._function == function
        assert getattr(function, "__handler") == decorator


class TestCopy:
    def test_should_copy_decorator(self):
        # Create decorator
        decorator = Decorator(
            identifier="Identifier",
            name="Name",
            errors=[Exception],
            enabled=True,
        )

        # Copy decorator
        copy = decorator.clone()

        # Assert that the method returns the correct value
        assert copy is not decorator
        assert copy._identifier == "Identifier"
        assert copy._name == "Name"
        assert copy._description == ""
        assert copy._enabled is True
        assert copy._errors == [Exception]
