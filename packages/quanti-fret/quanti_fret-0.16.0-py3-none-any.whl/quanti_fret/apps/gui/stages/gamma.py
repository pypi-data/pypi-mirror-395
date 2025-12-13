from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.popup import PopUpManager
from quanti_fret.apps.gui.stages.stage_calculation import StageCalculatorWidget
from quanti_fret.apps.gui.stages.results_table import TripletResultsTable
from quanti_fret.apps.gui.utils import (
    BackgroundResultCells, PercentileSpinBox, ResultCells
)
from quanti_fret.core import QtfException

from qtpy.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StageGammaWidget(StageCalculatorWidget):
    """ Handle the stage that computes the BT or DE stages.
    """

    def __init__(self, mode: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            mode (str): Weather this widget is in BT or DE mode
        """
        self._mode = mode
        if mode == 'BT':
            self._gamma_type = 'bt'
            self._series_name = 'donors'
            self._gamma_channel = 'DD'
            self._gamma_background_index = 0
            self._gamma_name = 'Alpha BT'
        elif mode == 'DE':
            self._gamma_type = 'de'
            self._series_name = 'acceptors'
            self._gamma_channel = 'AA'
            self._gamma_background_index = 2
            self._gamma_name = 'Delta DE'
        else:
            QtfException(
                'Invalid StageGammaWidget type. Must be in ["BT", "DE"]'
            )

        super().__init__(
            self._gamma_type, IOGuiManager().cali, *args, showProgress=True,
            **kwargs
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

        # Locked settings
        lockedSettingsBox = QGroupBox('Locked', parent=parent)
        settingsLayout.addWidget(lockedSettingsBox)
        lockedSettingsLayout = QGridLayout()
        lockedSettingsBox.setLayout(lockedSettingsLayout)
        self._sSeries = ResultCells(
            lockedSettingsBox, 'Series', lockedSettingsLayout, 0)
        self._sSeries.setLocked(True)
        self._sBackground = BackgroundResultCells(
            lockedSettingsBox, 'Background', lockedSettingsLayout, 1)
        self._sBackground.setLocked(True)

        # Other settings
        btSettingsBox = QGroupBox(self._gamma_type.upper(), parent=parent)
        settingsLayout.addWidget(btSettingsBox)
        btSettingsLayout = QGridLayout()
        btSettingsBox.setLayout(btSettingsLayout)

        # percentile
        sPercentilelabel = QLabel(
            'Discard Low Percentile:', parent=btSettingsBox
        )
        btSettingsLayout.addWidget(sPercentilelabel, 0, 0)
        self._sPercentileBox = PercentileSpinBox(parent=btSettingsBox)
        self._sPercentileBox.valueChanged.connect(self._set_percentile)
        # self._sPercentileBox.setSizePolicy(
        #     QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        # )
        btSettingsLayout.addWidget(self._sPercentileBox, 0, 1)

        # Details
        sPlotDetailLabel = QLabel(
            'Plot Sequences Details:', parent=btSettingsBox
        )
        btSettingsLayout.addWidget(sPlotDetailLabel, 1, 0)
        self._sPlotDetailsBox = QCheckBox(parent=btSettingsBox)
        btSettingsLayout.addWidget(self._sPlotDetailsBox, 1, 1)
        self._sPlotDetailsBox.stateChanged.connect(self._set_plot_details)

        return settingsLayout

    def _buildResultsStage(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the results of the Stage. If None
        is returned, will not create this box

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout | None: Results layout created
        """
        layout = QGridLayout()
        self._rGamma = ResultCells(parent, self._gamma_name, layout, 0)
        self._rGamma.setBold(True)
        self._rStd = ResultCells(parent, 'Standard Deviation', layout, 1)
        self._rStd.setBold(False)
        self._rNbPix = ResultCells(parent, 'Nb Pixels', layout, 2)
        self._rNbPix.setBold(False)
        return layout

    def _buildResultsSetting(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the settings used to compute
        the results. If None is returned, will not create this box

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout | None: Results layout created
        """
        layout = QGridLayout()
        self._rSeries = ResultCells(parent, 'Series name', layout, 0)
        self._rNbSeq = ResultCells(parent, 'Nb Sequences', layout, 1)
        self._rBckg = BackgroundResultCells(parent, 'Background', layout, 2)
        self._rPercentile = ResultCells(
            parent, 'Discard Low Percentile', layout, 3
        )
        self._rPlotDetails = ResultCells(parent, 'Plot Details', layout, 4)
        return layout

    def _buildResultsPlots(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the stage plots buttons. If None
        is returned, will not create this box

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout | None: Results layout created
        """
        layout = QVBoxLayout()
        self._rScatterButton = QPushButton('Scatter Plot', parent=parent)
        self._rScatterButton.clicked.connect(
            lambda: self._openStageFigure('scatter', 'Scatter Plot')
        )
        self._rBoxplotButton = QPushButton('Box Plot', parent=parent)
        self._rBoxplotButton.clicked.connect(
            lambda: self._openStageFigure('boxplot', 'Box Plot')
        )
        layout.addWidget(self._rScatterButton)
        layout.addWidget(self._rBoxplotButton)
        return layout

    def _buildResultsTripletsTable(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the results triplet table. If None
        is returned, will not create this box

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout: Results layout created
        """
        layout = QVBoxLayout()
        rTripletTable = TripletResultsTable(
            'calibration', self._gamma_type, parent=parent, hasPlot=True,
            detailIndex=4
        )
        rTripletTable.plotClicked.connect(self._openSequenceDetail)
        layout.addWidget(rTripletTable)
        return layout

    def _blockAllSignals(self, val: bool) -> None:
        """ Call the `blockSignal` method of all widget whose signal is
        connected to a slot.

        The purpose of this method is to prevent slots to call config save
        while being updated by it.

        Args:
            val (bool): The value to pass to the `blockSignal` method
        """
        self._sPercentileBox.blockSignals(val)
        self._sPlotDetailsBox.blockSignals(val)

    def _updateSettings(self) -> None:
        """ Update the number of sequences for each series
        """
        # Retrieve params
        params = self._iopm.params.get(self._gamma_type, True)
        _, series, background, percentile, plotDetails = params

        # Series
        text = f'{self._series_name.capitalize()} ({series.size})'
        self._sSeries.setResult(text)

        # Background
        self._sBackground.setResult(background)

        # percentile
        percentile = self._iopm.config.get(self._mode,
                                           'discard_low_percentile')
        self._sPercentileBox.setValue(percentile)

        # Plot details
        plotDetails = self._iopm.config.get(self._mode,
                                            'plot_sequence_details')
        self._sPlotDetailsBox.setChecked(plotDetails)

    def _loadResults(self) -> bool:
        """ Load the results, update the results widget. and inform if results
        were found.

        Returns:
            bool: True if results were loaded, False otherwise
        """
        # Retrieve settings and results
        settings = self._iopm.results[self._stage].get_stage_settings()
        if settings is None:
            return False
        series, nb_seq, background, percentile, plotDetails = settings
        results = self._iopm.results[self._stage].get_stage_results()
        if results is None:
            return False
        gamma, std_dev, nb_pix = results

        # Update settings
        self._rSeries.setResult(series)
        self._rNbSeq.setResult(nb_seq)
        self._rBckg.setResult(background)
        self._rPercentile.setResult(percentile)
        self._rPlotDetails.setResult(plotDetails)

        # Update results
        self._rGamma.setResult(gamma)
        self._rStd.setResult(std_dev)
        self._rNbPix.setResult(nb_pix)

        # Update Stage plot buttons
        figures = self._iopm.results[self._stage].get_stage_extras(
            check_only=True
        )
        self._rScatterButton.setEnabled(figures['scatter'])
        self._rBoxplotButton.setEnabled(figures['boxplot'])

        return True

    def _set_percentile(self, val: float) -> None:
        """ Set the percentile value in the config

        Args:
            val (float): Value to set
        """
        self._iopm.config.set(self._mode, 'discard_low_percentile', val)

    def _set_plot_details(self, _: bool) -> None:
        """Set the plot sequence details value in the config

        Args:
            _ (bool): Not used, we get the checked directly from widget
        """
        checked = self._sPlotDetailsBox.isChecked()
        self._iopm.config.set(self._mode, 'plot_sequence_details', checked)

    def _openStageFigure(self, key: str, title: str) -> None:
        """ Open a stage figure in a new window

        Args:
            key (str): Key of the figure in the extra figures dict
            title (str): Title of the dialog to open
        """
        valid = self._iopm.results[self._stage].get_stage_extras(key, True)
        if valid[key]:
            title = f'{self._stage.upper()} - {title}'
            extras = self._iopm.results[self._stage].get_stage_extras(key)
            PopUpManager().openFigure(extras[key], title)

    def _openSequenceDetail(self, id: int) -> None:
        """ Open the details of a sequence in a new window.
        """
        preTitle = f'{self._stage.upper()} - Seq #{id}'
        res = self._iopm.results[self._stage].get_triplet_extras(id)
        if res['hist_2d'] is not None:
            title = f'{preTitle} - 2D Histogram'
            PopUpManager().openFigure(res['hist_2d'], title)
        if res['gamma'] is not None:
            title = f'{preTitle} - Gamma'
            PopUpManager().openFigure(res['gamma'], title)
