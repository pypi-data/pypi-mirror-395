
from quanti_fret.io.base import IOPhaseManager
from quanti_fret.io.calibration.config import CalibrationConfig
from quanti_fret.io.calibration.results import CalibrationResultsManager
from quanti_fret.io.calibration.stage_params import CalibrationStageParams
from quanti_fret.io.calibration.series_manager import (
    QtfCalibrationSeriesManager
)

from pathlib import Path


class CalibrationIOPhaseManager(IOPhaseManager):
    """ Implementation of the IOPhaseManager for the calibration
    """
    def __init__(self, load_series: bool = True) -> None:
        """ Constructor

        Args:
            load_series (bool, optional): If True, the IOPhaseManager will load
                the series itself using the values found in config. Otherwise,
                it is let to the user to handle the series loading.
                Defaults to True.
        """
        super().__init__('calibration', load_series, exclude_disabled_seq=True)

    def _updated_config(self, section: str, key: str) -> None:
        """ Signal that the config has been updated

        This catch the changes in input path and output path.

        Args:
            section (str): Section updated
            key (str): Key updated
        """
        super()._updated_config(section, key)
        if self._allow_updates:
            if section == 'Output' and key == 'output_dir':
                self._new_stage_params()
                if self._iopm_to_notify is not None:
                    val = self.config.get(section, key)
                    self._iopm_to_notify.external_config_update(
                        section, key, val)

    def _create_config(self, config_path: Path) -> None:
        """ Create the Config instance

        Args:
            config_path (os.PathLike | str): Path to the config to load
        """
        # Config
        self._config = CalibrationConfig()

    def _create_series_manager(self, load_series: bool) -> None:
        """ Create the Series Manager instance

        Must be called after `self._create_config`

        Args:
            load_series (bool): If True, also load the series
        """
        assert self._config is not None
        self._series_manager = QtfCalibrationSeriesManager()
        if load_series:
            for series in ['donors', 'acceptors', 'standards']:
                self._reset_series(series)

    def _create_results_manager(self) -> None:
        """ Create the ResultsManager instance

        Must be called after `self._create_config`
        """
        assert self._config is not None
        output_path: Path = self.config.get('Output', 'output_dir')
        self._results_manager = CalibrationResultsManager(output_path)

    def _create_stage_params(self) -> None:
        """ Create the ResultsManager instance

        Must be called after `self._create_config`,
        `self._create_series_manager` and `self._create_results_manager`
        """
        assert self._config is not None
        assert self._series_manager is not None
        assert self._results_manager is not None
        self._stage_params = CalibrationStageParams(
            self._config, self._series_manager, self._results_manager)
