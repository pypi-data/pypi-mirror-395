# ruff: noqa: D401

import time

from unitelabs.cdk import sila


class UnobservablePropertyTest(sila.Feature):
    """This feature tests a static and a dynamic unobservable property."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.UnobservableProperty()
    def get_answer_to_everything(self) -> int:
        """Returns the answer to the ultimate question of life, the universe, and everything. 42."""

        return 42

    @sila.UnobservableProperty()
    def get_seconds_since_1970(self) -> int:
        """Returns the unix timestamp: The time in seconds since January 1st of 1970."""

        return round(time.time())
