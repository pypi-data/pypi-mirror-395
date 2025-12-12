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
    """ Compute the average background values of each channel on the given
    series.

    This function exists mainly to keep the same logic of getting parameters
    from StageParams and passing them to the function that performs the run

    Args:
        series (QtfSeries): series to compute the background on
        engine (BackgroundEngine): The engine to use to compute the Background

    Returns:
        tuple[float, float, float] | None: Average background for every
            channels (DA, DD, AA) or None if no background was generated
    """
    return engine.compute_background_on_series(series)


def substract_background(
    triplet: Triplet, engine: BackgroundEngine
) -> np.ndarray:
    """ Substract a background to a triplet

    Every negative values will be clipped to 0.

    The background will be taken from the engine

    Args:
        triplet (Triplet): Triplet to substract the background of

    Returns:
        np.ndarray: the triplet as a numpy array with all 3 channels (DD,
            DA, AA) stacked, and with the background substracted
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
    """ Get the background associated with the Mode

    Args:
        mode (BackgroundMode): Mode of the Background
        background (tuple[float, float, float] | None, optional): Fixed
            Background to set (used only for the FIXED mode). Defaults to None.
        percentile (float, optional): percentile value (used only for the
            PERCENTILE mode). Defaults to -1.

    Returns:
        BackgroundEngine: The Background Engine to use
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
