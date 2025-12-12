
from quanti_fret.io.base.config import Config
from quanti_fret.io.base.results import ResultsManager, StageResults
from quanti_fret.io.base.series_manager import QtfSeriesManager
from quanti_fret.io.base.stage_params import StageParams
from quanti_fret.io.base.triplet_scanner import (
    TripletScanner, TripletSequenceLoader
)

from quanti_fret.core import QtfException, QtfSeries

import abc
import os
from pathlib import Path
from types import MethodType
from typing import Any, Callable


class IOPhaseManager(abc.ABC):
    """ Class that provides an access, from a single object, to a Config, a
    SeriesManager, a ResultsManager and a StageParams for a given phase.

    This class ensure that these 4 objects are linked and in a coherent state,
    meaning that every changes in one of them will be propagated to the others
    if needed (for example changing the output path in the config will modify
    the results manager).

    When using this class, you are expected to call all the time the getter
    properties to get config, series manager result manager or stage params in
    case they changed since last call. (Do not store them locally)

    Config, SeriesManager, ResultsManager and StageParams are proxied to
    catch their `save` or `set` method to propagate the information if needed.

    `_updated_config`, `_updated_series` and `_updated_results` are called
    every time `set` is called on the config or series manager, and everytime
    `save` is called from results manager.

    You must load a config before calling the different getters.
    """
    def __init__(
        self, phase: str, load_series: bool = True,
        exclude_disabled_seq: bool = True
    ) -> None:
        """ Constructor

        Args:
            phase (str): Name of the phase associated
            load_series (bool, optional): If True, the IOPhaseManager will load
                the series itself using the values found in config. Otherwise,
                it is let to the user to handle the series loading.
                Defaults to True.
            exclude_disabled_seq (bool): If True, will exclude disabled
                sequences when loadng a series.
        """
        self._allow_updates = False
        self._phase = phase
        self._load_series = load_series
        self._exclude_disabled_seq = exclude_disabled_seq
        self._object_to_update: IOPhaseManager = self
        self._iopm_to_notify: IOPhaseManager | None = None

        self._config: Config | None = None
        self._series_manager: QtfSeriesManager | None = None
        self._results_manager: ResultsManager | None = None
        self._stage_params: StageParams | None = None

    def load_config(self, config_path: os.PathLike | str) -> None:
        """ Load a new config from the given file

        Args:
            config_path (os.PathLike | str): Path to the config to load.
        """
        # Force to notify the IOPhaseManager when a value is set to the config.
        def new_set(self_: Config, section: str, key: str, value: Any) -> None:
            self_.__class__.set(self_, section, key, value)
            self._object_to_update._updated_config(section, key)

        self._allow_updates = False

        # Create the config
        self._create_config(Path(config_path))
        self.config.set = MethodType(new_set, self.config)  # type: ignore
        self.config.load(config_path)

        # Update other IOs
        self._new_series_manager()
        self._new_results_manager()
        self._new_stage_params()

        self._allow_updates = True

    def reset_config(self) -> None:
        """ Reset internal state by setting all parameters to None.

        The iopm can't be used without a `load_config` after that.
        """
        self._allow_updates = False
        self._config = None
        self._series_manager = None
        self._results_manager = None
        self._stage_params = None

    def link_iopm(self, other: 'IOPhaseManager | None') -> None:
        """ Link this IOPM to another one for specific notification

        Args:
            other (IOPhaseManager | None): IOPM to link
        """
        self._iopm_to_notify = other

    def external_config_update(self, section: str, key: str, val: Any) -> None:
        """ Signal that the config of the IOPM linked to self has been updated

        Args:
            section (str): Section updated
            key (str): Key updated
            val (Any): New value
        """
        pass

    @property
    def config(self) -> Config:
        if self._config is None:
            err = f'No config was set for the phase "{self._phase}"'
            raise QtfException(err)
        return self._config

    @property
    def series(self) -> QtfSeriesManager:
        if self._series_manager is None:
            err = f'No config was set for the phase "{self._phase}"'
            raise QtfException(err)
        return self._series_manager

    @property
    def results(self) -> ResultsManager:
        if self._results_manager is None:
            err = f'No config was set for the phase "{self._phase}"'
            raise QtfException(err)
        return self._results_manager

    @property
    def params(self) -> StageParams:
        if self._stage_params is None:
            err = f'No config was set for the phase "{self._phase}"'
            raise QtfException(err)
        return self._stage_params

    def _updated_config(self, section: str, key: str) -> None:
        """ Signal that the config has been updated

        This catch the changes in input path and output path.

        Args:
            section (str): Section updated
            key (str): Key updated
        """
        if self._allow_updates:
            if section == 'Series':
                self._reset_series(key)
            if section == 'Output' and key == 'output_dir':
                self._new_results_manager()
            if section == 'Output' and key == 'clean_before_run':
                clean_all_output = self.config.get(section, key)
                self.results.set_clean_all_output(clean_all_output)

    def _updated_series(self, name: str) -> None:
        """ Signal that the series have been updated

        Args:
            name (str): Name of the series updated
        """
        pass

    def _updated_results(self, stage: str):
        """ Signal that the results have been updated

        Args:
            stage (str): Stage updated
        """
        pass

    def _updated_params(self) -> None:
        """ Signal that the Stage params have been updated
        """
        pass

    def _new_series_manager(self) -> None:
        """ Create a new QtfSeriesManager and wrap its `set` method to inform
        the IOPhaseManager that a series was updated.
        """
        # Force to notify the IOPhaseManager when a series is set to the
        # manager.
        def new_set(
            self_: QtfSeriesManager, name: str,
            sequences: QtfSeries
        ) -> None:
            self_.__class__.set(self_, name, sequences)
            self._object_to_update._updated_series(name)

        self._create_series_manager(self._load_series)
        self.series.set = MethodType(new_set, self.series)  # type: ignore

    def _reset_series(self, series: str) -> None:
        """ Reset the series given as parameter by either scanning it again,
        or setting it to empty if `self._load_series` is False.

        Args:
            series (str): Series to reset
        """
        self.series.set(series, QtfSeries([]))
        if self._load_series:
            tsl = self._generate_sequence_loader()
            scanner = TripletScanner(tsl)
            sequences_path = self.config.get('Series', series)
            if sequences_path is not None:
                s = scanner.scan(sequences_path)
                if self._exclude_disabled_seq:
                    s = s.get_only_enabled()
                self.series.set(series, s)

    def _generate_sequence_loader(self) -> TripletSequenceLoader:
        """ Generate a TripletSequenceLoader using the configuration

        Args:
            series (str): Series to reset
        """
        regex = {
            'dd_path': '',
            'da_path': '',
            'aa_path': '',
            'mask_cell_path': '',
            'mask_bckg_path': '',
        }
        for key in regex:
            regex[key] = self.config.get('Regex', key[:-5])
        return TripletSequenceLoader(regex)

    def _new_results_manager(self) -> None:
        """ Create a new ResultsManager and wrap its `set` method to inform
        the IOPhaseManager that the ResultsManager was updated.
        """
        # Force to notify the IOPhaseManager when a results is saved.
        def save_stage_overwrite(
            stage: str
        ) -> Callable[[StageResults, tuple[Any, ...], tuple[Any, ...]], None]:
            def new_save(
                self_: StageResults, settings: tuple[Any, ...],
                results: tuple[Any, ...]
            ) -> None:
                self_.__class__.save_stage(self_, settings, results)
                self._object_to_update._updated_results(stage)
            return new_save

        self._create_results_manager()
        clean_all_output = self.config.get('Output', 'clean_before_run')
        self.results.set_clean_all_output(clean_all_output)
        for stage, manager in self.results._managers.items():
            manager.save_stage = MethodType(  # type: ignore
                save_stage_overwrite(stage), manager
            )

    def _new_stage_params(self) -> None:
        """ Create a new StageParams
        """
        self._create_stage_params()

    def _create_config(self, config_path: Path) -> None:
        """ Create the Config instance

        To be overridden

        Args:
            config_path (os.PathLike | str): Path to the config to load
        """
        raise QtfException('Not implemented')

    def _create_series_manager(self, load_series: bool) -> None:
        """ Create the Series Manager instance

        Must be called after `self._create_config`

        To be overridden

        Args:
            load_series (bool): If True, also load the series
        """
        raise QtfException('Not implemented')

    def _create_results_manager(self) -> None:
        """ Create the ResultsManager instance

        Must be called after `self._create_config`

        To be overridden
        """
        raise QtfException('Not implemented')

    def _create_stage_params(self) -> None:
        """ Create the ResultsManager instance

        Must be called after `self._create_config`,
        `self._create_series_manager` and `self._create_results_manager`

        To be overridden
        """
        raise QtfException('Not implemented')
