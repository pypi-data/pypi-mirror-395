from quanti_fret.apps.cli.view.printers import print_bullet_list
from quanti_fret.apps.cli.view.stage_view import StageView

from quanti_fret.algo import (
    BackgroundEngine, BackgroundEngineDisabled, BackgroundEngineFixed,
    BackgroundEngineMask, BackgroundEnginePercentile
)
from quanti_fret.core import QtfSeries, QtfException
from quanti_fret.io import IOPhaseManager


class CalculationView(StageView):
    """ Classes that handle the display of calculation stages

    This class uses an IOPhaseManager to fetche the information to display
    with:
        * IOPhaseManager.params for the settings
        * IOPhaseManager.results for the results

    To specify this class for each stage, you need to pass to the constrcutor
        * The title to display
        * The description of each settings values that are returned by the
            `StageParam.get` associated with the stage. The descriptions should
            be a list of str having the same order than the values returned
        * The description of each results values that will be returned by the
            `ResultsManager.get`methods. The descriptions should be a list of
            str having the same order than the results returned.
    """

    def __init__(
        self, stage: str, title: str, settings_keys: list[str],
        results_keys: list[str], iopm: IOPhaseManager, separator_lenth: int
    ) -> None:
        """ Constructor

        Args:
            title (str): The title to display
            settings_keys (list[str]): The keys to display for the settings
            results_keys (list[str]): The keys to deisplay for the results
            iopm (IOPhaseManager): iopmanage used to get the information to
                display
            separator_lenth (int): The expected length for the separators
        """
        super().__init__(title, separator_lenth)
        self._stage = stage
        self._settings_keys = settings_keys
        self._results_keys = results_keys
        self._iopm = iopm

    def settings(self) -> None:
        """ Print the settings of the stage

        Fetches the results using the `IOPhaseManager.params.get` methods, and
        transform the series used into an integer representing its length.
        """
        params = self._iopm.params.get(self._stage)
        assert len(params) == len(self._settings_keys)
        print('Settings:')
        lines: list[str] = []
        for line in zip(self._settings_keys, params):
            descr = line[0]
            val = line[1]
            if isinstance(val, BackgroundEngine):
                if isinstance(val, BackgroundEngineFixed):
                    lines.append(f'{descr} Mode: {3}')
                    lines.append(f'{descr} Value: {val.background}')
                elif isinstance(val, BackgroundEngineDisabled):
                    lines.append(f'{descr} Mode: {0}')
                elif isinstance(val, BackgroundEngineMask):
                    lines.append(f'{descr} Mode: {1}')
                elif isinstance(val, BackgroundEnginePercentile):
                    lines.append(f'{descr} Mode: {2}')
                    lines.append(f'{descr} Percentile: {val._percentile}')
                else:
                    err = f'Expected engine value "{val}" has wrong type'
                    raise QtfException(err)
            else:
                if type(val) is QtfSeries:
                    val = val.size
                lines.append(f'{descr}: {val}')
        print_bullet_list(1, lines)

    def results(self) -> None:
        """ Print the results of the stage
        """
        results = self._iopm.results[self._stage].get_stage_results()
        if results is None:
            raise QtfException("Results can't be retrieved")
        assert len(results) == len(self._results_keys)
        if len(results) == 0:
            print('Computing Done!')
        else:
            print('Results:')
            results_list = list(results)
            for i in range(len(results)):
                res = results_list[i]
                if isinstance(res, BackgroundEngine):
                    if isinstance(res, BackgroundEngineFixed):
                        results_list[i] = res.background
                    elif isinstance(res, BackgroundEngineDisabled):
                        results_list[i] = 'Disabled'
                    else:
                        err = f'Expected engine value "{res}" has wrong type'
                        raise QtfException(err)
            lines = [
                f'{line[0]}: {line[1]}' for line in zip(self._results_keys,
                                                        results_list)
            ]
            print_bullet_list(1, lines)
