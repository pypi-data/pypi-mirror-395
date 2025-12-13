from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.core import QtfSeries, Triplet

import numpy as np


class BackgroundEngineMask(BackgroundEngine):
    """ The ``BackgroundEngineMask`` uses the triplet's background mask to
    compute the median background values.

    The background values returned are the median of all the triplet's
    background pixels, keeping separated the 3 channels (DD, DA, AA).

    The pixels to use are determined with the background mask from each
    triplet using :any:`Triplet.mask_bckg`.

    For a series, we keep only one sample element per sequences (using
    :any:`QtfSeries.iterator`).
    """

    @property
    def mode(self) -> BackgroundMode:
        return BackgroundMode.MASK

    def compute_background_on_series(
        self, series: QtfSeries
    ) -> tuple[float, float, float] | None:
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
        dd = triplet.dd
        da = triplet.da
        aa = triplet.aa
        mask_bckg = triplet.mask_bckg

        bckg_dd = float(np.round((np.median(dd[mask_bckg])), 3))
        bckg_da = float(np.round((np.median(da[mask_bckg])), 3))
        bckg_aa = float(np.round((np.median(aa[mask_bckg])), 3))

        return bckg_dd, bckg_da, bckg_aa

    def __eq__(self, other):
        """ Two ``BackgroundEngineMask`` are always equals """
        if isinstance(other, BackgroundEngineMask):
            return True
        return False
