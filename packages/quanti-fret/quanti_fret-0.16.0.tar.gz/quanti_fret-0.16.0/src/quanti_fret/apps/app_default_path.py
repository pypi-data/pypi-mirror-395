from quanti_fret.core import QtfException

import functools
from pathlib import Path
from typing import Callable

from platformdirs import PlatformDirs


class AppDefaultPath:
    """ Class to get the path to the app defaults files and directory.

    It gives access, for a given phase, to the path to the:
        * file containing the active config
        * defaults config directories
        * base config used if no config is specified
        * default output directory
    """
    @staticmethod
    def check_phase(func: Callable[[str], Path]) -> Callable[[str], Path]:
        """ Decorator that check if the phase is valid
        """
        functools.wraps(func)

        def wrapper_check_phase(phase: str) -> Path:
            if phase not in ['calibration', 'fret']:
                raise QtfException(f'Unknown phase "{phase}"')
            return func(phase)

        return wrapper_check_phase

    @staticmethod
    @check_phase
    def active_config_path_file(phase: str) -> Path:
        """ Get the path to the file containing the active config

        Args:
            pase (str): phase to get values from

        Returns:
            Path: file path
        """
        dir = AppDefaultPath.__get_dir()
        filename = f'active_{phase}_config_path.txt'
        return Path(dir.user_state_dir) / filename

    @staticmethod
    @check_phase
    def configs_dir(phase: str) -> Path:
        """ Get the path to to the defaults config directories

        Args:
            pase (str): phase to get values from

        Returns:
            Path: dir path
        """
        dir = AppDefaultPath.__get_dir()
        return Path(dir.user_config_dir) / 'user_configs' / phase

    @staticmethod
    @check_phase
    def base_config_file(phase: str) -> Path:
        """ Get the path to the base config used if no config is specified

        Args:
            pase (str): phase to get values from

        Returns:
            Path: file path
        """
        return AppDefaultPath.configs_dir(phase) / f'base_{phase}_config.ini'

    @staticmethod
    @check_phase
    def output_dir(phase: str) -> Path:
        """ Get the path to to the default output directory

        Args:
            pase (str): phase to get values from

        Returns:
            Path: dir path
        """
        dir = AppDefaultPath.__get_dir()
        return Path(dir.user_data_dir) / 'output' / phase

    @staticmethod
    def __get_dir() -> PlatformDirs:
        """ Get the platformDirs associated with the QuanTI-FRET app

        Args:
            pase (str): phase to get values from

        Returns:
            PlatformDirs: PlatformDirs associated with the app
        """
        return PlatformDirs('QuanTI-FRET', 'LIPhy')
