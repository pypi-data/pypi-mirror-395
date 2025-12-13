from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.core import QtfSeries, Triplet, QtfException

import numpy as np


class BackgroundEnginePercentile(BackgroundEngine):
    """ The ``BackgroundEnginePercentile`` computes the median background
    on the pixels with the lowest value.

    The background values returned are the median of all the triplet's
    background pixels, keeping separated the 3 channels (DD, DA, AA).

    The pixels to use are determined, for each channel, by choosing the values
    representing the lowest given percentile.

    For a series, we keep only one sample element per sequences (using
    :any:`QtfSeries.iterator`).
    """

    def __init__(self, percentile: float) -> None:
        """ Constructor

        Args:
            percentile (float): Low percentile values to use to select the
                pixels for the background computation. Must be between 0 and
                100.

        Raises:
            QtfException: The percentile is out of range
        """
        super().__init__()
        if percentile < 0. or percentile > 100.:
            msg = f'Background percentile "{percentile} out of range "[0-100]"'
            raise QtfException(msg)
        self._percentile = percentile

    @property
    def mode(self) -> BackgroundMode:
        return BackgroundMode.PERCENTILE

    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
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
        dd = triplet.dd
        da = triplet.da
        aa = triplet.aa

        dd_median = self._compute_background_on_channel(dd)
        da_median = self._compute_background_on_channel(da)
        aa_median = self._compute_background_on_channel(aa)

        return dd_median, da_median, aa_median

    def _compute_background_on_channel(self, array: np.ndarray) -> float:
        """ Compute the background of a single channel.

        The input array must represents a single channel of either a triplet
        or a series of sequences of triplets.

        To compute the background, it extracts, for each triplet, the low
        percentile pixels. It then compute the median of all the values
        extracted.

        Args:
            channel (np.ndarray): The channel data for every triplet of the
                series (or for just one triplet). Shape is either (height,
                width) or (Series Length, Sequence length, height, width)

        Returns:
            float: The background
        """
        val_max = np.nanpercentile(array, self._percentile, axis=(-2, -1))
        val_max = np.expand_dims(val_max, axis=(-1, -2))
        median = np.median(array[array <= val_max])
        return float(np.round(median, 3))

    def __eq__(self, other):
        """ Two ``BackgroundEnginePercentile`` are equals if their percentile
        value are equals.
        """
        if isinstance(other, BackgroundEnginePercentile):
            return self._percentile == other._percentile
        return False
