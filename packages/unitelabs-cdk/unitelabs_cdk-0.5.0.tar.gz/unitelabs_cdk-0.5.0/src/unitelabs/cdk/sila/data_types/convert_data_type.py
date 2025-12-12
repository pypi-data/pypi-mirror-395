import sila.datetime

import sila
from sila import (
    Element,
    Native,
)


def to_sila(value: Native, responses: dict[str, Element]) -> sila.Native:
    """
    Convert a (intermediate) command response to a SiLA native value.

    Args:
      value: The command responses value to convert.
      responses: The SiLA data type of the message.

    Returns:
      The converted SiLA native value.
    """

    if not isinstance(value, (tuple, dict)):
        if keys := responses.keys():
            identifier = next(iter(keys))
            value = {identifier: value}
        else:
            value = {}

    if isinstance(value, tuple):
        values = {}
        for index, name in enumerate(responses.keys()):
            if index >= len(value):
                msg = f"Expected {len(responses)} elements in tuple, received {value}."
                raise ValueError(msg)
            values[name] = value[index]

        value = values

    return value
