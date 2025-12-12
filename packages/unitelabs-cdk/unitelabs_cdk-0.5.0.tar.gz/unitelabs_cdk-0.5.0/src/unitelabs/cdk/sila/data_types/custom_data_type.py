import dataclasses

import typing_extensions as typing

from ..common import Dataclass, Feature
from .custom import Custom


@dataclasses.dataclass
class CustomDataType(Dataclass):
    """
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
      ...     print(my_custom_data.param_a, my_custom_data.param_b)
    """

    @typing.override
    @classmethod
    def attach(cls, feature: Feature) -> type[Custom]:
        super().attach(feature)

        if cls._identifier in feature.data_type_definitions:
            return feature.data_type_definitions[cls._identifier]

        data_type = cls._infer_data_type(feature)
        cls._custom = Custom.create(
            identifier=cls._identifier,
            display_name=cls._name,
            description=cls._description,
            data_type=data_type,
            feature=feature,
        )
        cls._custom._class = cls

        return cls._custom
