import re
import unicodedata
import warnings


def to_display_name(value: str, sep: str = "_") -> str:
    """
    Convert a class name to a SiLA display name.

    Example:
      >>> to_display_name("MyClassName")
      "My Class Name"

      >>> to_display_name("my_variable_name")
      "My Variable Name"
    """

    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
    value = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", value)
    value = " ".join(x[0].upper() + x[1:] for x in (value or "").split(sep) if x)

    if len(value) > 255:
        value = value[:255]
        warnings.warn(f"Display '{value}' name is too long and will be truncated.", stacklevel=5)

    return value


def to_identifier(value: str) -> str:
    """
    Convert a SiLA display name to a SiLA identifier.

    Example:
      >>> to_identifier("My Class Name")
      "MyClassName"

      >>> to_identifier("My Variable Name")
      "MyVariableName"
    """

    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]", "", value)

    if not value:
        return ""

    if not value[0].isalpha():
        value = "I" + value

    if not value[0].isupper():
        value = value[0].upper() + value[1:]

    return value
