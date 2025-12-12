from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.core import QtfSeries, Triplet, QtfException

import numpy as np


class BackgroundEnginePercentile(BackgroundEngine):
    """ This is a background computed using the low percentile values of the
    triplets

    To compute the background, we extract the values, for a given channel, of
    all the pixels of the triplet (or of all triplets of a series) within the
    background area. We then take the median of all these values.

    In this mode, the background area is defined, for each triplets, and for
    each channels, by the pixels, representing the lowest given percentile
    values.
    """
    def __init__(self, percentile: float) -> None:
        """ Constructor

        Args:
            percentile (float): Low percentile values to use to compute the
                background
        """
        super().__init__()
        if percentile < 0. or percentile > 100.:
            msg = f'Background percentile "{percentile} out of range "[0-100]"'
            raise QtfException(msg)
        self._percentile = percentile

    @property
    def mode(self) -> BackgroundMode:
        """ Get the BackgroundMode associated with the class
        """
        return BackgroundMode.PERCENTILE

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
        sit = series.iterator(sample_sequences=True)
        series_np = np.stack([triplet.as_numpy for triplet in sit], axis=0)

        dds = series_np[:, 0]
        das = series_np[:, 1]
        aas = series_np[:, 2]

        dd_median = self._compute_background_on_channel(dds)
        da_median = self._compute_background_on_channel(das)
        aa_median = self._compute_background_on_channel(aas)

        return dd_median, da_median, aa_median

    def compute_background_on_triplet(
        self, triplet: Triplet
    ) -> tuple[float, float, float] | None:
        """ Compute the background value using a single Triplet as an input

        Args:
            triplet (Triplet): Triplet to use to compute the background

        Returns:
            tuple[float, float, float]: Background for every channels (DA, DD,
                AA)
        """
        dd = triplet.dd
        da = triplet.da
        aa = triplet.aa

        dd_median = self._compute_background_on_channel(dd)
        da_median = self._compute_background_on_channel(da)
        aa_median = self._compute_background_on_channel(aa)

        return dd_median, da_median, aa_median

    def _compute_background_on_channel(self, array: np.ndarray) -> float:
        """ Compute the background on a single channel.

        This expect the input array to be representing a single channel inside
        either a triplet or a series of sequences of triplets.

        Args:
            channel (np.ndarray): the channel for every triplet of the
                series

        Returns:
            float: The background
        """
        val_max = np.nanpercentile(array, self._percentile, axis=(-2, -1))
        val_max = np.expand_dims(val_max, axis=(-1, -2))
        median = np.median(array[array <= val_max])
        return float(np.round(median, 3))

    def _compute_background_on_np(
        self, array: np.ndarray
    ) -> tuple[float, float, float]:
        """ Compute the background on a numpy Array

        This takes as an input any array, as long as it's last 3 axis are of
        shape (3, Width, Height).

        This is not used anymore, I keep it in case.

        Args:
            array (np.ndarray): Array to use to compute the background

        Returns:
            tuple[float, float, float] | None: Background for every channels
                (DA, DD, AA) or None if no background was generated
        """
        # Get percentile max value
        vals_max = np.nanpercentile(array,  self._percentile, axis=(-2, -1))
        vals_max = np.expand_dims(vals_max, axis=(-1, -2))
        # Reject all values higher than vals_max
        masked: np.ndarray = np.ma.masked_array(array, array > vals_max)
        # Compute the triplet mean values.
        median_axis = [d for d in range(-array.ndim, 0) if d != -3]
        median = np.ma.median(masked, axis=median_axis)
        median = np.round(median, 3)
        # Return background
        assert median.shape == (3,)

        return float(median[0]), float(median[1]), float(median[2])

    def __eq__(self, other):
        """ Overrides the default __eq__ implementation """
        if isinstance(other, BackgroundEnginePercentile):
            return self._percentile == other._percentile
        return False
