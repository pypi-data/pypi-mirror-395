from quanti_fret.apps.cli.view import CliView
from quanti_fret.io import (
    CalibrationIOPhaseManager, FretIOPhaseManager, IOManager
)
from quanti_fret.run import QtfRunner

import functools
import os
import sys
import traceback


class CliController:
    """Controller for a Command Line Interface application.

    It works with:
        * An IOPhaseManager that will handle inputs and outputs
        * A QtfRunner that will run the different stages
        * A CliView that will handle the display

    It creates first the IOPhaseManager with the path to the config passed in
    argument. The iopmanage will handle the loading of the config and series.
    It will:
        * Display the series found
        * Run the background calculation
        * Run the BT calculation
        * Run the DE calculation
        * Run the XM calculation
    For each stage, it will call the view to display the stage title, the
    settings, and the results.
    """
    @staticmethod
    def catch_errors(func):
        """ Decorator that make sure to call the view error display and that
        exit the program if an error occurs.
        """
        @functools.wraps(func)
        def wrapper_catch_errors(*args, **kwargs):
            self = args[0]
            try:
                value = func(*args, **kwargs)
                return value
            except Exception:
                self._view.error(traceback.format_exc())
                sys.exit(-1)
        return wrapper_catch_errors

    def __init__(
        self,
        calibration_config_path: os.PathLike | str | None = None,
        fret_config_path: os.PathLike | str | None = None,
    ) -> None:
        """Constructor

        Args:
            config_path (os.PathLike | str): Path the the config file
        """
        iopm_cali = CalibrationIOPhaseManager(load_series=True)
        if calibration_config_path is not None:
            iopm_cali.load_config(calibration_config_path)
        iopm_fret = FretIOPhaseManager(load_series=True)
        if fret_config_path is not None:
            iopm_fret.load_config(fret_config_path)

        iom = IOManager(iopm_cali, iopm_fret)

        self._runner = QtfRunner(iom)
        self._view = CliView(iom)

    def run(self) -> None:
        """ Run the QuanTI-FRET application
        """
        self.run_calibration()
        self.run_fret()

    def run_calibration(self) -> None:
        """ Run the calibration phase
        """
        self._view.phase('calibration')
        self._print_series()
        self._run_background()
        self._run_bt()
        self._run_de()
        self._run_xm()

    def run_fret(self) -> None:
        """ Run the fret phase
        """
        self._view.phase('fret')
        self._print_series()
        self._run_fret_()

    @catch_errors
    def _run_fret_(self) -> None:
        """Run the Fret calculation stage
        """
        self._view.stage('fret')
        self._view.settings()
        self._runner.run_fret()
        self._view.results()

    @catch_errors
    def _print_series(self):
        self._view.stage('series')
        self._view.settings()
        self._view.results()

    @catch_errors
    def _run_background(self) -> None:
        """Run the Background computation
        """
        self._view.stage('background')
        self._view.settings()
        self._runner.run_background()
        self._view.results()

    @catch_errors
    def _run_bt(self) -> None:
        """Run the BT calculation
        """
        self._view.stage('bt')
        self._view.settings()
        self._runner.run_bt()
        self._view.results()

    @catch_errors
    def _run_de(self) -> None:
        """Run the DE calculation
        """
        self._view.stage('de')
        self._view.settings()
        self._runner.run_de()
        self._view.results()

    @catch_errors
    def _run_xm(self) -> None:
        """Run the XM calculation
        """
        self._view.stage('xm')
        self._view.settings()
        self._runner.run_xm()
        self._view.results()
