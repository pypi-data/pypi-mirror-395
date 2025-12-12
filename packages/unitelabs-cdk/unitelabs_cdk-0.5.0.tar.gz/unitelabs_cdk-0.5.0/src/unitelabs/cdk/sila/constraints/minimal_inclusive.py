import dataclasses
import datetime
import typing

from sila.framework.constraints import MinimalInclusive as SiLAMinimalInclusive
from sila.framework.data_types import Date, Integer, Real, Time, Timestamp


@dataclasses.dataclass
class MinimalInclusive(SiLAMinimalInclusive):
    """A constraint that enforces a lower inclusive bound on a value."""

    value: typing.Union[int, float, datetime.date, datetime.time, datetime.datetime]

    def __post_init__(self):
        if isinstance(self.value, int):
            self.value = Integer(self.value)
        elif isinstance(self.value, float):
            self.value = Real(self.value)
        elif isinstance(self.value, datetime.datetime):
            self.value = Timestamp.from_datetime(self.value)
        elif isinstance(self.value, datetime.date):
            self.value = Date.from_date(self.value)
        elif isinstance(self.value, datetime.time):
            self.value = Time.from_time(self.value)

        else:
            msg = (
                "Expected type of str, int, float, datetime.date, datetime.time, datetime.datetime, "
                f"Instead received type '{type(self.value)}'."
            )
            raise TypeError(msg)
