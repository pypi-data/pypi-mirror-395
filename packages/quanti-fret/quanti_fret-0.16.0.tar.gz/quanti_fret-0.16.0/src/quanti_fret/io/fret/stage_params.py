from quanti_fret.io.fret.config import FretConfig
from quanti_fret.io.calibration import CalibrationResultsManager

from quanti_fret.algo import BackgroundEngine
from quanti_fret.core import QtfSeries, QtfException
from quanti_fret.io.base import (
    Config,
    ResultsManager,
    QtfSeriesManager,
    StageParams,
)

from typing import Any


class FretStageParams(StageParams):
    """ Class that returns the parameters to use to run each stages of the
    fret.

    This class is linked to a Config, a QtfSeriesManager and a ResultsManager
    that it uses to get the differents parameters.

    For all stages, a check is done on the parameters and an exception is
    raised if some are missing. You can ignore this behavior by setting
    `allow_none_values` to True if you want all the parameters that are valid
    others will be set to None)

    The method always return one parameter more than the ones passed to the
    stage's run method, which is a decription of the input series (either its
    name or the mode used for background computation)
    """

    def __init__(
        self, config: Config, series_manager: QtfSeriesManager,
        results_manager: ResultsManager | None
    ) -> None:
        """ Constructor

        Args:
            config (Config): Config to use
            series_manager (QtfSeriesManager): Series Manager to use
            results_manager (ResultsManager): Results Manager to use
        """
        if type(config) is not FretConfig:
            raise QtfException('Unexpected Config type')
        if results_manager is not None and \
           type(results_manager) is not CalibrationResultsManager:
            raise QtfException('Unexpected ResultsManager type')

        self._config = config
        self._series = series_manager
        self._results = results_manager
        super().__init__()

    def get(
        self, stage: str, allow_none_values: bool = False
    ) -> tuple[Any, ...]:
        """ Get the parameters of the stage passed in arguments

        Args:
            stage (str): Stage to get the parameters from. Must be in
                ['fret', 'fret_params']
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[Any, ...]: The parameters for the stage (see each starge get
                method for more information)
        """
        stages_gets = {
            'fret': self._fret,
            'fret_params': self._fret_params,
            'cali_background': self._cali_background,
        }
        if stage not in stages_gets:
            raise QtfException(f'Unknown stage {stage}')
        return stages_gets[stage](allow_none_values)

    def _fret(
        self, allow_none_values: bool = False
    ) -> tuple[str, QtfSeries, float | None, float | None, float | None,
               float | None, BackgroundEngine | None, float, float, float,
               float, bool, int]:
        """  Get the params for the Fret to run on a full series.

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[str, QtfSeries, float | None, float | None, float | None,
                  float | None, BackgroundEngine | None, float, float, float,
                  float, bool, int]:
                - Name of the series
                - Series to use
                - Alpha BT value
                - Delta DE value
                - BetaX value
                - GammaM DE value
                - Background on all 3 channels
                - Sigma S value
                - Target S value
                - Sigma Gauss value
                - Weights Threshold value
                - Save analysis details
                - Sampling
        """
        # Get series
        series = self._series.get('experiments')
        if series.size == 0 and not allow_none_values:
            raise QtfException('0 Sequences found')

        params = self._fret_params(allow_none_values)
        background = params[4]
        self.validate_series_for_background(background, series,
                                            allow_none_values)

        return ('experiments', series, *params)

    def _fret_params(
        self, allow_none_values: bool = False
    ) -> tuple[float | None, float | None, float | None, float | None,
               BackgroundEngine | None, float, float, float, float, bool, int]:
        """  Get the params for the Fret set_params method.

        These are the Fret params without the series associated. Use this to
        run on single triplet.

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[float | None, float | None, float | None, float | None,
                  BackgroundEngine | None, float, float, float, float, bool,
                  int]:
                - Alpha BT value
                - Delta DE value
                - BetaX value
                - GammaM DE value
                - Background on all 3 channels
                - Sigma S value
                - Target S value
                - Sigma Gauss value
                - Weights Threshold value
                - Save analysis details
                - Sampling
        """
        # Get Fret settings from config
        sigma_s: float = self._config.get('Fret', 'sigma_s')
        target_s: float = self._config.get('Fret', 'target_s')
        sigma_gauss: float = self._config.get('Fret', 'sigma_gauss')
        weights_threshold: float = self._config.get('Fret',
                                                    'weights_threshold')
        analysis_details: bool = self._config.get('Fret',
                                                  'save_analysis_details')
        analysis_sampling: int = self._config.get('Fret',
                                                  'analysis_sampling')

        # Get Background settings
        background = self.get_background_engine_from_config(self._config)

        if self._results is None:
            if not allow_none_values:
                raise QtfException('No Calibration config file set')
            else:
                alpha_bt = None
                delta_de = None
                beta_x = None
                gamma_m = None
        else:
            # Retrieve calibration results
            if background is None:
                res = self._results['background'].get_stage_results()
                if res is None:
                    if not allow_none_values:
                        raise QtfException('No Background results found')
                    background = None
                else:
                    background, = res

            res = self._results['bt'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No BT results found')
                alpha_bt = None
            else:
                alpha_bt, _, _ = res

            res = self._results['de'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No DE results found')
                delta_de = None
            else:
                delta_de, _, _ = res

            res = self._results['xm'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No XM results found')
                beta_x = None
                gamma_m = None
            else:
                beta_x, gamma_m, _, _, _ = res

        return (
            alpha_bt, delta_de, beta_x, gamma_m, background,
            sigma_s, target_s, sigma_gauss, weights_threshold,
            analysis_details, analysis_sampling,
        )

    def _cali_background(
        self, allow_none_values: bool = False
    ) -> tuple[BackgroundEngine | None]:
        """  Get the background value from calibration

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            BackgroundEngine | None: Background engine from calibration or
                None if no results is found
        """
        if self._results is None:
            if not allow_none_values:
                raise QtfException('No Calibration config file set')
            else:
                background = None
        else:
            # Retrieve calibration results
            res = self._results['background'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No Background results found')
                background = None
            else:
                background, = res

        return (background,)
