import dataclasses
import unittest.mock

import pytest

import sila
from unitelabs.cdk.sila.command.intermediate import Intermediate
from unitelabs.cdk.sila.command.status import Status
from unitelabs.cdk.sila.data_types.any import Any
from unitelabs.cdk.sila.utils.docstring import Docstring, parse_docstring


class TestGoogleStyle:
    def test_should_parse_function_docstring(self):
        # Create function
        def test_function(
            param_a: str, param_b: int, *, status: Status, intermediate: Intermediate[tuple[bytes, int]]
        ) -> tuple[bool, float]:
            """
            Some short introduction.

            With more details later on.

            Examples:
              Example on how to use the function:
              >>> for i in test_function("a", 1):
              ...     print(i)
              True
              1.23

            Args:
              ParamA: The first parameter.
              DifferentB: The second parameter.

            Yields:
              InterResponseA: The first intermediate response.
              InterResponseB: The second intermediate response.

            Returns:
              ResponseA: The first response.
              ResponseB: The second response.

            Raises:
              RuntimeError: If the matrix is not numerically invertible.
            """

            return True, 1.23

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description=(
                "Some short introduction.\n\nWith more details later on.\n\nExample on how to use the function:\n"
                '>>> for i in test_function("a", 1):\n...     print(i)\nTrue\n1.23\n'
            ),
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The first parameter.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="DifferentB",
                    display_name="Different B",
                    description="The second parameter.",
                    data_type=sila.Integer,
                ),
            },
            yields={
                "inter_response_a": sila.Element(
                    identifier="InterResponseA",
                    display_name="Inter Response A",
                    description="The first intermediate response.",
                    data_type=sila.Binary,
                ),
                "inter_response_b": sila.Element(
                    identifier="InterResponseB",
                    display_name="Inter Response B",
                    description="The second intermediate response.",
                    data_type=sila.Integer,
                ),
            },
            returns={
                "response_a": sila.Element(
                    identifier="ResponseA",
                    display_name="Response A",
                    description="The first response.",
                    data_type=sila.Boolean,
                ),
                "response_b": sila.Element(
                    identifier="ResponseB",
                    display_name="Response B",
                    description="The second response.",
                    data_type=sila.Real,
                ),
            },
            raises={
                "runtime_error": docstring.raises["runtime_error"],
            },
        )

        assert issubclass(docstring.raises["runtime_error"], sila.DefinedExecutionError)
        assert docstring.raises["runtime_error"].identifier == "RuntimeError"
        assert docstring.raises["runtime_error"].display_name == "Runtime Error"
        assert docstring.raises["runtime_error"].description == "If the matrix is not numerically invertible."

    def test_should_parse_class_docstring(self):
        # Create class
        class TestClass:
            """
            Some short introduction.

            With more details later on.

            Examples:
              Example on how to use the class:
              >>> test_class = TestClass("a", 1)
              ... print(test_class.param_a)
              a

            Attributes:
              ParamA: The first value.
              ParamB: The second value.
            """

            param_a: str
            param_b: int

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(TestClass, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description=(
                "Some short introduction.\n\nWith more details later on.\n\nExample on how to use the class:\n"
                '>>> test_class = TestClass("a", 1)\n... print(test_class.param_a)\na\n'
            ),
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The first value.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="ParamB",
                    display_name="Param B",
                    description="The second value.",
                    data_type=sila.Integer,
                ),
            },
        )

    def test_should_parse_dataclass_docstring(self):
        # Create dataclass
        @dataclasses.dataclass
        class TestClass:
            """
            Some short introduction.

            With more details later on.

            Examples:
              Example on how to use the class:
              >>> test_class = TestClass("a", 1)
              ... print(test_class.param_a)
              a

            Attributes:
              ParamA: The first value.
              ParamB: The second value.
            """

            param_a: str
            param_b: int

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(TestClass, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description=(
                "Some short introduction.\n\nWith more details later on.\n\nExample on how to use the class:\n"
                '>>> test_class = TestClass("a", 1)\n... print(test_class.param_a)\na\n'
            ),
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The first value.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="ParamB",
                    display_name="Param B",
                    description="The second value.",
                    data_type=sila.Integer,
                ),
            },
        )

    def test_should_parse_description(self):
        # Create function
        def test_function() -> None:
            """Test function."""

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(description="Test function.")

    def test_should_parse_multiline_description(self):
        # Create function
        def test_function() -> None:
            """
            Test function.

            With more details later on.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(description="Test function.\n\nWith more details later on.")

    def test_should_parse_missing_parameter(self):
        # Create function
        def test_function(param_a) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            parameters={"param_a": sila.Element(identifier="ParamA", display_name="Param A", data_type=Any)}
        )

    def test_should_parse_no_parameter(self):
        # Create function
        def test_function() -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(parameters={})

    def test_should_parse_one_parameter(self):
        # Create function
        def test_function(param_a: bool) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            parameters={"param_a": sila.Element(identifier="ParamA", display_name="Param A", data_type=sila.Boolean)}
        )

    def test_should_parse_one_parameter_with_description(self):
        # Create function
        def test_function(param_a: bool) -> None:
            """Test function.

            Args:
              ParamA: The parameter.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA", display_name="Param A", description="The parameter.", data_type=sila.Boolean
                )
            },
        )

    def test_should_parse_one_parameter_with_multiline_description(self):
        # Create function
        def test_function(param_a: bool) -> None:
            """Test function.

            Args:
              ParamA: The parameter
                over multiple
                lines.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The parameter\nover multiple\nlines.",
                    data_type=sila.Boolean,
                )
            },
        )

    def test_should_parse_one_parameter_with_annotation(self):
        # Create function
        def test_function(param_a) -> None:
            """Test function.

            Args:
              ParamA (int): The parameter.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA", display_name="Param A", description="The parameter.", data_type=Any
                )
            },
        )

    def test_should_parse_multiple_parameter(self):
        # Create function
        def test_function(param_a: str, param_b: int, param_c: float) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            parameters={
                "param_a": sila.Element(identifier="ParamA", display_name="Param A", data_type=sila.String),
                "param_b": sila.Element(identifier="ParamB", display_name="Param B", data_type=sila.Integer),
                "param_c": sila.Element(identifier="ParamC", display_name="Param C", data_type=sila.Real),
            }
        )

    def test_should_parse_multiple_parameter_with_description(self):
        # Create function
        def test_function(param_a: str, param_b: int, param_c: float) -> None:
            """Test function.

            Args:
              ParamA: The string parameter.
              ParamB: The integer parameter.
              ParamC: The float parameter.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The string parameter.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="ParamB",
                    display_name="Param B",
                    description="The integer parameter.",
                    data_type=sila.Integer,
                ),
                "param_c": sila.Element(
                    identifier="ParamC", display_name="Param C", description="The float parameter.", data_type=sila.Real
                ),
            },
        )

    def test_should_parse_multiple_parameter_with_annotation(self):
        # Create function
        def test_function(param_a: str, param_b, param_c: float) -> None:
            """Test function.

            Args:
              ParamA (bool): The string parameter.
              ParamB (bool): The integer parameter.
              ParamC: The float parameter.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The string parameter.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="ParamB",
                    display_name="Param B",
                    description="The integer parameter.",
                    data_type=Any,
                ),
                "param_c": sila.Element(
                    identifier="ParamC", display_name="Param C", description="The float parameter.", data_type=sila.Real
                ),
            },
        )

    def test_should_skip_missing_parameter_description(self):
        # Create function
        def test_function(param_a: str, param_b: int, param_c: float) -> None:
            """Test function.

            Args:
              ParamA: The string parameter.
              ParamB: The integer parameter.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The string parameter.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="ParamB",
                    display_name="Param B",
                    description="The integer parameter.",
                    data_type=sila.Integer,
                ),
                "param_c": sila.Element(identifier="ParamC", display_name="Param C", data_type=sila.Real),
            },
        )

    def test_should_ignore_untyped_parameter_description(self):
        # Create function
        def test_function(param_a: str, param_b: int, param_c: float) -> None:
            """Test function.

            Args:
              ParamA: The string parameter.
              ParamB: The integer parameter.
              ParamC: The float parameter.
              ParamD: The boolean parameter.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The string parameter.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="ParamB",
                    display_name="Param B",
                    description="The integer parameter.",
                    data_type=sila.Integer,
                ),
                "param_c": sila.Element(
                    identifier="ParamC", display_name="Param C", description="The float parameter.", data_type=sila.Real
                ),
            },
        )

    def test_should_parse_missing_return(self):
        # Create function
        def test_function(): ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            returns={"response_0": sila.Element(identifier="Response0", display_name="Response 0", data_type=Any)}
        )

    def test_should_parse_no_return(self):
        # Create function
        def test_function() -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(returns={})

    def test_should_parse_one_return(self):
        # Create function
        def test_function() -> bool: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            returns={
                "response_0": sila.Element(identifier="Response0", display_name="Response 0", data_type=sila.Boolean)
            }
        )

    def test_should_parse_one_return_with_description(self):
        # Create function
        def test_function() -> bool:
            """Test function.

            Returns:
              The response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_0": sila.Element(
                    identifier="Response0",
                    display_name="Response 0",
                    description="The response.",
                    data_type=sila.Boolean,
                )
            },
        )

    def test_should_parse_one_return_with_multiline_description(self):
        # Create function
        def test_function() -> bool:
            """Test function.

            Returns:
              The response
                over multiple
                lines.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_0": sila.Element(
                    identifier="Response0",
                    display_name="Response 0",
                    description="The response\nover multiple\nlines.",
                    data_type=sila.Boolean,
                )
            },
        )

    def test_should_parse_one_return_with_name(self):
        # Create function
        def test_function() -> bool:
            """Test function.

            Returns:
              Response: The response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response": sila.Element(
                    identifier="Response", display_name="Response", description="The response.", data_type=sila.Boolean
                )
            },
        )

    def test_should_parse_one_return_with_annotation(self):
        # Create function
        def test_function():
            """Test function.

            Returns:
              Response (int): The response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response": sila.Element(
                    identifier="Response",
                    display_name="Response",
                    description="The response.",
                    data_type=Any,
                )
            },
        )

    def test_should_parse_multiple_return(self):
        # Create function
        def test_function() -> tuple[str, int, float]: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            returns={
                "response_0": sila.Element(identifier="Response0", display_name="Response 0", data_type=sila.String),
                "response_1": sila.Element(identifier="Response1", display_name="Response 1", data_type=sila.Integer),
                "response_2": sila.Element(identifier="Response2", display_name="Response 2", data_type=sila.Real),
            }
        )

    def test_should_parse_multiple_return_with_description(self):
        # Create function
        def test_function() -> tuple[str, int, float]:
            """Test function.

            Returns:
              The string response.
              The integer response
                over multiple lines.
              The float response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_0": sila.Element(
                    identifier="Response0",
                    display_name="Response 0",
                    data_type=sila.String,
                    description="The string response.",
                ),
                "response_1": sila.Element(
                    identifier="Response1",
                    display_name="Response 1",
                    data_type=sila.Integer,
                    description="The integer response\nover multiple lines.",
                ),
                "response_2": sila.Element(
                    identifier="Response2",
                    display_name="Response 2",
                    data_type=sila.Real,
                    description="The float response.",
                ),
            },
        )

    def test_should_parse_multiple_return_with_name(self):
        # Create function
        def test_function() -> tuple[str, int, float]:
            """Test function.

            Returns:
              ResponseString: The string response.
              ResponseInt: The integer response
                over multiple lines.
              ResponseFloat: The float response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    description="The string response.",
                    data_type=sila.String,
                ),
                "response_int": sila.Element(
                    identifier="ResponseInt",
                    display_name="Response Int",
                    description="The integer response\nover multiple lines.",
                    data_type=sila.Integer,
                ),
                "response_float": sila.Element(
                    identifier="ResponseFloat",
                    display_name="Response Float",
                    description="The float response.",
                    data_type=sila.Real,
                ),
            },
        )

    def test_should_parse_multiple_return_with_annotation(self):
        # Create function
        def test_function() -> tuple[str, int, float]:
            """Test function.

            Returns:
              ResponseString: The string response.
              ResponseInt (bool): The integer response
                over multiple lines.
              ResponseFloat: The float response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    description="The string response.",
                    data_type=sila.String,
                ),
                "response_int": sila.Element(
                    identifier="ResponseInt",
                    display_name="Response Int",
                    description="The integer response\nover multiple lines.",
                    data_type=sila.Integer,
                ),
                "response_float": sila.Element(
                    identifier="ResponseFloat",
                    display_name="Response Float",
                    description="The float response.",
                    data_type=sila.Real,
                ),
            },
        )

    def test_should_skip_missing_return_description(self):
        # Create function
        def test_function() -> tuple[str, int, float]:
            """Test function.

            Returns:
              ResponseString: The string response.
              The integer response
                over multiple lines.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    description="The string response.",
                    data_type=sila.String,
                ),
                "response_1": sila.Element(
                    identifier="Response1",
                    display_name="Response 1",
                    description="The integer response\nover multiple lines.",
                    data_type=sila.Integer,
                ),
                "response_2": sila.Element(
                    identifier="Response2",
                    display_name="Response 2",
                    data_type=sila.Real,
                ),
            },
        )

    def test_should_ignore_untyped_return_description(self):
        # Create function
        def test_function() -> tuple[str, int, float]:
            """Test function.

            Returns:
              ResponseString: The string response.
              ResponseInt: The integer response
                over multiple lines.
              ResponseFloat: The float response.
              ResponseBoolean: The boolean response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            returns={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    description="The string response.",
                    data_type=sila.String,
                ),
                "response_int": sila.Element(
                    identifier="ResponseInt",
                    display_name="Response Int",
                    description="The integer response\nover multiple lines.",
                    data_type=sila.Integer,
                ),
                "response_float": sila.Element(
                    identifier="ResponseFloat",
                    display_name="Response Float",
                    description="The float response.",
                    data_type=sila.Real,
                ),
            },
        )

    def test_should_parse_missing_yield(self):
        # Create function
        def test_function(intermediate: Intermediate) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            yields={
                "intermediate_response_0": sila.Element(
                    identifier="IntermediateResponse0",
                    display_name="Intermediate Response 0",
                    data_type=Any,
                )
            }
        )

    def test_should_parse_no_yield(self):
        # Create function
        def test_function(intermediate: Intermediate[None]) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(yields={})

    def test_should_parse_one_yield(self):
        # Create function
        def test_function(intermediate: Intermediate[bool]) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            yields={
                "intermediate_response_0": sila.Element(
                    identifier="IntermediateResponse0",
                    display_name="Intermediate Response 0",
                    data_type=sila.Boolean,
                )
            }
        )

    def test_should_parse_one_yield_with_description(self):
        # Create function
        def test_function(intermediate: Intermediate[bool]) -> None:
            """Test function.

            Yields:
              The intermediate response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "intermediate_response_0": sila.Element(
                    identifier="IntermediateResponse0",
                    display_name="Intermediate Response 0",
                    data_type=sila.Boolean,
                    description="The intermediate response.",
                )
            },
        )

    def test_should_parse_one_yield_with_multiline_description(self):
        # Create function
        def test_function(intermediate: Intermediate[bool]) -> None:
            """Test function.

            Yields:
              The intermediate response
                over multiple
                lines.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "intermediate_response_0": sila.Element(
                    identifier="IntermediateResponse0",
                    display_name="Intermediate Response 0",
                    data_type=sila.Boolean,
                    description="The intermediate response\nover multiple\nlines.",
                )
            },
        )

    def test_should_parse_one_yield_with_name(self):
        # Create function
        def test_function(intermediate: Intermediate[bool]) -> None:
            """Test function.

            Yields:
              IntermediateResponse: The intermediate response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "intermediate_response": sila.Element(
                    identifier="IntermediateResponse",
                    display_name="Intermediate Response",
                    data_type=sila.Boolean,
                    description="The intermediate response.",
                )
            },
        )

    def test_should_parse_one_yield_with_annotation(self):
        # Create function
        def test_function(intermediate: Intermediate) -> None:
            """Test function.

            Yields:
              IntermediateResponse (int): The intermediate response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "intermediate_response": sila.Element(
                    identifier="IntermediateResponse",
                    display_name="Intermediate Response",
                    data_type=Any,
                    description="The intermediate response.",
                )
            },
        )

    def test_should_parse_multiple_yields(self):
        # Create function
        def test_function(intermediate: Intermediate[tuple[str, int, float]]) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            yields={
                "intermediate_response_0": sila.Element(
                    identifier="IntermediateResponse0",
                    display_name="Intermediate Response 0",
                    data_type=sila.String,
                ),
                "intermediate_response_1": sila.Element(
                    identifier="IntermediateResponse1",
                    display_name="Intermediate Response 1",
                    data_type=sila.Integer,
                ),
                "intermediate_response_2": sila.Element(
                    identifier="IntermediateResponse2",
                    display_name="Intermediate Response 2",
                    data_type=sila.Real,
                ),
            }
        )

    def test_should_parse_multiple_yield_with_description(self):
        # Create function
        def test_function(intermediate: Intermediate[tuple[str, int, float]]) -> None:
            """Test function.

            Yields:
              The string response.
              The integer response
                over multiple lines.
              The float response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "intermediate_response_0": sila.Element(
                    identifier="IntermediateResponse0",
                    display_name="Intermediate Response 0",
                    data_type=sila.String,
                    description="The string response.",
                ),
                "intermediate_response_1": sila.Element(
                    identifier="IntermediateResponse1",
                    display_name="Intermediate Response 1",
                    data_type=sila.Integer,
                    description="The integer response\nover multiple lines.",
                ),
                "intermediate_response_2": sila.Element(
                    identifier="IntermediateResponse2",
                    display_name="Intermediate Response 2",
                    data_type=sila.Real,
                    description="The float response.",
                ),
            },
        )

    def test_should_parse_multiple_yield_with_name(self):
        # Create function
        def test_function(intermediate: Intermediate[tuple[str, int, float]]) -> None:
            """Test function.

            Yields:
              ResponseString: The string response.
              ResponseInt: The integer response
                over multiple lines.
              ResponseFloat: The float response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    data_type=sila.String,
                    description="The string response.",
                ),
                "response_int": sila.Element(
                    identifier="ResponseInt",
                    display_name="Response Int",
                    data_type=sila.Integer,
                    description="The integer response\nover multiple lines.",
                ),
                "response_float": sila.Element(
                    identifier="ResponseFloat",
                    display_name="Response Float",
                    data_type=sila.Real,
                    description="The float response.",
                ),
            },
        )

    def test_should_parse_multiple_yields_with_annotation(self):
        # Create function
        def test_function(intermediate: Intermediate[tuple[str, int, float]]) -> None:
            """Test function.

            Yields:
              ResponseString: The string response.
              ResponseInt (bool): The integer response
                over multiple lines.
              ResponseFloat: The float response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    description="The string response.",
                    data_type=sila.String,
                ),
                "response_int": sila.Element(
                    identifier="ResponseInt",
                    display_name="Response Int",
                    description="The integer response\nover multiple lines.",
                    data_type=sila.Integer,
                ),
                "response_float": sila.Element(
                    identifier="ResponseFloat",
                    display_name="Response Float",
                    description="The float response.",
                    data_type=sila.Real,
                ),
            },
        )

    def test_should_skip_missing_yield_description(self):
        # Create function
        def test_function(intermediate: Intermediate[tuple[str, int, float]]) -> None:
            """Test function.

            Yields:
              ResponseString: The string response.
              The integer response
                over multiple lines.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    data_type=sila.String,
                    description="The string response.",
                ),
                "intermediate_response_1": sila.Element(
                    identifier="IntermediateResponse1",
                    display_name="Intermediate Response 1",
                    data_type=sila.Integer,
                    description="The integer response\nover multiple lines.",
                ),
                "intermediate_response_2": sila.Element(
                    identifier="IntermediateResponse2",
                    display_name="Intermediate Response 2",
                    data_type=sila.Real,
                ),
            },
        )

    def test_should_ignore_untyped_yield_description(self):
        # Create function
        def test_function(intermediate: Intermediate[tuple[str, int, float]]) -> None:
            """Test function.

            Yields:
              ResponseString: The string response.
              ResponseInt: The integer response
                over multiple lines.
              ResponseFloat: The float response.
              ResponseBoolean: The boolean response.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns(UserWarning):
            docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Test function.",
            yields={
                "response_string": sila.Element(
                    identifier="ResponseString",
                    display_name="Response String",
                    data_type=sila.String,
                    description="The string response.",
                ),
                "response_int": sila.Element(
                    identifier="ResponseInt",
                    display_name="Response Int",
                    data_type=sila.Integer,
                    description="The integer response\nover multiple lines.",
                ),
                "response_float": sila.Element(
                    identifier="ResponseFloat",
                    display_name="Response Float",
                    data_type=sila.Real,
                    description="The float response.",
                ),
            },
        )

    def test_should_ignore_self(self):
        # Create function
        def test_function(self, param_a: str) -> None: ...

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            parameters={"param_a": sila.Element(identifier="ParamA", display_name="Param A", data_type=sila.String)}
        )

    def test_should_keep_casing(self):
        # Create function
        def test_function(uuid: int, prefix_uuid: int, uuid_suffix: int, prefix_uuid_suffix: int) -> None:
            """
            Some short introduction.

            Args:
              UUID: The UUID.
              PrefixUUID: The prefix UUID.
              UUIDSuffix: The UUID suffix.
              PrefixUUIDSuffix: The prefix UUID suffix.
            """

        # Parse docstring
        feature = unittest.mock.Mock()
        docstring = parse_docstring(test_function, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Some short introduction.",
            parameters={
                "uuid": sila.Element(
                    identifier="UUID", display_name="UUID", description="The UUID.", data_type=sila.Integer
                ),
                "prefix_uuid": sila.Element(
                    identifier="PrefixUUID",
                    display_name="Prefix UUID",
                    description="The prefix UUID.",
                    data_type=sila.Integer,
                ),
                "uuid_suffix": sila.Element(
                    identifier="UUIDSuffix",
                    display_name="UUID Suffix",
                    description="The UUID suffix.",
                    data_type=sila.Integer,
                ),
                "prefix_uuid_suffix": sila.Element(
                    identifier="PrefixUUIDSuffix",
                    display_name="Prefix UUID Suffix",
                    description="The prefix UUID suffix.",
                    data_type=sila.Integer,
                ),
            },
        )


class TestRestructured:
    def test_should_parse_docstring(self):
        # Create function
        def test_function(
            param_a: str, param_b: int, *, status: Status, intermediate: Intermediate[tuple[bytes, int]]
        ) -> tuple[bool, float]:
            """
            Some short introduction.

            With more details later on.

            .. parameter:: The first parameter.
            .. parameter:: The second parameter.
              :name: Alternative Parameter
            .. yield:: The first intermediate response.
              :name: Inter Response A
            .. yield:: The second intermediate response.
              :name: Inter Response B
            .. return:: The first response.
              :name: Response A
            .. return:: The second response.
              :name: Response B
            """

            return True, 1.23

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns():
            docstring = parse_docstring(test_function, feature)

        assert docstring == Docstring(
            description="Some short introduction.\n\nWith more details later on.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The first parameter.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="AlternativeParameter",
                    display_name="Alternative Parameter",
                    description="The second parameter.",
                    data_type=sila.Integer,
                ),
            },
            yields={
                "inter_response_a": sila.Element(
                    identifier="InterResponseA",
                    display_name="Inter Response A",
                    description="The first intermediate response.",
                    data_type=sila.Binary,
                ),
                "inter_response_b": sila.Element(
                    identifier="InterResponseB",
                    display_name="Inter Response B",
                    description="The second intermediate response.",
                    data_type=sila.Integer,
                ),
            },
            returns={
                "response_a": sila.Element(
                    identifier="ResponseA",
                    display_name="Response A",
                    description="The first response.",
                    data_type=sila.Boolean,
                ),
                "response_b": sila.Element(
                    identifier="ResponseB",
                    display_name="Response B",
                    description="The second response.",
                    data_type=sila.Real,
                ),
            },
            raises={},
        )

    def test_should_parse_class_docstring(self):
        # Create class
        class TestClass:
            """
            Some short introduction.

            With more details later on.

            .. parameter:: The first value.
            .. parameter:: The second value.
              :name: Alternative Value
            """

            param_a: str
            param_b: int

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns():
            docstring = parse_docstring(TestClass, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Some short introduction.\n\nWith more details later on.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The first value.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="AlternativeValue",
                    display_name="Alternative Value",
                    description="The second value.",
                    data_type=sila.Integer,
                ),
            },
        )

    def test_should_parse_dataclass_docstring(self):
        # Create class
        @dataclasses.dataclass
        class TestClass:
            """
            Some short introduction.

            With more details later on.

            .. parameter:: The first value.
            .. parameter:: The second value.
              :name: Alternative Value
            """

            param_a: str
            param_b: int

        # Parse docstring
        feature = unittest.mock.Mock()
        with pytest.warns():
            docstring = parse_docstring(TestClass, feature)

        # Assert that the method returns the correct value
        assert docstring == Docstring(
            description="Some short introduction.\n\nWith more details later on.",
            parameters={
                "param_a": sila.Element(
                    identifier="ParamA",
                    display_name="Param A",
                    description="The first value.",
                    data_type=sila.String,
                ),
                "param_b": sila.Element(
                    identifier="AlternativeValue",
                    display_name="Alternative Value",
                    description="The second value.",
                    data_type=sila.Integer,
                ),
            },
        )
