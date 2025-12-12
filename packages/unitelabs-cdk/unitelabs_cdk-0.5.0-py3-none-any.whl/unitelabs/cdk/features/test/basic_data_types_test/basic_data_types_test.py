# ruff: noqa: D401, E501

from unitelabs.cdk import sila


class BasicDataTypesTest(sila.Feature):
    """Provides commands and properties to set or respectively get all SiLA Basic Data Types via command parameters or property responses respectively."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    # Data type String

    @sila.UnobservableCommand()
    def echo_string_value(self, string_value: str) -> str:
        """
        Receives a String value and returns the String value that has been received.

        Args:
          StringValue: The String value to be returned.

        Returns:
          ReceivedValue: The String value that has been received.
        """

        return string_value

    @sila.UnobservableProperty()
    def get_string_value(self) -> str:
        """Returns the String value 'SiLA2_Test_String_Value'."""

        return "SiLA2_Test_String_Value"

    # Data type Integer

    @sila.UnobservableCommand()
    def echo_integer_value(self, integer_value: int) -> int:
        """
        Receives an Integer value and returns the Integer value that has been received.

        Args:
          IntegerValue: The Integer value to be returned.

        Returns:
          ReceivedValue: The Integer value that has been received.
        """

        return integer_value

    @sila.UnobservableProperty()
    def get_integer_value(self) -> int:
        """Returns the Integer value 5124."""

        return 5124

    # Data type Real

    @sila.UnobservableCommand()
    def echo_real_value(self, real_value: float) -> float:
        """
        Receives a Real value and returns the Real value that has been received.

        Args:
          RealValue: The Real value to be returned.

        Returns:
          ReceivedValue: The Real value that has been received.
        """

        return real_value

    @sila.UnobservableProperty()
    def get_real_value(self) -> float:
        """Returns the Real value 3.1415926."""

        return 3.1415926

    # Data type Boolean

    @sila.UnobservableCommand()
    def echo_boolean_value(self, boolean_value: bool) -> bool:
        """
        Receives a Boolean value and returns the Boolean value that has been received.

        Args:
          BooleanValue: The Boolean value to be returned.

        Returns:
          ReceivedValue: The Boolean value that has been received.
        """

        return boolean_value

    @sila.UnobservableProperty()
    def get_boolean_value(self) -> bool:
        """Returns the Boolean value true."""

        return True

    # Data type Date

    @sila.UnobservableCommand()
    def echo_date_value(self, date_value: sila.datetime.date) -> sila.datetime.date:
        """
        Receives a Date value and returns the Date value that has been received.

        Args:
          DateValue: The Date value to be returned.

        Returns:
          ReceivedValue: The Date value that has been received.
        """

        return date_value

    @sila.UnobservableProperty()
    def get_date_value(self) -> sila.datetime.date:
        """Returns the Date value 05.08.2022 respective 08/05/2018, timezone +2."""

        return sila.datetime.date(
            year=2022, month=8, day=5, tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2))
        )

    # Data type Time

    @sila.UnobservableCommand()
    def echo_time_value(self, time_value: sila.datetime.time) -> sila.datetime.time:
        """
        Receives a Time value and returns the Time value that has been received.

        Args:
          TimeValue: The Time value to be returned.

        Returns:
          ReceivedValue: The Time value that has been received.
        """

        return time_value

    @sila.UnobservableProperty()
    def get_time_value(self) -> sila.datetime.time:
        """Returns the Time value 12:34:56.789, timezone +2."""

        return sila.datetime.time(
            hour=12,
            minute=34,
            second=56,
            microsecond=789000,
            tzinfo=sila.datetime.timezone(offset=sila.datetime.timedelta(hours=+2)),
        )

    # Data type Timestamp

    @sila.UnobservableCommand()
    def echo_timestamp_value(self, timestamp_value: sila.datetime.datetime) -> sila.datetime.datetime:
        """
        Receives a Timestamp value and returns a message containing the Timestamp value that has been received.

        Args:
          TimestampValue: The Timestamp value to be returned.

        Returns:
          ReceivedValue: The Timestamp value that has been received.
        """

        return timestamp_value

    @sila.UnobservableProperty()
    def get_timestamp_value(self) -> sila.datetime.datetime:
        """Returns the Timestamp value 2022-08-05 12:34:56.789, timezone +2."""

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
