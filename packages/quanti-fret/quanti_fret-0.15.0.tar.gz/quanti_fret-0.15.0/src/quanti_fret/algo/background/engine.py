from quanti_fret.algo.background.mode import BackgroundMode

from quanti_fret.core import QtfSeries, Triplet

import abc


class BackgroundEngine(abc.ABC):
    """ BackgroundEngines classes allow you to compute backgrounds from series
    or triplets
    """
    @property
    @abc.abstractmethod
    def mode(self) -> BackgroundMode:
        """ Get the BackgroundMode associated with the class
        """
        pass

    @abc.abstractmethod
    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a whole series as an input

        Args:
            series (QtfSeries): series to use to compute the background

        Returns:
            tuple[float, float, float] | None: Background for every channels
                (DA, DD, AA) or None if no background was generated
        """
        pass

    @abc.abstractmethod
    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as an input

        Args:
            triplet (Triplet): Triplet to use to compute the background

        Returns:
            tuple[float, float, float] | None: Background for every channels
                (DA, DD, AA) or None if no background was generated
        """
        pass
