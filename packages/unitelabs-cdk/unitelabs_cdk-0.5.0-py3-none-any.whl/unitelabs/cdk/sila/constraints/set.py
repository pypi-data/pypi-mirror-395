import collections.abc
import dataclasses
import datetime
import typing

from sila.framework.constraints import Set as SiLASet
from sila.framework.data_types import Date, Integer, Real, String, Time, Timestamp


@dataclasses.dataclass
class Set(SiLASet):
    """
    A constraint that enforces that a value is part of a defined set of values.

    Raises:
      ValueError: If the list of allowed values is empty.
    """

    values: collections.abc.Sequence[typing.Union[str, int, float, datetime.date, datetime.time, datetime.datetime]]

    def __post_init__(self):
        values_type = type(self.values[0]) if self.values else None

        if values_type is str:
            self.values = [String(value) for value in self.values]
        elif values_type is int:
            self.values = [Integer(value) for value in self.values]
        elif values_type is float:
            self.values = [Real(value) for value in self.values]
        elif values_type is datetime.datetime:
            self.values = [Timestamp.from_datetime(value) for value in self.values]
        elif values_type is datetime.date:
            self.values = [Date.from_date(value) for value in self.values]
        elif values_type is datetime.time:
            self.values = [Time.from_time(value) for value in self.values]
        else:
            msg = (
                "Expected type of str, int, float, datetime.date, datetime.time, datetime.datetime, "
                f"Instead received type '{values_type}'."
            )
            raise TypeError(msg)
        return super().__post_init__()
