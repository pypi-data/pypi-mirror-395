import dataclasses

from sila import Element, Integer, List, Real
from unitelabs.cdk.sila.common.feature import Feature
from unitelabs.cdk.sila.data_types.structure import Structure


class TestFromNative:
    async def test_should_parse_structure_from_native(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestInnerStructure:
            value: int
            another_value: list[float]

        feature = Feature()
        data_type: type[Structure] = Structure.create(
            {
                "value": Element("Value", "Value", "", Integer),
                "another_value": Element("AnotherValue", "Another Value", "", List.create(Real)),
            }
        )
        data_type._class = TestInnerStructure

        # Convert from native
        value = await data_type.from_native(feature.context, {"value": 42, "another_value": [1.1, 2.2, 3.3]})

        # Assert that the method returns the correct value
        assert value == data_type(
            value={
                "value": Integer(value=42),
                "another_value": List.create(Real)(value=[Real(value=1.1), Real(value=2.2), Real(value=3.3)]),
            }
        )

    async def test_should_parse_structure_from_instance(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestInnerStructure:
            value: int
            another_value: list[float]

        feature = Feature()
        data_type: type[Structure] = Structure.create(
            {
                "value": Element("Value", "Value", "", Integer),
                "another_value": Element("AnotherValue", "Another Value", "", List.create(Real)),
            }
        )
        data_type._class = TestInnerStructure

        # Convert from native
        value = await data_type.from_native(
            feature.context, TestInnerStructure(value=42, another_value=[1.1, 2.2, 3.3])
        )

        # Assert that the method returns the correct value
        assert value == data_type(
            value={
                "value": Integer(value=42),
                "another_value": List.create(Real)(value=[Real(value=1.1), Real(value=2.2), Real(value=3.3)]),
            }
        )


class TestToNative:
    async def test_should_parse_structure(self):
        # Create custom data type definition
        @dataclasses.dataclass
        class TestInnerStructure:
            value: int
            another_value: list[float]

        feature = Feature()
        data_type: type[Structure] = Structure.create(
            {
                "value": Element("Value", "Value", "", Integer),
                "another_value": Element("AnotherValue", "Another Value", "", List.create(Real)),
            }
        )
        data_type._class = TestInnerStructure
        value = await data_type.from_native(feature.context, {"value": 42, "another_value": [1.1, 2.2, 3.3]})

        # Convert to native
        native = await value.to_native(feature.context)

        # Assert that the method returns the correct value
        assert isinstance(native, TestInnerStructure)
        assert native.value == 42
        assert native.another_value == [1.1, 2.2, 3.3]
