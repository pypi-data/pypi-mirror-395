from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.core import QtfSeries, Triplet


class BackgroundEngineFixed(BackgroundEngine):
    """ Represent a fixed background.

    Will always return the background values passed to the __init__
    """
    def __init__(self, background: tuple[float, float, float]) -> None:
        """ Constructor

        Args:
            background (tuple[float, float, float]): BAckground to fix
        """
        super().__init__()
        self.background = background

    @property
    def mode(self) -> BackgroundMode:
        """ Get the BackgroundMode associated with the class
        """
        return BackgroundMode.FIXED

    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a whole series as an input

        Return the fixed background

        Args:
            series (QtfSeries): series to use to compute the background

        Returns:
            tuple[float, float, float] | None: The fixed background
        """
        return self.background

    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as an input

        Return the fixed background

        Args:
            triplet (Triplet): Triplet to use to compute the background

        Returns:
            tuple[float, float, float] | None: The fixed background
        """
        return self.background

    def __eq__(self, other):
        """ Overrides the default __eq__ implementation """
        if isinstance(other, BackgroundEngineFixed):
            return self.background == other.background
        return False
