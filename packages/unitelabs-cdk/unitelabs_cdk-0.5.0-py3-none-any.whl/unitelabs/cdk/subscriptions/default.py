import enum


class Default(enum.Enum):
    """A sentinel value used to indicate that a `Subject`, `Publisher`, or `Subscription` has not been updated yet."""

    token = 0


_DEFAULT_VALUE = Default.token
