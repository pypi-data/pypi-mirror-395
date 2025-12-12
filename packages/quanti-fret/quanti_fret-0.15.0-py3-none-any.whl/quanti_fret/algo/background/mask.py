from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.core import QtfSeries, Triplet

import numpy as np


class BackgroundEngineMask(BackgroundEngine):
    """ This is a background computed using the background mask of the triplets

    To compute the background, we extract the values, for a given channel, of
    all the pixels of the triplet (or of all triplets of a series) within the
    background area. We then take the median of all these values.

    In this mode, the background area is defined, for each triplets, by the
    background mask of the triplet.
    """
    @property
    def mode(self) -> BackgroundMode:
        """ Get the BackgroundMode associated with the class
        """
        return BackgroundMode.MASK

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
        series_list = [
            triplet.as_numpy[:, triplet.mask_bckg] for triplet in sit
        ]
        series_np = np.concatenate(series_list, axis=1)

        dds = series_np[0]
        das = series_np[1]
        aas = series_np[2]

        bckg_dd = float(np.round((np.median(dds)), 3))
        bckg_da = float(np.round((np.median(das)), 3))
        bckg_aa = float(np.round((np.median(aas)), 3))

        return bckg_dd, bckg_da, bckg_aa

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
        dd = triplet.dd
        da = triplet.da
        aa = triplet.aa
        mask_bckg = triplet.mask_bckg

        bckg_dd = float(np.round((np.median(dd[mask_bckg])), 3))
        bckg_da = float(np.round((np.median(da[mask_bckg])), 3))
        bckg_aa = float(np.round((np.median(aa[mask_bckg])), 3))

        return bckg_dd, bckg_da, bckg_aa

    def __eq__(self, other):
        """ Overrides the default __eq__ implementation """
        if isinstance(other, BackgroundEngineMask):
            return True
        return False
