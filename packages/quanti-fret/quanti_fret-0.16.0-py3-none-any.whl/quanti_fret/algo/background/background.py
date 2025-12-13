from quanti_fret.algo.background.disabled import BackgroundEngineDisabled
from quanti_fret.algo.background.engine import BackgroundEngine
from quanti_fret.algo.background.fixed import BackgroundEngineFixed
from quanti_fret.algo.background.mask import BackgroundEngineMask
from quanti_fret.algo.background.mode import BackgroundMode
from quanti_fret.algo.background.percentile import BackgroundEnginePercentile

import quanti_fret.algo.matrix_functions as mfunc
from quanti_fret.core import QtfSeries, QtfException, Triplet

import numpy as np


def compute_background(
    series: QtfSeries, engine: BackgroundEngine
) -> tuple[float, float, float] | None:
    """ Compute the median background values of each channel (DD, DA, AA) on
    the given series.

    This functions does nothing but calling the
    :any:`BackgroundEngine.compute_background_on_series` method of the engine.
    It exists just to keep the same logic of getting parameters from
    :any:`StageParams` and passing them to the function that performs the run.

    Args:
        series (QtfSeries): Series used to extracts the backgrounds.
        engine (BackgroundEngine): Engine used to compute the median
            background.

    Returns:
        tuple[float, float, float] | None: Average background for every
        channels (DA, DD, AA) or None if no background was generated.
    """
    return engine.compute_background_on_series(series)


def substract_background(
    triplet: Triplet, engine: BackgroundEngine
) -> np.ndarray:
    """ Substract a background to a triplet.

    Every negative values will be clipped to 0.

    The background to substract will be computed using the the engine.

    Args:
        triplet (Triplet): Triplet we want to substract the background of.
        engine (BackgroundEngine): Engine used to compute the background to
            substract.

    Returns:
        np.ndarray: The triplet as a numpy array with all 3 channels (DD,
        DA, AA) stacked on first axis, and with the background substracted.
    """
    background = engine.compute_background_on_triplet(triplet)
    if background is None:
        return triplet.as_numpy
    else:
        return mfunc.substract_background(triplet.as_numpy, background)


def create_background_engine(
    mode: BackgroundMode,
    background: tuple[float, float, float] | None = None,
    percentile: float = -1
) -> BackgroundEngine:
    """ Create the background associated with the given Mode and parameters.

    Args:
        mode (BackgroundMode): Mode of the Background to create.
        background (tuple[float, float, float] | None, optional): Fixed
            Background value to set. Used only for the ``FIXED`` mode. If in
            ``FIXED`` mode, this parameter can't be None. Defaults to None.
        percentile (float, optional): percentile value to set. Used only for
            the ``PERCENTILE`` mode. If in ``PERCENTILE`` mode, this parameter
            must be between 0 and 100. Defaults to -1.

    Returns:
        BackgroundEngine: The Background Engine created.
    """
    if mode == BackgroundMode.DISABLED:
        return BackgroundEngineDisabled()
    elif mode == BackgroundMode.MASK:
        return BackgroundEngineMask()
    elif mode == BackgroundMode.PERCENTILE:
        return BackgroundEnginePercentile(percentile)
    else:
        if background is None:
            err = 'You must specify a background value for the fix mode'
            raise QtfException(err)
        return BackgroundEngineFixed(background)
