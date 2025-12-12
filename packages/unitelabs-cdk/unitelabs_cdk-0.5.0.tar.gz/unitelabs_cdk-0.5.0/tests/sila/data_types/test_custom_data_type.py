import dataclasses
import textwrap

import pytest

import sila
from sila import Element, Integer, List, Real, String, Structure
from unitelabs.cdk.sila.command.unobservable_command import UnobservableCommand
from unitelabs.cdk.sila.common.feature import Feature
from unitelabs.cdk.sila.data_types.custom_data_type import CustomDataType
from unitelabs.cdk.sila.property.unobservable_property import UnobservableProperty


class TestInherit:
    async def test_should_subclass_custom_data_type(self):
        # Create custom data type
        class TestCustomDataType(CustomDataType):
            pass

        # Assert that the method returns the correct value
        assert TestCustomDataType._identifier == "TestCustomDataType"
        assert TestCustomDataType._name == "Test Custom Data Type"
        assert TestCustomDataType._description == textwrap.dedent("""\
            A custom data type definition that can be reused in multiple places.

            Examples:
              Define a custom data type:
              >>> @dataclasses.dataclass
              ... class MyCustomDataType(sila.CustomDataType):
              ...   \"\"\"Describe what your data type is for.\"\"\"
              ...   param_a: str
              ...   param_b: int
              ...
              ... class MyFeature(sila.Feature):
              ...   @sila.UnobservableProperty()
              ...   async def my_property(self) -> MyCustomDataType:
              ...     \"\"\"Describe what your property does.\"\"\"
              ...     return MyCustomDataType(param_a="Hello, World!", param_b=42)
              ...
              ...   @sila.UnobservableCommand()
              ...   async def my_property(self, my_custom_data: MyCustomDataType) -> None:
              ...     \"\"\"
              ...     Describe what your command does.
              ...
              ...     Args:
              ...       my_custom_data: The custom data type to process.
              ...     \"\"\"
              ...     print(my_custom_data.param_a, my_custom_data.param_b)""")

    async def test_should_dynamically_create_custom_data_type(self):
        # Create custom data type
        TestCustomDataType: type[CustomDataType] = dataclasses.make_dataclass(
            "TestCustomDataType", (), bases=(CustomDataType,)
        )

        # Assert that the method returns the correct value
        assert TestCustomDataType._identifier == "TestCustomDataType"
        assert TestCustomDataType._name == "Test Custom Data Type"

    async def test_should_infer_description_from_docs(self):
        # Create custom data type
        class TestCustomDataType(CustomDataType):
            """A specific custom data type."""

        # Assert that the method returns the correct value
        assert TestCustomDataType._identifier == "TestCustomDataType"
        assert TestCustomDataType._name == "Test Custom Data Type"
        assert TestCustomDataType._description == "A specific custom data type."


class TestAttach:
    async def test_should_raise_on_missing_fields(self):
        # Create custom data type
        feature = Feature()

        class TestCustomDataType(CustomDataType):
            pass

        # Attach
        with pytest.raises(
            ValueError,
            match=(
                r"Could not detect any fields on 'TestCustomDataType'\. "
                r"Did you forget to annotated your data type definition with `@dataclasses.dataclass`?"
            ),
        ):
            TestCustomDataType.attach(feature)

    async def test_should_add_custom_data_type_to_feature(self):
        # Create custom data type
        feature = Feature()

        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: str

        # Attach
        TestCustomDataType.attach(feature)

        # Assert that the method returns the correct value
        assert feature.data_type_definitions["TestCustomDataType"] == TestCustomDataType._custom

    async def test_should_infer_basic_property(self):
        # Create custom data type
        feature = Feature()

        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: str

        # Attach
        TestCustomDataType.attach(feature)

        # Assert that the method returns the correct value
        assert TestCustomDataType._custom.data_type == String

    async def test_should_infer_list_property(self):
        # Create custom data type
        feature = Feature()

        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: list[float]

        # Attach
        TestCustomDataType.attach(feature)

        # Assert that the method returns the correct value
        assert TestCustomDataType._custom.data_type() == List.create(Real)()

    async def test_should_infer_structure_property(self):
        # Create custom data type
        feature = Feature()

        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: int
            another_value: list[float]

        # Attach
        TestCustomDataType.attach(feature)

        # Assert that the method returns the correct value
        assert (
            TestCustomDataType._custom.data_type()
            == Structure.create(
                {
                    "value": Element(
                        identifier="Value",
                        display_name="Value",
                        data_type=Integer,
                    ),
                    "another_value": Element(
                        identifier="AnotherValue",
                        display_name="Another Value",
                        data_type=List.create(Real),
                    ),
                }
            )()
        )


class TestToNative:
    async def test_should_parse_basic_to_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: str

        # Create unobservable property
        def function() -> TestCustomDataType:
            return TestCustomDataType(test_custom_data_type="Hello, World!")

        server = sila.server.Server()
        feature = Feature()
        unobservable_property = UnobservableProperty()
        unobservable_property(function)
        unobservable_property.attach(feature)
        server.register_feature(feature)

        # Execute unobservable property
        assert isinstance(unobservable_property._handler, sila.UnobservableProperty)
        response = await unobservable_property._handler.read()

        # Assert that the method returns the correct value
        assert response == (await TestCustomDataType._custom.from_native(server, "Hello, World!")).encode(number=1)

    async def test_should_parse_list_to_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: list[float]

        # Create unobservable property
        def function() -> TestCustomDataType:
            return TestCustomDataType(test_custom_data_type=[1.1, 2.2, 3.3])

        server = sila.server.Server()
        feature = Feature()
        unobservable_property = UnobservableProperty()
        unobservable_property(function)
        unobservable_property.attach(feature)
        server.register_feature(feature)

        # Execute unobservable property
        assert isinstance(unobservable_property._handler, sila.UnobservableProperty)
        response = await unobservable_property._handler.read()

        # Assert that the method returns the correct value
        assert response == (await TestCustomDataType._custom.from_native(server, [1.1, 2.2, 3.3])).encode(number=1)

    async def test_should_parse_structure_to_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: int
            another_value: list[float]

        # Create unobservable property
        def function() -> TestCustomDataType:
            return TestCustomDataType(value=42, another_value=[1.1, 2.2, 3.3])

        server = sila.server.Server()
        feature = Feature()
        unobservable_property = UnobservableProperty()
        unobservable_property(function)
        unobservable_property.attach(feature)
        server.register_feature(feature)

        # Execute unobservable property
        assert isinstance(unobservable_property._handler, sila.UnobservableProperty)
        response = await unobservable_property._handler.read()

        # Assert that the method returns the correct value
        assert response == (
            await TestCustomDataType._custom.from_native(server, {"value": 42, "another_value": [1.1, 2.2, 3.3]})
        ).encode(number=1)


class TestFromNative:
    async def test_should_parse_native_to_basic(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: str

        # Create unobservable property
        def function(value: TestCustomDataType) -> None:
            assert value == TestCustomDataType(test_custom_data_type="Hello, World!")

        server = sila.server.Server()
        feature = Feature()
        unobservable_property = UnobservableCommand()
        unobservable_property(function)
        unobservable_property.attach(feature)
        server.register_feature(feature)

        # Execute unobservable property
        assert isinstance(unobservable_property._handler, sila.UnobservableCommand)
        await unobservable_property._handler.execute(
            (await TestCustomDataType._custom.from_native(server, "Hello, World!")).encode(number=1)
        )

    async def test_should_parse_list_to_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: list[float]

        # Create unobservable property
        def function(value: TestCustomDataType) -> None:
            assert value == TestCustomDataType(test_custom_data_type=[1.1, 2.2, 3.3])

        server = sila.server.Server()
        feature = Feature()
        unobservable_property = UnobservableCommand()
        unobservable_property(function)
        unobservable_property.attach(feature)
        server.register_feature(feature)

        # Execute unobservable property
        assert isinstance(unobservable_property._handler, sila.UnobservableCommand)

        await unobservable_property._handler.execute(
            (await TestCustomDataType._custom.from_native(server, [1.1, 2.2, 3.3])).encode(number=1)
        )

    async def test_should_parse_structure_to_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: int
            another_value: list[float]

        # Create unobservable property
        def function(value: TestCustomDataType) -> None:
            assert value == TestCustomDataType(value=42, another_value=[1.1, 2.2, 3.3])

        server = sila.server.Server()
        feature = Feature()
        unobservable_property = UnobservableCommand()
        unobservable_property(function)
        unobservable_property.attach(feature)
        server.register_feature(feature)

        # Execute unobservable property
        assert isinstance(unobservable_property._handler, sila.UnobservableCommand)
        await unobservable_property._handler.execute(
            (
                await TestCustomDataType._custom.from_native(server, {"value": 42, "another_value": [1.1, 2.2, 3.3]})
            ).encode(number=1)
        )
