import datetime

from unitelabs.cdk import sila


class GreetingProvider(sila.Feature):
    """
    Example implementation of a minimum Feature.

    Provides a Greeting to the Client and a StartYear property, informing about the year the Server has been started.
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="examples",
            version="1.0",
            maturity_level="Verified",
        )

        self._start_year = datetime.datetime.now().year

    @sila.UnobservableCommand()
    async def say_hello(self, name: str) -> str:
        """
        Say "Hello SiLA 2 + [Name]" to the client.

        Args:
          name: The name, SayHello shall use to greet

        Returns:
          Greeting: The greeting string, returned to the SiLA Client.
        """

        return f"Hello SiLA 2 {name}"

    @sila.UnobservableProperty()
    async def start_year(self) -> int:
        """Get the year the SiLA Server has been started in."""

        return self._start_year
