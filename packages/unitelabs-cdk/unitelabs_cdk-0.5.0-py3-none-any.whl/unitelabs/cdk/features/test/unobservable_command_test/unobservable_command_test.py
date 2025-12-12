# ruff: noqa: D205, D401, D415

from unitelabs.cdk import sila


class UnobservableCommandTest(sila.Feature):
    """Feature for testing unobservable commands"""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.UnobservableCommand()
    def command_without_parameters_and_responses(self) -> None:
        """A command that takes no parameters and returns no responses"""

    @sila.UnobservableCommand()
    def convert_integer_to_string(self, integer: int) -> str:
        """
        A command that takes one integer parameter and returns its string representation.

        Args:
          Integer: An integer, e.g. 12345

        Returns:
          StringRepresentation: The string representation of the given integer, e.g. '12345'
        """

        return str(integer)

    @sila.UnobservableCommand()
    def join_integer_and_string(self, integer: int, string: str) -> str:
        """
        A command which takes an integer and a string parameter and returns a string with both joined (e.g.
        "123abc")

        Args:
          Integer: An integer, e.g. 123
          String: A string, e.g. 'abc'

        Returns:
          JoinedParameters: Both parameters joined as string (e.g. '123abc')
        """

        return f"{integer}{string}"

    @sila.UnobservableCommand()
    def split_string_after_first_character(self, string: str) -> tuple[str, str]:
        """
        A command which splits a given string after its first character. Returns empty parts if the input was
        too short.

        Args:
          String: A string, e.g. 'abcde'

        Returns:
          FirstCharacter: The first character, e.g. 'a', or an empty string if the input was empty
          Remainder: The remainder, e.g. 'bcde', or an empty string if the input was shorter that two characters
        """

        return string[:1], string[1:]
