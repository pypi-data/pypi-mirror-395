from enum import Enum


class BackgroundMode(Enum):
    """ Describes how the background is computed.
    """

    DISABLED = 0
    """No background is computed."""

    MASK = 1
    """Background is computed using the triplet's background masks."""

    PERCENTILE = 2
    """Background is computed using triplet's low pixels."""

    FIXED = 3
    """Background has always the same value."""

    __order__ = 'DISABLED MASK PERCENTILE FIXED'

    def __str__(self) -> str:
        return self.name.capitalize()
