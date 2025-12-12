from quanti_fret.apps.gui.stages.background.mode import BackgroundModeBox
from quanti_fret.apps.gui.stages.background.floating import (
    FloatingBackgroundBox
)
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.stages.stage_calculation import StageCalculatorWidget
from quanti_fret.apps.gui.utils import ResultCells

from quanti_fret.algo import BackgroundMode

from qtpy.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QGridLayout,
    QLabel,
    QLayout,
    QVBoxLayout,
    QWidget,
)


class StageBackgroundWidget(StageCalculatorWidget):
    """ Handle the stage that computes the background for the calibration phase
    """

    def __init__(self, *args, **kwargs) -> None:
        """Constructor

        Args:
            phase (str): Phase of the widget
        """
        # Must be instanciated before super init
        self._seriesCheckBox: dict[str, QCheckBox] = {}
        self._phase = 'calibration'

        super().__init__('background', IOGuiManager().cali, *args, **kwargs)

        # Must be done after super init to avoid useless signal emission
        for name in self._seriesCheckBox:
            self._seriesCheckBox[name].stateChanged.connect(
                lambda val, name=name: self._select_series(name, val)
            )

    def _buildSettings(self, parent: QWidget) -> QLayout:
        """ Create the settings QLayout that will be added to the top of the
        widget layout.

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout: Settings layout created
        """
        settingsLayout = QVBoxLayout()

        # Floating Box
        floatingBox = FloatingBackgroundBox(self._phase, parent=parent)
        settingsLayout.addWidget(floatingBox)

        # Mode Box
        self._modeBox = BackgroundModeBox(self._phase, parent=parent)
        settingsLayout.addWidget(self._modeBox)

        # Series Button
        self._seriesBox = QGroupBox('Series', parent=parent)
        settingsLayout.addWidget(self._seriesBox)
        seriesLayout = QVBoxLayout()
        self._seriesBox.setLayout(seriesLayout)
        for name in self._iopm.series._series:
            self._seriesCheckBox[name] = QCheckBox(
                name, parent=self._seriesBox
            )
            seriesLayout.addWidget(self._seriesCheckBox[name])

        return settingsLayout

    def _buildResultsStage(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the results of the Stage

        Returns:
            QLayout: Results layout created
        """
        layout = QGridLayout()

        self._ddResult = ResultCells(parent, 'DD', layout, 0, 0)
        self._ddResult.setBold(True)

        self._daResult = ResultCells(parent, 'DA', layout, 0, 2)
        self._daResult.setBold(True)

        self._aaResult = ResultCells(parent, 'AA', layout, 0, 4)
        self._aaResult.setBold(True)

        self._disabledResult = QLabel('Disabled', parent=parent)
        layout.addWidget(self._disabledResult, 1, 0)
        font = self._disabledResult.font()
        font.setBold(True)
        self._disabledResult.setFont(font)

        return layout

    def _buildResultsSetting(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the settings used to compute
        the results

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout: Results layout created
        """
        layout = QGridLayout()

        self._seriesResult = ResultCells(parent, 'Series', layout, 0)
        self._seqCountResult = ResultCells(parent, 'Nb Sequences', layout, 1)
        self._modeResult = ResultCells(parent, 'Mode', layout, 2)
        self._extraInfoResult = ResultCells(parent, '', layout, 3)

        return layout

    def _blockAllSignals(self, val: bool) -> None:
        """ Call the `blockSignal` method of all widget whose signal is
        connected to a slot.

        The purpose of this method is to prevent slots to call config save
        while being updated by it.

        Args:
            val (bool): The value to pass to the `blockSignal` method
        """
        for name in self._seriesCheckBox:
            self._seriesCheckBox[name].blockSignals(val)

    def _updateSettings(self) -> None:
        """ Update the number of sequences for each series
        """
        # Series
        for name in self._seriesCheckBox:
            checked = self._iopm.config.get('Background', f'use_{name}')
            self._seriesCheckBox[name].setChecked(checked)
            nb_elements = self._iopm.series.get(name).size
            self._seriesCheckBox[name].setText(f'{name} ({nb_elements})')

        # Disabled what is needed
        floating = self._iopm.config.get('Background', 'floating')
        if floating:
            self._seriesBox.setEnabled(False)
        else:
            self._seriesBox.setEnabled(True)

    def _loadResults(self) -> bool:
        """ Load the results, update the results widget. and inform if results
        were found.

        Returns:
            bool: True if results were loaded, False otherwise
        """
        # Retrieve settings and results
        settings = self._iopm.results['background'].get_stage_settings()
        if settings is None:
            return False
        series, nbSequences, engine = settings
        results = self._iopm.results['background'].get_stage_results()
        if results is None:
            return False
        background, = results

        # Update settings results
        self._seriesResult.setResult(','.join(series))
        self._seqCountResult.setResult(nbSequences)
        self._modeResult.setResult(engine.mode)
        if engine.mode == BackgroundMode.PERCENTILE:
            self._extraInfoResult.setTitle('Percentile')
            self._extraInfoResult.setResult(engine._percentile)
            self._extraInfoResult.show()
        elif engine.mode == BackgroundMode.FIXED:
            self._extraInfoResult.setTitle('Fixed Value')
            self._extraInfoResult.setResult(engine.background)
            self._extraInfoResult.show()
        else:
            self._extraInfoResult.hide()

        # Update background results
        if background.mode == BackgroundMode.DISABLED:
            self._ddResult.hide()
            self._daResult.hide()
            self._aaResult.hide()
            self._disabledResult.show()
        else:
            self._ddResult.show()
            self._daResult.show()
            self._aaResult.show()
            self._disabledResult.hide()
            self._ddResult.setResult(background.background[0])
            self._daResult.setResult(background.background[1])
            self._aaResult.setResult(background.background[2])

        return True

    def _select_series(self, name: str, _: int) -> None:
        """ Select or unselect the series for background computation

        Args:
            name (str): name of the series to set
        """
        checked = self._seriesCheckBox[name].isChecked()
        self._iopm.config.set('Background', f'use_{name}', checked)
