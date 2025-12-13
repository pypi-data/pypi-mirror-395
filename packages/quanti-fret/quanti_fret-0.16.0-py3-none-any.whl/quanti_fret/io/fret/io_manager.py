from quanti_fret.core import QtfException
from quanti_fret.io.base import IOPhaseManager
from quanti_fret.io.calibration.results import CalibrationResultsManager
from quanti_fret.io.calibration.config import CalibrationConfig
from quanti_fret.io.fret.config import FretConfig
from quanti_fret.io.fret.results import FretResultsManager
from quanti_fret.io.fret.stage_params import FretStageParams
from quanti_fret.io.fret.series_manager import QtfFretSeriesManager

from pathlib import Path
from typing import Any


class FretIOPhaseManager(IOPhaseManager):
    """ Implementation of the IOPhaseManager for the fret
    """
    def __init__(self, load_series: bool = True) -> None:
        """ Constructor

        Args:
            load_series (bool, optional): If True, the IOPhaseManager will load
                the series itself using the values found in config. Otherwise,
                it is let to the user to handle the series loading.
                Defaults to True.
        """
        super().__init__('fret', load_series, exclude_disabled_seq=False)

    def _updated_config(self, section: str, key: str) -> None:
        """ Signal that the config has been updated

        This catch the changes in input path and output path.

        Args:
            section (str): Section updated
            key (str): Key updated
        """
        super()._updated_config(section, key)
        if self._allow_updates:
            if section == 'Calibration' and key == 'config_file':
                self._new_stage_params()

    def _create_config(self, config_path: Path) -> None:
        """ Create the Config instance

        Args:
            config_path (os.PathLike | str): Path to the config to load

        Returns:
            Config: The config created
        """
        # Config
        self._config = FretConfig()

    def _create_series_manager(self, load_series: bool) -> None:
        """ Create the Series Manager instance

        Must be called after `self._create_config`

        Args:
            load_series (bool): If True, also load the series

        Returns:
            QtfSeriesManager: The series manager created
        """
        assert self._config is not None
        self._series_manager = QtfFretSeriesManager()
        if load_series:
            self._reset_series('experiments')

    def _create_results_manager(self) -> None:
        """ Create the ResultsManager instance

        Must be called after `self._create_config`

        Returns:
            ResultsManager: The results manager created
        """
        assert self._config is not None
        output_path: Path = self.config.get('Output', 'output_dir')
        self._results_manager = FretResultsManager(output_path)

    def _create_stage_params(self) -> None:
        """ Create the ResultsManager instance

        Must be called after `self._create_config`,
        `self._create_series_manager` and `self._create_results_manager`

        Returns:
            StageParams: The stage params created
        """
        assert self._config is not None
        assert self._series_manager is not None

        cali_config_file = self._config.get('Calibration', 'config_file')
        if cali_config_file is None:
            calibration_dir = None
        else:
            config = CalibrationConfig()
            try:
                config.load(cali_config_file)
            except Exception as e:
                msg = f'Error while loading calibration config: {e}'
                raise QtfException(msg)
            calibration_dir = config.get('Output', 'output_dir')
        self._instanciate_stage_params(calibration_dir)

    def _instanciate_stage_params(self, cali_path: Path | None) -> None:
        """ Instanciate the stage param associated with this IOPM

        Args:
            cali_path (Path | None): Path to the calibration results folder
        """
        assert self._config is not None
        assert self._series_manager is not None

        if cali_path is None:
            self._stage_params = FretStageParams(
                self._config, self._series_manager, None
            )
        else:
            cali_results_manager = CalibrationResultsManager(cali_path)
            self._stage_params = FretStageParams(
                self._config, self._series_manager, cali_results_manager
            )

    def external_config_update(self, section: str, key: str, val: Any) -> None:
        """ Signal that the config of the IOPM linked to self has been updated

        Args:
            section (str): Section updated
            key (str): Key updated
        """
        if self._config is not None and self._series_manager is not None:
            if section == 'Output' and key == 'output_dir':
                assert val is None or isinstance(val, Path)
                self._instanciate_stage_params(val)
                self._object_to_update._updated_params()
