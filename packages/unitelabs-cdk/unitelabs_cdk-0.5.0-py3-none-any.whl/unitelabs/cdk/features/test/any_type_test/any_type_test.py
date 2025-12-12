# ruff: noqa: D205, D401, D415, E501

import typing_extensions as typing

from sila import Serializer
from unitelabs.cdk import sila


class AnyTypeTest(sila.Feature):
    """Provides commands and properties to set or respectively get SiLA Any Type values via command parameters or property responses respectively."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.UnobservableCommand()
    async def set_any_type_value(
        self, any_type_value: sila.Any
    ) -> tuple[
        typing.Annotated[
            str,
            sila.constraints.Schema(
                "Xml",
                url="https://gitlab.com/SiLA2/sila_base/-/raw/beb5d703ab62b1242695f3a591f04a07ebc7b528/schema/AnyTypeDataType.xsd",
            ),
        ],
        sila.Any,
    ]:
        """
        Receives an Any type value and returns the type and the value that has been received.

        Args:
          AnyTypeValue: The Any type value to be set.

        Returns:
          ReceivedAnyType: The type that has been received.
          ReceivedValue: The value that has been received.
        """

        if isinstance(any_type_value, dict):
            Structure = sila.data_types.Structure.create(
                {
                    "StringTypeValue": sila.data_types.Element(
                        identifier="StringTypeValue",
                        display_name="StringTypeValue",
                        description="Astringvalue.",
                        data_type=sila.data_types.String,
                    ),
                    "IntegerTypeValue": sila.data_types.Element(
                        identifier="IntegerTypeValue",
                        display_name="IntegerTypeValue",
                        description="Anintegervalue.",
                        data_type=sila.data_types.Integer,
                    ),
                    "DateTypeValue": sila.data_types.Element(
                        identifier="DateTypeValue",
                        display_name="DateTypeValue",
                        description="Adatevalue.",
                        data_type=sila.data_types.Date,
                    ),
                }
            )

            return Serializer.serialize(Structure.serialize, remove_whitespace=True), await Structure.from_native(
                self.context,
                {
                    "StringTypeValue": "A String value",
                    "IntegerTypeValue": 83737665,
                    "DateTypeValue": sila.datetime.date(
                        year=2022,
                        month=8,
                        day=5,
                        tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                    ),
                },
            )

        data_type = await sila.data_types.AnyType.from_native(self.context, any_type_value)

        return data_type.schema, any_type_value

    @sila.UnobservableProperty()
    def get_any_type_string_value(self) -> sila.Any:
        """Returns the Any type String value 'SiLA_Any_type_of_String_type'."""

        return "SiLA_Any_type_of_String_type"

    @sila.UnobservableProperty()
    def get_any_type_integer_value(self) -> sila.Any:
        """Returns the Any type Integer value 5124."""

        return 5124

    @sila.UnobservableProperty()
    def get_any_type_real_value(self) -> sila.Any:
        """Returns an Any type Real value 3.1415926."""

        return 3.1415926

    @sila.UnobservableProperty()
    def get_any_type_boolean_value(self) -> sila.Any:
        """Returns the Any type Boolean value true."""

        return True

    @sila.UnobservableProperty()
    def any_type_binary_value(self) -> sila.Any:
        """Returns the Any type ASCII-encoded string value 'SiLA_Any_type_of_Binary_type' as Binary."""

        return b"SiLA_Any_type_of_Binary_type"

    @sila.UnobservableProperty()
    def get_any_type_date_value(self) -> sila.Any:
        """Returns the Any type Date value 05.08.2022 respective 08/05/2022, timezone +2."""

        return sila.datetime.date(
            year=2022, month=8, day=5, tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2))
        )

    @sila.UnobservableProperty()
    def get_any_type_time_value(self) -> sila.Any:
        """Returns the Any type Time value 12:34:56.789, timezone +2."""

        return sila.datetime.time(
            hour=12,
            minute=34,
            second=56,
            microsecond=789000,
            tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
        )

    @sila.UnobservableProperty()
    def get_any_type_timestamp_value(self) -> sila.Any:
        """Returns the Any type Timestamp value 2022-08-05 12:34:56.789, timezone +2."""

        return sila.datetime.datetime(
            year=2022,
            month=8,
            day=5,
            hour=12,
            minute=34,
            second=56,
            microsecond=789000,
            tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
        )

    @sila.UnobservableProperty()
    def any_type_list_value(self) -> sila.Any:
        """Returns the Any type String List value ('SiLA 2', 'Any', 'Type', 'String', 'List')"""

        return ["SiLA 2", "Any", "Type", "String", "List"]

    @sila.UnobservableProperty()
    async def any_type_structure_value(self) -> sila.Any:
        """
        Returns the following Any type Structure value:
        - String 'StringTypeValue' = 'A String value',
        - Integer 'IntegerTypeValue' = 83737665,
        - Date 'DateTypeValue' = 05.08.2022 respective 08/05/2022 timezone +2 )
        """

        Structure = sila.data_types.Structure.create(
            {
                "StringTypeValue": sila.data_types.Element(
                    identifier="StringTypeValue",
                    display_name="StringTypeValue",
                    description="Astringvalue.",
                    data_type=sila.data_types.String,
                ),
                "IntegerTypeValue": sila.data_types.Element(
                    identifier="IntegerTypeValue",
                    display_name="IntegerTypeValue",
                    description="Anintegervalue.",
                    data_type=sila.data_types.Integer,
                ),
                "DateTypeValue": sila.data_types.Element(
                    identifier="DateTypeValue",
                    display_name="DateTypeValue",
                    description="Adatevalue.",
                    data_type=sila.data_types.Date,
                ),
            }
        )

        return await Structure.from_native(
            self.context,
            {
                "StringTypeValue": "A String value",
                "IntegerTypeValue": 83737665,
                "DateTypeValue": sila.datetime.date(
                    year=2022, month=8, day=5, tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2))
                ),
            },
        )
