from quanti_fret.algo import (
    BackgroundEngine, BackgroundMode, create_background_engine
)
from quanti_fret.core import QtfException, QtfSeries
from quanti_fret.io.base.config import Config

import abc
from typing import Any


class StageParams(abc.ABC):
    """ Class that returns the parameters to use to run each stages.

    This class is linked to a Config, a QtfSeriesManager and a ResultsManager
    that it uses to get the differents parameters.

    For all stages, a check is done on the parameters and an exception is
    raised if some are missing. You can ignore this behavior by setting
    `allow_none_values` to True if you want all the parameters that are valid
    (others will be set to None)

    The method always return one parameter more than the ones to pass to the
    stage's run method, which is a decription of the input series (either its
    name or the mode used for background computation)
    """

    @abc.abstractmethod
    def get(
        self, stage: str, allow_none_values: bool = False
    ) -> tuple[Any, ...]:
        """ Get the parameters of the stage passed in arguments

        Args:
            stage (str): Stage to get the parameters from. Must be in
                the stages accepted by the StageParams implementation
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[Any, ...]: The parameters for the stage (see each starge get
                method for more information)
        """
        pass

    def get_background_engine_from_config(
        self, config: Config, invert_floating: bool = False
    ) -> BackgroundEngine | None:
        """ Utility function to retrive the background engine from the config

        Args:
            config (Config): Config to use
            ignore_floating (bool): Invert the floating value. Used to
                differenciate background stage for calibration and the rest.

        Returns:
            BackgroundEngine | None: The engine to use or None if no engine
                was created
        """
        floating: bool = config.get('Background', 'floating')
        mode: BackgroundMode = config.get('Background', 'mode')
        percentile: float = config.get('Background', 'percentile')
        fixed_background: tuple[float, float, float] = \
            config.get('Background', 'fixed_background')

        if invert_floating:
            floating = not floating

        if floating:
            return create_background_engine(
                mode=mode, background=fixed_background, percentile=percentile
            )
        else:
            return None

    def validate_series_for_background(
        self, engine: BackgroundEngine | None, series: QtfSeries,
        disable_exception: bool = False
    ) -> bool:
        """ Test if the series is compatible with the background mode.

        For now, test that all the triplets have a background mask if the
        mode is BackgroundMode.MASK

        Args:
            engine (BackgroundEngine): Background engine to use
            series (QtfSeries): series to check
            disable_exception (bool, optional): If set to True, will not
                raise an exception on error. Default to False

        Raises:
            QtfException: If the series is not compatible

        Returns:
            bool: True if series is compatible, False otherwise
        """
        if engine is None:
            return True
        if engine.mode == BackgroundMode.MASK:
            if not series.have_all_mask_bckg():
                if not disable_exception:
                    err = "Some triplets don't have a mask background"
                    raise QtfException(err)
                else:
                    return False
        return True
