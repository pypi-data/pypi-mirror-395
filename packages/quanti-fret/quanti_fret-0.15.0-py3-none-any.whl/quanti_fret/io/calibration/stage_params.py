from quanti_fret.algo import (
    BackgroundEngine, BackgroundMode, create_background_engine
)
from quanti_fret.io.calibration.config import CalibrationConfig
from quanti_fret.io.calibration.results import CalibrationResultsManager

from quanti_fret.core import QtfSeries, QtfException
from quanti_fret.io.base import (
    Config,
    ResultsManager,
    QtfSeriesManager,
    StageParams,
)

from typing import Any


class CalibrationStageParams(StageParams):
    """ Class that returns the parameters to use to run each stages of the
    calibration.

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
        results_manager: ResultsManager
    ) -> None:
        """ Constructor

        Args:
            config (Config): Config to use
            series_manager (QtfSeriesManager): Series Manager to use
            results_manager (ResultsManager): Results Manager to use
        """
        if type(config) is not CalibrationConfig:
            raise QtfException('Unexpected Config type')
        if type(results_manager) is not CalibrationResultsManager:
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
                ['background', 'bt', 'de', 'xm']
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
            'background': self._background,
            'bt': self._bt,
            'de': self._de,
            'xm': self._xm,
        }
        if stage not in stages_gets:
            raise QtfException(f'Unknown stage {stage}')
        return stages_gets[stage](allow_none_values)

    def _background(
        self, allow_none_values: bool = False
    ) -> tuple[list[str], QtfSeries, BackgroundEngine]:
        """ Get the params for the background run

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[BackgroundMode, QtfSeries]: [mode, series]
        """
        # Get config values
        engine = self.get_background_engine_from_config(
            self._config, invert_floating=True
        )
        use_donors: float = self._config.get('Background', 'use_donors')
        use_acceptors: float = self._config.get('Background', 'use_acceptors')
        use_standards: float = self._config.get('Background', 'use_standards')

        # Get background
        if engine is None:
            engine = create_background_engine(mode=BackgroundMode.DISABLED)

        # Set up series
        series_names: list[str] = []
        if engine.mode in [BackgroundMode.PERCENTILE, BackgroundMode.MASK]:
            if use_donors:
                series_names.append('donors')
            if use_acceptors:
                series_names.append('acceptors')
            if use_standards:
                series_names.append('standards')
        series = self._series.get(series_names)
        if engine.mode in [BackgroundMode.PERCENTILE, BackgroundMode.MASK]:
            if series.size == 0 and not allow_none_values:
                raise QtfException('0 Sequences found')

        self.validate_series_for_background(engine, series, allow_none_values)

        # return results
        return series_names, series, engine

    def _bt(
        self, allow_none_values: bool = False
    ) -> tuple[str, QtfSeries, BackgroundEngine | None, float, bool]:
        """ Get the params for the BT run

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[str, QtfSeries, BackgroundEngine | None, float, bool]:
                - Name of the series
                - Series to use
                - Background engine
                - Discard low percentile value
                - Plot details value
        """
        # Manage params
        donors = self._series.get('donors')
        if donors.size == 0 and not allow_none_values:
            raise QtfException('0 Sequences found')
        if not donors.have_all_mask_cell() and not allow_none_values:
            raise QtfException('Some mask cells are missing')
        low_percentile: float = self._config.get(
            'BT',
            'discard_low_percentile')
        plot_details: bool = self._config.get(
            'BT',
            'plot_sequence_details')

        # Manage Background
        background = self.get_background_engine_from_config(self._config)
        if background is None:
            res = self._results['background'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No Background results found')
                background = None
            else:
                background, = res
        self.validate_series_for_background(background, donors,
                                            allow_none_values)

        return 'donors', donors, background, low_percentile, plot_details

    def _de(
        self, allow_none_values: bool = False
    ) -> tuple[str, QtfSeries, BackgroundEngine | None, float, bool]:
        """ Get the params for the DE run

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[str, QtfSeries, BackgroundEngine, float, bool]:
                - Name of the series
                - Series to use
                - Background engine
                - Discard low percentile value
                - Plot details value
        """
        # Manage params
        acceptors = self._series.get('acceptors')
        if acceptors.size == 0 and not allow_none_values:
            raise QtfException('0 Sequences found')
        if not acceptors.have_all_mask_cell() and not allow_none_values:
            raise QtfException('Some mask cells are missing')
        low_percentile: float = self._config.get(
            'DE',
            'discard_low_percentile')
        plot_details: bool = self._config.get(
            'DE',
            'plot_sequence_details')

        # Manage Background
        background = self.get_background_engine_from_config(self._config)
        if background is None:
            res = self._results['background'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No Background results found')
                background = None
            else:
                background, = res
        self.validate_series_for_background(background, acceptors,
                                            allow_none_values)

        return ('acceptors', acceptors, background, low_percentile,
                plot_details)

    def _xm(
        self, allow_none_values: bool = False
    ) -> tuple[str, QtfSeries, float | None, float | None,
               BackgroundEngine | None, tuple[float, float],
               bool, int]:
        """  Get the params for the GammaXM run

        Args:
            allow_none_values (bool, optional): If true, will not raise
                exceptions if elements are missing for the run, instead values
                not found will be set to None.. Defaults to False.

        Raises:
            QtfException: If elements are missing for the run.

        Returns:
            tuple[str, QtfSeries, float | None, float | None,
                  BackgroundEngine | None, tuple[float, float],
                  bool, int]:
                - Name of the series
                - Series to use
                - Alpha BT value
                - Delta DE value
                - Background engine
                - Percentil Range
                - Save analysis details
                - Sampling
        """
        # Get XM settings
        series = self._series.get('standards')
        if series.size == 0 and not allow_none_values:
            raise QtfException('0 Sequences found')
        if not series.have_all_mask_cell() and not allow_none_values:
            raise QtfException('Some mask cells are missing')
        low_percentile: float = self._config.get(
            'XM',
            'discard_low_percentile')
        high_percentile: float = self._config.get(
            'XM',
            'discard_high_percentile')
        analysis_details: bool = self._config.get(
            'XM',
            'save_analysis_details')
        sampling: int = self._config.get(
            'XM',
            'analysis_sampling')

        # Manage Background
        background = self.get_background_engine_from_config(self._config)
        if background is None:
            res = self._results['background'].get_stage_results()
            if res is None:
                if not allow_none_values:
                    raise QtfException('No Background results found')
                background = None
            else:
                background, = res
        self.validate_series_for_background(background, series,
                                            allow_none_values)

        # Retrieve previous results
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
        return ('standards', series, alpha_bt, delta_de, background,
                (low_percentile, high_percentile), analysis_details, sampling)
