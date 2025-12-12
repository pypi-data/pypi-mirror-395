from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode

from quanti_fret.core import QtfSeries, Triplet


class BackgroundEngineDisabled(BackgroundEngine):
    """ Represent a disabled background.

    It just returns None as a background
    """
    @property
    def mode(self) -> BackgroundMode:
        """ Get the BackgroundMode associated with the class
        """
        return BackgroundMode.DISABLED

    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a whole series as an input

        Does nothing, just returns (0., 0., 0.)

        Args:
            series (QtfSeries): series to use to compute the background

        Returns:
            tuple[float, float, float] | None: None
        """
        return None

    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as an input

        Does nothing, just returns None

        Args:
            triplet (Triplet): Triplet to use to compute the background

        Returns:
            tuple[float, float, float]: None
        """
        return None

    def __eq__(self, other):
        """ Overrides the default __eq__ implementation """
        if isinstance(other, BackgroundEngineDisabled):
            return True
        return False
