import dataclasses

from sila import Integer, List, Real, String
from unitelabs.cdk.sila.common.feature import Feature
from unitelabs.cdk.sila.data_types.custom_data_type import CustomDataType


class TestFromNative:
    async def test_should_parse_basic_from_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: str

        feature = Feature()
        data_type = TestCustomDataType.attach(feature)

        # Convert from native
        value = await data_type.from_native(feature.context, "Hello, World!")

        # Assert that the method returns the correct value
        assert value == data_type(value=String(value="Hello, World!"))

    async def test_should_parse_basic_from_custom_data_type(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: str

        feature = Feature()
        data_type = TestCustomDataType.attach(feature)
        native = TestCustomDataType(test_custom_data_type="Hello, World!")

        # Convert from native
        value = await data_type.from_native(feature.context, native)

        # Assert that the method returns the correct value
        assert value == data_type(value=String(value="Hello, World!"))

    async def test_should_parse_structure_from_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: int
            another_value: list[float]

        feature = Feature()
        data_type = TestCustomDataType.attach(feature)

        # Convert from native
        value = await data_type.from_native(feature.context, {"value": 42, "another_value": [1.1, 2.2, 3.3]})

        # Assert that the method returns the correct value
        assert value == data_type(
            data_type.data_type(
                {
                    "value": Integer(value=42),
                    "another_value": List.create(Real)(value=[Real(value=1.1), Real(value=2.2), Real(value=3.3)]),
                }
            )
        )

    async def test_should_parse_structure_from_custom_data_type(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: int
            another_value: list[float]

        feature = Feature()
        data_type = TestCustomDataType.attach(feature)
        native = TestCustomDataType(value=42, another_value=[1.1, 2.2, 3.3])

        # Convert from native
        value = await data_type.from_native(feature.context, native)

        # Assert that the method returns the correct value
        assert value == data_type(
            data_type.data_type(
                {
                    "value": Integer(value=42),
                    "another_value": List.create(Real)(value=[Real(value=1.1), Real(value=2.2), Real(value=3.3)]),
                }
            )
        )


class TestToNative:
    async def test_should_parse_basic(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            test_custom_data_type: str

        feature = Feature()
        data_type = TestCustomDataType.attach(feature)
        value = await data_type.from_native(feature.context, "Hello, World!")

        # Convert to native
        native = await value.to_native(feature.context)

        # Assert that the method returns the correct value
        assert isinstance(native, TestCustomDataType)
        assert native.test_custom_data_type == "Hello, World!"

    async def test_should_parse_structure(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestCustomDataType(CustomDataType):
            value: int
            another_value: list[float]

        feature = Feature()
        data_type = TestCustomDataType.attach(feature)
        value = await data_type.from_native(feature.context, {"value": 42, "another_value": [1.1, 2.2, 3.3]})

        # Convert to native
        native = await value.to_native(feature.context)

        # Assert that the method returns the correct value
        assert isinstance(native, TestCustomDataType)
        assert native.value == 42
        assert native.another_value == [1.1, 2.2, 3.3]
