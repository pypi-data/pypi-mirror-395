from quanti_fret.apps.cli.view.calculation_view import CalculationView
from quanti_fret.apps.cli.view.printers import print_error, print_phase
from quanti_fret.apps.cli.view.series_view import SeriesView
from quanti_fret.apps.cli.view.stage_view import StageView

from quanti_fret.core import QtfException
from quanti_fret.io import IOManager


class CliView:
    """ Handles the display in CLI mode.
    """
    def __init__(self, iom: IOManager):
        """ Constructor

        Creates the differents stage views.

        Args:
            iom (IOeManager): IOManager used in the view to get the fret and
                calibration IOPhaseManager to get the informations to display
        """
        self._separator_length = 80
        self._current_stage = 'series'
        self._current_phase = 'calibration'
        self._phases: dict[str, dict[str, StageView]] = {
            'calibration': {
                'series': SeriesView(
                    iom.cali,
                    self._separator_length,
                    ['donors', 'acceptors', 'standards']
                ),
                'background': CalculationView(
                    'background',
                    'Computing background',
                    ['Series', 'Number of sequences used', 'Background'],
                    ['Background'],
                    iom.cali,
                    self._separator_length
                ),
                'bt': CalculationView(
                    'bt',
                    'Computing Alpha_BT (BleedThrough)',
                    ['Series Name', 'Number of sequences used',
                     'Background',
                     'Discard Low Percentile',
                     'Plot sequence Details'],
                    ['Alpha BT', 'Standard Deviation', 'Number of Pixels'],
                    iom.cali,
                    self._separator_length
                ),
                'de': CalculationView(
                    'de',
                    'Computing Delta_DE (Direct Excitation)',
                    ['Series Name', 'Number of sequences used',
                     'Background',
                     'Discard Low Percentile',
                     'Plot sequence Details'],
                    ['Delta DE', 'Standard Deviation', 'Number of Pixels'],
                    iom.cali,
                    self._separator_length
                ),
                'xm': CalculationView(
                    'xm',
                    'Computing GammaXM',
                    ['Series Name', 'Number of sequences used', 'Alpha BT',
                     'Delta DE', 'Background', 'Keep Percentile Range',
                     'Save Analysis Details', 'Sampling for Analysis'],
                    ['BetaX', 'GammaM', 'RedChi2', 'R2', 'Q'],
                    iom.cali,
                    self._separator_length
                ),
            },
            'fret': {
                'series': SeriesView(
                    iom.fret,
                    self._separator_length,
                    ['experiments']
                ),
                'fret': CalculationView(
                    'fret',
                    'Computing Fret',
                    ['Series Name', 'Number of sequences used', 'Alpha BT',
                     'Delta DE', 'BetaX', 'GammaM', 'Background',
                     'Sigma S', 'Targer S', 'Sigma Gauss', 'Weights Threshold',
                     'Save Analysis Details', 'Sampling for Analysis'],
                    [],
                    iom.fret,
                    self._separator_length
                ),
            }
        }

    def error(self, msg: str) -> None:
        """ Print an error message

        Args:
            msg (str): Error message to display
        """
        print_error(msg, self._separator_length)

    def phase(self, phase: str) -> None:
        """ Set the phase of the view and print its title.

        Args:
            phase (str): Phase to set

        Raises:
            QtfException: If the phase wdoesn't exists
        """
        if phase not in self._phases:
            raise QtfException(f'Unknown phase "{phase}"')
        self._current_phase = phase
        print_phase(f'Starting Phase: {phase.capitalize()}',
                    self._separator_length)

    def stage(self, stage: str) -> None:
        """ Set the stage of the view and print its title.

        Args:
            stage (str): Stage to set

        Raises:
            QtfException: If the stage wdoesn't exists
        """
        if stage not in self._phases[self._current_phase]:
            raise QtfException(f'Unknown stage "{stage}"')
        self._current_stage = stage
        self._phases[self._current_phase][stage].title()

    def settings(self) -> None:
        """ Display the settings of the current stage
        """
        self._phases[self._current_phase][self._current_stage].settings()

    def results(self) -> None:
        """ Display the results of the current stage
        """
        self._phases[self._current_phase][self._current_stage].results()
