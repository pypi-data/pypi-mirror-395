from quanti_fret.apps.app_default_path import AppDefaultPath
from quanti_fret.core import QtfException, Singleton
from quanti_fret.io import (
    CalibrationConfig, CalibrationIOPhaseManager, Config, FretConfig,
    FretIOPhaseManager, IOManager, IOPhaseManager, QtfSeriesManager,
    ResultsManager, StageParams
)

from os import PathLike
from enum import Enum
from pathlib import Path
import traceback
from typing import Any

from qtpy.QtCore import QObject, Signal, SignalInstance


class IOGuiManager(metaclass=Singleton):
    """ Single entry point in all the GUI app to get access to a single
    instance of the IOPhaseGuiManager for calibration and fret.
    """

    def __init__(self):
        """ Constructor: Creates the IOPhaseGuiManagers
        """
        self._iopm_cali = IOPhaseGuiManager('calibration')
        self._iopm_fret = IOPhaseGuiManager('fret')
        self._iopm = IOManager(self._iopm_cali, self._iopm_fret)
        self._iopm_cali.link_iopm(None)

    def get_iopm(self, phase: str) -> 'IOPhaseGuiManager':
        """ Get the IOPhaseGuiManager associated with the given phase.

        Args:
            phase (str): phase to get the IOPhaseGuiManager from

        Raises:
            QtfException: phase doesn't exists

        Returns:
            IOPhaseGuiManager:  IOPhaseGuiManager associated
        """
        if phase == 'calibration':
            return self._iopm_cali
        elif phase == 'fret':
            return self._iopm_fret
        else:
            raise QtfException(f'Unknown phase {phase}')

    @property
    def cali(self) -> 'IOPhaseGuiManager':
        """ Getter of the Calibration iopm

        Returns:
            IOPhaseGuiManager: The calibration io manager
        """
        return self._iopm_cali

    @property
    def fret(self) -> 'IOPhaseGuiManager':
        """ Getter of the Fret iopm

        Returns:
            IOPhaseGuiManager: The fret io manager
        """
        return self._iopm_fret

    @property
    def iom(self) -> 'IOManager':
        """ Getter of the IOManager

        Returns:
            IOPhaseGuiManager: The fret io manager
        """
        return self._iopm


class IOPhaseGuiManager(IOPhaseManager):
    """ IOPhaseManager decorator for Qt GUI application.

    It provides an access, from a given phase, to a single istance to the
    application's Config, SeriesManager, ResultsManager and StageParams.

    It manage the selection, saving and restoration of config and already
    computed results in between two runs of the application. It also provide
    a default config if none exists.

    When the Config, SeriesManager, and ResultsManager are modified, in
    addition to the IOPhaseManager default behavior, the signal `stateChanged`
    is emitted. For the Config, it is also saved automatically.

    When using this class, you are expected to call all the time the getter
    properties to get config, series manager or result manager in case they
    changed since last call.

    To work properly, it stores the following information in the system:
        * [user_state_dir]/active_config_path.txt: File containing the path to
            the active configuration.
        * [user_config_dir]/user_configs: Default location for user configs
        * base_config.ini: Path of the base config
        * [user_data_dir]/output: Default output dir location
    See platformdirs to know where are located the folder starting with "user_"

    You must load a config before calling the different getters.

    This class emit the following signals:
        * `stateChanged`: The state of the IO changed (either config, series
            or results).
        * `noConfig`: There is no more config attached to the manager.
        * `errorConfig`: An error occured while loading the config. Send the
            path to the config that was being loaded and the associated
            error and trace
    """
    class ConfigChangeMode(Enum):
        """ Mode describing the behavior when changing the config path.

        Can be:
            * CHANGE: We are selecting a new existing config without touching
                the old one
            * NEW: We are creating a new config with default values without
                touching the old one
            * DUPLICATE: We are creating a new config by copying the values
                of the old one. The old one if not modified
            * DELETE: We are selecting a new existing config and we are
                deleting the old one.
        """
        CHANGE = 0
        NEW = 1
        DUPLICATE = 2
        DELETE = 3

    class SignalEmmiter(QObject):
        """ This class is needed because Multiple inheritance with QObject
        doesn't work with PyQt
        """
        stateChanged = Signal()
        noConfig = Signal()
        errorConfig = Signal(Path, str, str)

    def __init__(self, phase: str) -> None:
        """Constructor
        """
        super().__init__(phase, load_series=False)

        self._iopm: IOPhaseManager
        if phase == 'calibration':
            self._iopm = CalibrationIOPhaseManager(load_series=False)
        elif phase == 'fret':
            self._iopm = FretIOPhaseManager(load_series=False)
        else:
            raise QtfException(f'Unknown phase "{phase}"')
        self._iopm._object_to_update = self

        # App folders and files
        self._configs_dir = AppDefaultPath.configs_dir(phase)
        self._outputs_dir = AppDefaultPath.output_dir(phase)
        self._base_config_path = AppDefaultPath.base_config_file(phase)
        self._active_config_path_file = \
            AppDefaultPath.active_config_path_file(phase)
        self._config_path: Path | None = None

        # Instanciate a SignalEmmiter
        self._signal_emitter = IOPhaseGuiManager.SignalEmmiter()

    @property
    def stateChanged(self) -> SignalInstance:
        """ Get the stateChanged signal

        Returns:
            SignalInstance: the stateChanged signal
        """
        return self._signal_emitter.stateChanged

    @property
    def noConfig(self) -> SignalInstance:
        """ Get the noConfig signal

        Returns:
            SignalInstance: the noConfig signal
        """
        return self._signal_emitter.noConfig

    @property
    def errorConfig(self) -> SignalInstance:
        """ Get the errorConfig signal

        Returns:
            SignalInstance: the errorConfig signal
        """
        return self._signal_emitter.errorConfig

    def load_config(self, config_path: PathLike | str) -> None:
        """ Load a new config from the given file

        If the config file doesn't exists, it creates one with default values.

        Args:
            config_path (os.PathLike | str): Path to the config to load.
        """
        # Set new config
        config_path = Path(config_path)
        self._generate_default_config(config_path)
        try:
            self._iopm.load_config(config_path)
        except Exception as e:
            self.errorConfig.emit(config_path, str(e), traceback.format_exc())
            raise e
        self._config_path = config_path
        self._save_active_config_path()

        # Emit signal
        self.stateChanged.emit()

    def reset_config(self) -> None:
        """ Reset internal state by setting all parameters to None.

        The  iom can't be used without a `load_config` after that.
        """
        self._iopm.reset_config()
        self._config_path = None
        self._save_active_config_path()
        self.noConfig.emit()

    @property
    def config(self) -> Config:
        return self._iopm.config

    @property
    def series(self) -> QtfSeriesManager:
        return self._iopm.series

    @property
    def results(self) -> ResultsManager:
        return self._iopm.results

    @property
    def params(self) -> StageParams:
        return self._iopm.params

    def link_iopm(self, other: 'IOPhaseManager | None') -> None:
        """ Link this IOPM to another one for specific notification

        Args:
            other (IOPhaseManager | None): IOPM to link
        """
        self._iopm.link_iopm(other)

    def external_config_update(self, section: str, key: str, val: Any) -> None:
        """ Signal that the config of the IOPM linked to self has been updated

        Args:
            section (str): Section updated
            key (str): Key updated
        """
        self._iopm.external_config_update(section, key, val)

    def change_config(self, path: Path | None, mode: ConfigChangeMode) -> bool:
        """ Change the config path.

        Depending of the mode, the new config will be filled with specific
        values, and the old config can be deleted.

        If the path is set to None, the  iom will be reset.

        Args:
            path (Path | None): New config  path, if None is set, the  iom will
                be reset.
            mode (ConfigChangeMode): Mode to use to set the new path (see
                ConfigChangeMode class for more details)

        Returns:
            bool: True if the config changed, False if an error occured
        """
        Mode = self.ConfigChangeMode
        old_config_path = self._config_path

        # Set new config
        if path is not None:
            # Create new config if needed
            save = mode in [Mode.NEW, Mode.DUPLICATE]
            copy = mode == Mode.DUPLICATE
            if save:
                if self._iopm.config is not None and copy:
                    config = self._iopm.config
                else:
                    config = self._create_standalone_config()
                if not copy:
                    config.set_default()
                    config.set('Output', 'output_dir', self._outputs_dir)
                config.save(path)

        # Delete old config if needed
        delete_old = mode == Mode.DELETE
        if delete_old:
            if old_config_path is not None:
                old_config_path.unlink()
            self._config_path = path
            self._save_active_config_path()

        if path is None:
            self.reset_config()
        else:
            try:
                self.load_config(path)
            except Exception:
                return False

        return True

    def load_active_config(self) -> bool:
        """ load the active config if set. If not set, returns False.

        It reads the location of the active config in the file
        self._active_config_path_file.

        Returns:
            bool: True if the config was loaded, false otherwise.
        """
        config_path = self.get_active_config_path()

        if config_path is None:
            return False
        else:
            try:
                self.load_config(config_path)
                return True
            except Exception:
                return False

    def load_base_config(self) -> bool:
        """ Load the user's base config.

        The user base config is a config file that is located in a user's
        home folder associated with the app. It is generated if it doesn't
        exists. It's location is described in AppDefaultPath.base_config_file()

        Returns:
            bool: True if the config was loaded, False if an error occured
        """
        try:
            self.load_config(self._base_config_path)
            return True
        except Exception:
            return False

    def _updated_config(self, section: str, key: str) -> None:
        """ Signal that the config has been updated

        This
            * catches the changes in input path and output path
            * Saves the config
            * Emits the `stateChanged` signal

        Args:
            section (str): Section updated
            key (str): Key updated
        """
        assert self._config_path is not None
        if self._iopm._allow_updates:
            self._iopm._updated_config(section, key)
            self.config.save(self._config_path)
            self.stateChanged.emit()

    def _updated_series(self, name: str) -> None:
        """ Signal that the series have been updated

        Emit the `stateChanged` signal

        Args:
            name (str): Name of the series updated
        """
        if self._iopm._allow_updates:
            self._iopm._updated_series(name)
            self.stateChanged.emit()

    def _updated_results(self, stage: str):
        """ Signal that the results have been updated

        Emit the `stateChanged` signal

        Args:
            stage (str): Stage updated
        """
        if self._iopm._allow_updates:
            self._iopm._updated_results(stage)
            self.stateChanged.emit()

    def _updated_params(self):
        """ Signal that the stage params have been updated

        Emit the `stateChanged` signal
        """
        if self._iopm._allow_updates:
            self._iopm._updated_params()
            self.stateChanged.emit()

    def get_active_config_path(self) -> Path | None:
        """ Get the path to the active config if it exists.

        Returns:
            Path | None: Path to the active config if it exists
        """
        # Generate the active config path file
        self._generate_active_config_path_file()
        # Read the config and returns it
        with open(self._active_config_path_file, 'r') as f:
            config_path_str = f.read()
        if config_path_str.rstrip() == "":
            return None
        return Path(config_path_str)

    def _generate_active_config_path_file(self) -> None:
        """ Generate the active config path file if it doesn't exists
        """
        if not self._active_config_path_file.is_file():
            if self._active_config_path_file.exists():
                err = 'Path to store active config exists and is not a file: '
                err += f'{self._active_config_path_file}'
                raise QtfException(err)
            self._active_config_path_file.parent.mkdir(parents=True,
                                                       exist_ok=True)
            self._active_config_path_file.touch()

    def _save_active_config_path(self) -> None:
        """ Save the current config path in the active config path file
        """
        self._generate_active_config_path_file()
        if self._config_path is None:
            path = ""
        else:
            path = str(self._config_path)
        with open(self._active_config_path_file, 'w') as f:
            f.write(path)

    def _generate_default_config(self, path: Path) -> None:
        """ Generate the config file passing default values if it doesn't
        already exists

        Args:
            path (Path): Path to the config to generate.
        """
        if not path.is_file():
            if path.exists():
                err = 'Config path exists and is not a file: ' \
                      f'{path}'
                raise QtfException(err)
            path.parent.mkdir(parents=True, exist_ok=True)
            config = self._create_standalone_config()
            config.set_default()
            config.set('Output', 'output_dir', self._outputs_dir)
            config.save(path)

    def _create_standalone_config(self) -> Config:
        """ Getter of the Config class associated with the manager

        Returns:
            CalibrationConfig | FretConfig: Config class associated
        """
        if self._phase == 'calibration':
            return CalibrationConfig()
        elif self._phase == 'fret':
            return FretConfig()
        else:
            raise QtfException('Unknown type')
