from sila.framework.errors.defined_execution_error import DefinedExecutionError
from unitelabs.cdk.sila.common.errors import define_error


class TestDefineError:
    # Defines an error with exception type.
    def test_define_error_with_type(self):
        exception = Exception

        defined_execution_error = define_error(exception)

        assert issubclass(defined_execution_error, DefinedExecutionError)
        assert defined_execution_error.identifier == "Exception"
        assert defined_execution_error.display_name == "Exception"
        assert defined_execution_error.description == "Common base class for all non-exit exceptions."

    # Defines an error with exception instance.
    def test_define_error_with_instance(self):
        exception = RuntimeError()

        defined_execution_error = define_error(exception)

        assert issubclass(defined_execution_error, DefinedExecutionError)
        assert defined_execution_error.identifier == "RuntimeError"
        assert defined_execution_error.display_name == "Runtime Error"
        assert defined_execution_error.description == "Unspecified run-time error."

    # Defines an error with exception instance.
    def test_define_error_with_message(self):
        exception = ValueError("Hello, World!")

        defined_execution_error = define_error(exception)

        assert issubclass(defined_execution_error, DefinedExecutionError)
        assert defined_execution_error.identifier == "ValueError"
        assert defined_execution_error.display_name == "Value Error"
        assert defined_execution_error.description == "Inappropriate argument value (of correct type)."
