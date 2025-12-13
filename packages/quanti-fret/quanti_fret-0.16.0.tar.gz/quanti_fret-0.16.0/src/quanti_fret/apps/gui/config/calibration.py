from quanti_fret.apps.gui.config.config import ConfigManagementWidget
from quanti_fret.apps.gui.utils import (
    BackgroundResultCells, HLine, ResultCells
)

from qtpy.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QVBoxLayout,
)


class CalibrationConfigManagementWidget(ConfigManagementWidget):
    """ Handle the selection and creation of config files of calibration phase.

    It also display the summary results of the calibration if any.
    """
    def __init__(self, *args, **kwargs) -> None:
        """ Constructor
        """
        super().__init__('calibration', *args, **kwargs)

    def _buildSeparator(self) -> None:
        """ Build the separator line between config management and results
        """
        horizontal_line = HLine(parent=self)
        self.layout().addWidget(horizontal_line)  # type: ignore

    def _buildPhaseSummary(self) -> None:
        """ Build the widgets to show the Calibration results
        """
        # Result layout
        resultLayout = QVBoxLayout()
        self.layout().addLayout(resultLayout)  # type: ignore

        # Result settings box
        box = QGroupBox('Results from Current Config', parent=self)
        resultLayout.addWidget(box)
        grid = QGridLayout()
        box.setLayout(grid)

        # Results
        self._rBackground = BackgroundResultCells(box, 'Background', grid, 0)
        self._rAlphaBt = ResultCells(box, 'AlphaBT', grid, 1)
        self._rDeltaDe = ResultCells(box, 'DeltaDE', grid, 2)
        self._rBetaX = ResultCells(box, 'BetaX', grid, 3)
        self._rGammaM = ResultCells(box, 'GammaM', grid, 4)
        self._rBackground.setBold(True)
        self._rAlphaBt.setBold(True)
        self._rDeltaDe.setBold(True)
        self._rBetaX.setBold(True)
        self._rGammaM.setBold(True)

    def _updateResults(self) -> None:
        """Update the calibration results
        """
        background = None
        alphaBT = None
        deltaDE = None
        betaX = None
        gammaM = None

        res = self._iopm.results['background'].get_stage_results()
        if res is not None:
            background = res[0]

        res = self._iopm.results['bt'].get_stage_results()
        if res is not None:
            alphaBT = str(res[0])

        res = self._iopm.results['de'].get_stage_results()
        if res is not None:
            deltaDE = str(res[0])

        res = self._iopm.results['xm'].get_stage_results()
        if res is not None:
            betaX = res[0]
            gammaM = res[1]

        self._rBackground.setResult(background)
        self._rAlphaBt.setResult(alphaBT)
        self._rDeltaDe.setResult(deltaDE)
        self._rBetaX.setResult(betaX)
        self._rGammaM.setResult(gammaM)
