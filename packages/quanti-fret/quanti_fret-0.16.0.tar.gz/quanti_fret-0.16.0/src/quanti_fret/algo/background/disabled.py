from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode

from quanti_fret.core import QtfSeries, Triplet


class BackgroundEngineDisabled(BackgroundEngine):
    """ The ``BackgroundEngineDisabled`` disables the computation of a
    background.

    It always returns ``None`` when computing a background.
    """

    @property
    def mode(self) -> BackgroundMode:
        return BackgroundMode.DISABLED

    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a series as input.

        Does nothing, just returns None.

        Args:
            series (QtfSeries): Series to use to compute the background.

        Returns:
            tuple[float, float, float] | None: Always returns None.
        """
        return None

    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as input.

        Does nothing, just returns None.

        Args:
            triplet (Triplet): Triplet to use to compute the background.

        Returns:
            tuple[float, float, float]: Always returns None.
        """
        return None

    def __eq__(self, other):
        """ Two ``BackgroundEngineDisabled`` are always equals """
        if isinstance(other, BackgroundEngineDisabled):
            return True
        return False
