# ruff: noqa: D205, D401, D415, E501

import dataclasses

from unitelabs.cdk import sila


@dataclasses.dataclass
class TestStructure(sila.CustomDataType):
    """
    An example Structure data type containing all SiLA basic types.

    Attributes:
      StringTypeValue: A value of SiLA data type String.
      IntegerTypeValue: A value of SiLA data type Integer.
      RealTypeValue: A value of SiLA data type Real.
      BooleanTypeValue: A value of SiLA data type Boolean.
      BinaryTypeValue: A value of SiLA data type Binary.
      DateTypeValue: A value of SiLA data type Date.
      TimeTypeValue: A value of SiLA data type Time.
      TimestampTypeValue: A value of SiLA data type Timestamp
      AnyTypeValue: A value of SiLA data type Any.
    """

    string_type_value: str
    integer_type_value: int
    real_type_value: float
    boolean_type_value: bool
    binary_type_value: bytes
    date_type_value: sila.datetime.date
    time_type_value: sila.datetime.time
    timestamp_type_value: sila.datetime.datetime
    any_type_value: sila.Any


class ListDataTypeTest(sila.Feature):
    """Provides commands and properties to set or respectively get SiLA List Data Type values via command parameters or property responses respectively."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.UnobservableProperty()
    def empty_string_list(self) -> list[str]:
        """Returns an empty list of String type."""

        return []

    @sila.UnobservableCommand()
    def echo_string_list(self, string_list: list[str]) -> list[str]:
        """
        Receives a list of string values and returns a list containing the string values that have been received.

        Args:
          StringList: The list of string values to be returned.

        Returns:
          ReceivedValues: A list containing the string values that have been received.
        """

        return string_list

    @sila.UnobservableProperty()
    def string_list(self) -> list[str]:
        """Returns a list with the following string values: 'SiLA 2', 'is', 'great'."""

        return ["SiLA 2", "is", "great"]

    @sila.UnobservableCommand()
    def echo_integer_list(self, integer_list: list[int]) -> list[int]:
        """
        Receives a list of integer values and returns a list containing the integer values that have been received.

        Args:
          IntegerList: The list of integer values to be returned.

        Returns:
          ReceivedValues: A list containing the integer values that have been received.
        """

        return integer_list

    @sila.UnobservableProperty()
    def integer_list(self) -> list[int]:
        """Returns a list with the following Integer values: 1, 2, 3."""

        return [1, 2, 3]

    @sila.UnobservableCommand()
    def echo_structure_list(self, structure_list: list[TestStructure]) -> list[TestStructure]:
        """
        Receives a list of structure values and returns a list containing the structures that have been received.

        Args:
          StructureList: The list of structure values to be returned.

        Returns:
          ReceivedValues: A message containing the content of all structures that have been received.
        """

        return structure_list

    @sila.UnobservableProperty()
    def structure_list(self) -> list[TestStructure]:
        """
        Returns a list with 3 structure values, whereas the values of the first element are:
        string value = 'SiLA2_Test_String_Value_1'
        integer value = 5124
        real value = 3.1415926
        boolean value = true
        binary value (embedded string) = 'Binary_String_Value_1'
        date value = 05.08.2022 respective 08/05/2022
        time value = 12:34:56.789
        time stamp value = 2022-08-05 12:34:56.789
        any type value (string) = 'Any_Type_String_Value_1'

        For the second and third element:
        the last character of the strings changes to '2' respective '3'
        the numeric values are incremented by 1
        the boolean values becomes false for element 2 and true for element 3
        for the date value day, month and year are incremented by 1
        for the time value milliseconds, seconds, minutes and hours are incremented by 1
        for the time stamp value day, month, year, milliseconds, seconds, minutes and hours are incremented by 1.
        """

        return [
            TestStructure(
                string_type_value="SiLA2_Test_String_Value_1",
                integer_type_value=5124,
                real_type_value=3.1415926,
                boolean_type_value=True,
                binary_type_value=b"Binary_String_Value_1",
                date_type_value=sila.datetime.date(
                    year=2022, month=8, day=5, tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2))
                ),
                time_type_value=sila.datetime.time(
                    hour=12,
                    minute=34,
                    second=56,
                    microsecond=789000,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                timestamp_type_value=sila.datetime.datetime(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=34,
                    second=56,
                    microsecond=789000,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                any_type_value="Any_Type_String_Value_1",
            ),
            TestStructure(
                string_type_value="SiLA2_Test_String_Value_2",
                integer_type_value=5125,
                real_type_value=4.1415926,
                boolean_type_value=False,
                binary_type_value=b"Binary_String_Value_2",
                date_type_value=sila.datetime.date(
                    year=2023, month=9, day=6, tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2))
                ),
                time_type_value=sila.datetime.time(
                    hour=13,
                    minute=35,
                    second=57,
                    microsecond=790000,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                timestamp_type_value=sila.datetime.datetime(
                    year=2023,
                    month=9,
                    day=6,
                    hour=13,
                    minute=35,
                    second=57,
                    microsecond=790000,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                any_type_value="Any_Type_String_Value_2",
            ),
            TestStructure(
                string_type_value="SiLA2_Test_String_Value_3",
                integer_type_value=5126,
                real_type_value=5.1415926,
                boolean_type_value=True,
                binary_type_value=b"Binary_String_Value_3",
                date_type_value=sila.datetime.date(
                    year=2024,
                    month=10,
                    day=7,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                time_type_value=sila.datetime.time(
                    hour=14,
                    minute=36,
                    second=58,
                    microsecond=791000,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                timestamp_type_value=sila.datetime.datetime(
                    year=2024,
                    month=10,
                    day=7,
                    hour=14,
                    minute=36,
                    second=58,
                    microsecond=791000,
                    tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
                ),
                any_type_value="Any_Type_String_Value_3",
            ),
        ]
