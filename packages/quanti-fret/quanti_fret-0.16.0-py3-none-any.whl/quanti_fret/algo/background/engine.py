from quanti_fret.algo.background.mode import BackgroundMode

from quanti_fret.core import QtfSeries, Triplet

import abc


class BackgroundEngine(abc.ABC):
    """ The ``BackgroundEngines`` computes a median background values from a
    series or from a triplet.
    """

    @property
    @abc.abstractmethod
    def mode(self) -> BackgroundMode:
        """ The mode associated with the class.
        """
        pass

    @abc.abstractmethod
    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a series as input.

        Args:
            series (QtfSeries): Series to use to compute the background.

        Returns:
            tuple[float, float, float] | None: Background for every channels
                (DA, DD, AA) or None if no background was generated.
        """
        pass

    @abc.abstractmethod
    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as input.

        Args:
            triplet (Triplet): Triplet to use to compute the background.

        Returns:
            tuple[float, float, float] | None: Background for every channels
                (DA, DD, AA) or None if no background was generated
        """
        pass
