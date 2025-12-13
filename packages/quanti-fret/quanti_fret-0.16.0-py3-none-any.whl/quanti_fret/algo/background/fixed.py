from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.core import QtfSeries, Triplet


class BackgroundEngineFixed(BackgroundEngine):
    """ The ``BackgroundEngineFixed`` always returns a fixed value when
    computing a background.
    """

    def __init__(self, background: tuple[float, float, float]) -> None:
        """ Constructor

        Args:
            background (tuple[float, float, float]): Fix background to return.
        """
        super().__init__()
        self.background = background

    @property
    def mode(self) -> BackgroundMode:
        return BackgroundMode.FIXED

    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a series as input.

        Returns the fixed background passed to the constructor.

        Args:
            series (QtfSeries): Series to use to compute the background.

        Returns:
            tuple[float, float, float] | None: The fixed background.
        """
        return self.background

    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as input.

        Returns the fixed background passed to the constructor.

        Args:
            triplet (Triplet): Triplet to use to compute the background.

        Returns:
            tuple[float, float, float] | None: The fixed background.
        """
        return self.background

    def __eq__(self, other):
        """ Two ``BackgroundEngineFixed`` are equals if their fixed value are
        equals.
        """
        if isinstance(other, BackgroundEngineFixed):
            return self.background == other.background
        return False
