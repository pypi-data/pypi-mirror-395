from quanti_fret.core import QtfException
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.popup import PopUpManager
from quanti_fret.apps.gui.stages.results_table import TripletResultsTable
from quanti_fret.apps.gui.stages.stage_calculation import StageCalculatorWidget
from quanti_fret.apps.gui.utils import (
    BackgroundResultCells, ResultCells, PercentileSpinBox
)

import numpy as np

from qtpy.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QSpinBox,
    QLabel,
    QLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StageXmWidget(StageCalculatorWidget):
    """ Handle the stage that computes the BT or DE stages.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Constructor
        """
        # Mandatory in order to prevent saving config even if value didn't
        # change
        self._sPercentileLowValue = 0.0
        self._sPercentileHighValue = 0.0
        self._sAnalysisSamplingValue = 0

        super().__init__(
            'xm', IOGuiManager().cali, *args, showProgress=True, **kwargs
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
        self._sAlphaBt = ResultCells(
            lockedSettingsBox, 'AlphaBT', lockedSettingsLayout, 1)
        self._sAlphaBt.setLocked(True)
        self._sDeltaDe = ResultCells(
            lockedSettingsBox, 'DeltaDE', lockedSettingsLayout, 2)
        self._sDeltaDe.setLocked(True)
        self._sBackground = BackgroundResultCells(
            lockedSettingsBox, 'Background', lockedSettingsLayout, 3)
        self._sBackground.setLocked(True)

        # percentile
        percentileBox = QGroupBox('Percentile Range', parent=parent)
        settingsLayout.addWidget(percentileBox)
        percentileLayout = QHBoxLayout()
        percentileBox.setLayout(percentileLayout)
        percentileLowLayout = QHBoxLayout()
        percentileLayout.addLayout(percentileLowLayout)
        sPercentileLowlabel = QLabel('Low:', parent=percentileBox)
        self._sPercentileLowBox = PercentileSpinBox(parent=percentileBox)
        percentileLowLayout.addWidget(sPercentileLowlabel)
        percentileLowLayout.addWidget(self._sPercentileLowBox)
        percentileHighLayout = QHBoxLayout()
        percentileLayout.addLayout(percentileHighLayout)
        sPercentileHighlabel = QLabel('High:', parent=percentileBox)
        self._sPercentileHighBox = PercentileSpinBox(parent=percentileBox)
        percentileHighLayout.addWidget(sPercentileHighlabel)
        percentileHighLayout.addWidget(self._sPercentileHighBox)
        self._sPercentileLowBox.editingFinished.connect(self._setPercentileLow)
        self._sPercentileHighBox.editingFinished.connect(
            self._setPercentileHigh)

        # analysis
        analysisBox = QGroupBox('Analysis Details', parent=parent)
        settingsLayout.addWidget(analysisBox)
        analysisLayout = QHBoxLayout()
        analysisBox.setLayout(analysisLayout)
        self._sAnalysisDetailsCheckBox = QCheckBox(
            'Save Details', parent=analysisBox)
        self._sAnalysisDetailsCheckBox.stateChanged.connect(
            self._setAnalysisDetails)
        analysisLayout.addWidget(self._sAnalysisDetailsCheckBox)
        samplingLayout = QHBoxLayout()
        analysisLayout.addLayout(samplingLayout)
        samplingLabel = QLabel('Sampling', parent=analysisBox)
        samplingLayout.addWidget(samplingLabel)
        self._sAnalysisSamplingBox = QSpinBox(parent=analysisBox)
        self._sAnalysisSamplingBox.setRange(1, 10000)
        self._sAnalysisSamplingBox.setSingleStep(1)
        samplingLayout.addWidget(self._sAnalysisSamplingBox)
        self._sAnalysisSamplingBox.editingFinished.connect(self._setSampling)

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

        self._rBetaX = ResultCells(parent, 'BetaX', layout, 0)
        self._rGammaM = ResultCells(parent, 'GammaM', layout, 1)
        self._rRedChi2 = ResultCells(parent, 'RedChi2', layout, 2)
        self._rR2 = ResultCells(parent, 'R2', layout, 3)
        self._rQ = ResultCells(parent, 'Q', layout, 4)

        self._rBetaX.setBold(True)
        self._rGammaM.setBold(True)
        self._rRedChi2.setBold(False)
        self._rR2.setBold(False)
        self._rQ.setBold(False)

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
        self._rSeries = ResultCells(parent, 'Series Name', layout, 0)
        self._rNbSeq = ResultCells(parent, 'Nb Sequences', layout, 1)
        self._rAlphaBt = ResultCells(parent, 'AlphaBT', layout, 2)
        self._rDeltaDe = ResultCells(parent, 'DeltaDE', layout, 3)
        self._rBackground = BackgroundResultCells(
            parent, 'Background', layout, 4
        )
        self._rPercentileRange = ResultCells(
            parent, 'Percentile Range', layout, 5
        )
        self._rAnalysisDetails = ResultCells(
            parent, 'Save Analysis Details', layout, 6
        )
        self._rSamplingLabel = ResultCells(
            parent, 'Sampling for Analysis', layout, 7
        )
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

        # 3D plane
        planeBox = QGroupBox('3D Plane', parent=parent)
        layout.addWidget(planeBox)
        planeLayout = QHBoxLayout()
        planeBox.setLayout(planeLayout)
        self._r3dPlaneMatButton = QPushButton(
            '3D Plane (Matplot)', parent=planeBox)
        self._r3dPlaneMatButton.clicked.connect(
            lambda: self._openStageFigure(
                ['inspection', 'scatter_3d'], '3D Plane'
            )
        )
        planeLayout.addWidget(self._r3dPlaneMatButton)
        if PopUpManager().hasNapariMode():
            self._r3dPlaneNapariButton = QPushButton(
                '3D Plane (Napari)', parent=planeBox
            )
            self._r3dPlaneNapariButton.clicked.connect(self._open3dPlane)
            planeLayout.addWidget(self._r3dPlaneNapariButton)

        # Hist 2D
        hist2dBox = QGroupBox('2D Histograms', parent=parent)
        layout.addWidget(hist2dBox)
        hist2dLayout = QHBoxLayout()
        hist2dBox.setLayout(hist2dLayout)
        self._rH2dSvEButton = QPushButton('S vs E', parent=hist2dBox)
        self._rH2dSvEButton.clicked.connect(
            lambda: self._openStageFigure(
                ['hist2d_s_vs_e'], '2D Histogram S vs E'
            )
        )
        self._rH2dEvIButton = QPushButton('E vs Iaa', parent=hist2dBox)
        self._rH2dEvIButton.clicked.connect(
            lambda: self._openStageFigure(
                ['hist2d_e_vs_iaa'], '2D Histogram E vs IAA'
            )
        )
        self._rH2dSvIButton = QPushButton('S vs Iaa', parent=hist2dBox)
        self._rH2dSvIButton.clicked.connect(
            lambda: self._openStageFigure(
                ['hist2d_s_vs_iaa'], '2D Histogram S vs Iaa'
            )
        )
        hist2dLayout.addWidget(self._rH2dSvEButton)
        hist2dLayout.addWidget(self._rH2dEvIButton)
        hist2dLayout.addWidget(self._rH2dSvIButton)

        # Boxplots
        boxplotBox = QGroupBox('Boxplots', parent=parent)
        layout.addWidget(boxplotBox)
        boxplotLayout = QHBoxLayout()
        boxplotBox.setLayout(boxplotLayout)
        self._rBoxplotEButton = QPushButton('E', parent=boxplotBox)
        self._rBoxplotEButton.clicked.connect(
            lambda: self._openStageFigure(
                ['e_boxplot'], 'E Boxplot'
            )
        )
        self._rBoxplotSButton = QPushButton('S', parent=boxplotBox)
        self._rBoxplotSButton.clicked.connect(
            lambda: self._openStageFigure(
                ['s_boxplot'], 'S Boxplot'
            )
        )
        boxplotLayout.addWidget(self._rBoxplotEButton)
        boxplotLayout.addWidget(self._rBoxplotSButton)

        # ScatterPlots
        scatterBox = QGroupBox('Scatters', parent=parent)
        layout.addWidget(scatterBox)
        scatterLayout = QHBoxLayout()
        scatterBox.setLayout(scatterLayout)
        self._rScatterTvSeqButton = QPushButton(
            'Triplets per Seq', parent=scatterBox)
        self._rScatterTvSeqButton.clicked.connect(
            lambda: self._openStageFigure(
                ['inspection', 'triplets_per_seq'], 'Triplets per Seq'
            )
        )
        self._rScatterSvSeqButton = QPushButton(
            'S per Seq', parent=scatterBox)
        self._rScatterSvSeqButton.clicked.connect(
            lambda: self._openStageFigure(
                ['inspection', 's_per_seq'], 'S per Seq'
            )
        )
        self._rScatterSvEButton = QPushButton(
            'S vs E', parent=scatterBox)
        self._rScatterSvEButton.clicked.connect(
            lambda: self._openStageFigure(
                ['inspection', 's_vs_e'], 'S vs E'
            )
        )
        scatterLayout.addWidget(self._rScatterTvSeqButton)
        scatterLayout.addWidget(self._rScatterSvSeqButton)
        scatterLayout.addWidget(self._rScatterSvEButton)

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
            'calibration', 'xm', parent=parent
        )
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
        self._sPercentileLowBox.blockSignals(val)
        self._sPercentileHighBox.blockSignals(val)
        self._sAnalysisDetailsCheckBox.blockSignals(val)
        self._sAnalysisSamplingBox.blockSignals(val)

    def _updateSettings(self) -> None:
        """ Update the number of sequences for each series
        """
        params = self._iopm.params.get('xm', True)
        _, series, alphaBt, deltaDe, background, percentile, \
            analysis_details, sampling = params

        self._sPercentileLowValue = percentile[0]
        self._sPercentileHighValue = percentile[1]
        self._sAnalysisSamplingValue = sampling

        self._sSeries.setResult(f'Standards ({series.size})')
        self._sAlphaBt.setResult(alphaBt)
        self._sDeltaDe.setResult(deltaDe)
        self._sBackground.setResult(background)
        self._sPercentileLowBox.setValue(percentile[0])
        self._sPercentileHighBox.setValue(percentile[1])
        self._sAnalysisDetailsCheckBox.setChecked(analysis_details)
        self._sAnalysisSamplingBox.setValue(sampling)

    def _loadResults(self) -> bool:
        """ Load the results, update the results widget. and inform if results
        were found.

        Returns:
            bool: True if results were loaded, False otherwise
        """
        # Retrieve settings and results
        settings = self._iopm.results['xm'].get_stage_settings()
        if settings is None:
            return False
        series, nb_seq, alphaBt, deltaDe, background, percentile, \
            analysis_details, sampling = settings
        results = self._iopm.results['xm'].get_stage_results()
        if results is None:
            return False
        betaX, gammaM, redChi2, r2, q = results

        # Update settings
        self._rSeries.setResult(series)
        self._rNbSeq.setResult(nb_seq)
        self._rAlphaBt.setResult(alphaBt)
        self._rDeltaDe.setResult(deltaDe)
        self._rBackground.setResult(background)
        self._rPercentileRange.setResult(percentile)
        self._rAnalysisDetails.setResult(analysis_details)
        self._rSamplingLabel.setResult(sampling)

        # Update results
        self._rBetaX.setResult(betaX)
        self._rGammaM.setResult(gammaM)
        self._rRedChi2.setResult(redChi2)
        self._rR2.setResult(r2)
        self._rQ.setResult(q)

        # Update Stage plot buttons
        extras = self._iopm.results[self._stage].get_stage_extras(
            check_only=True
        )
        self._rH2dSvEButton.setEnabled(extras['hist2d_s_vs_e'])
        self._rH2dEvIButton.setEnabled(extras['hist2d_e_vs_iaa'])
        self._rH2dSvIButton.setEnabled(extras['hist2d_s_vs_iaa'])
        self._rBoxplotEButton.setEnabled(extras['e_boxplot'])
        self._rBoxplotSButton.setEnabled(extras['s_boxplot'])
        self._r3dPlaneMatButton.setEnabled(extras['inspection']['scatter_3d'])
        if PopUpManager().hasNapariMode():
            self._r3dPlaneNapariButton.setEnabled(extras['sampled_list'])
        self._rScatterTvSeqButton.setEnabled(
            extras['inspection']['triplets_per_seq'])
        self._rScatterSvSeqButton.setEnabled(extras['inspection']['s_per_seq'])
        self._rScatterSvEButton.setEnabled(extras['inspection']['s_vs_e'])

        return True

    def _setPercentileLow(self) -> None:
        """ Set the percentile value in the config

        Make sure it doesn't go above percentile high.
        """
        lowPercentile = self._sPercentileLowBox.value()
        highPercentile = self._sPercentileHighBox.value()
        if lowPercentile > 100:
            lowPercentile = 100
        elif lowPercentile < 0:
            lowPercentile = 0
        elif lowPercentile > highPercentile:
            lowPercentile = highPercentile
        self._sPercentileLowBox.setValue(lowPercentile)

        # Prevent useless savings
        if lowPercentile != self._sPercentileLowValue:
            self._sPercentileLowValue = lowPercentile
            self._iopm.config.set('XM', 'discard_low_percentile',
                                  lowPercentile)

    def _setPercentileHigh(self) -> None:
        """ Set the percentile value in the config

        Make sure it doesn't go above percentile high.
        """
        highPercentile = self._sPercentileHighBox.value()
        lowPercentile = self._sPercentileLowBox.value()
        if highPercentile > 100:
            highPercentile = 100
        elif highPercentile < 0:
            highPercentile = 0
        elif highPercentile < lowPercentile:
            highPercentile = lowPercentile
        self._sPercentileHighBox.setValue(highPercentile)

        # Prevent useless savings
        if highPercentile != self._sPercentileHighValue:
            self._sPercentileHighValue = highPercentile
            self._iopm.config.set('XM', 'discard_high_percentile',
                                  highPercentile)

    def _setAnalysisDetails(self, _: bool) -> None:
        """Set the analysis details value in the config

        Args:
            _ (bool): Not used, we get the checked directly from widget
        """
        checked = self._sAnalysisDetailsCheckBox.isChecked()
        self._iopm.config.set('XM', 'save_analysis_details', checked)

    def _setSampling(self) -> None:
        """ Set the analysis sampling value in the config
        """
        sampling = self._sAnalysisSamplingBox.value()
        if sampling != self._sAnalysisSamplingValue:
            self._sAnalysisSamplingValue = sampling
            self._iopm.config.set('XM', 'analysis_sampling', sampling)

    def _openStageFigure(self, key: list[str], title: str) -> None:
        """ Open a stage figure in a new window

        Args:
            key (str, list[str]): Key of the figure in the extra figures dict
            title (str): Title of the dialog to open
        """
        extras = self._iopm.results[self._stage].get_stage_extras(key, True)
        if len(key) == 1:
            valid = extras[key[0]]
        elif len(key) == 2:
            valid = extras[key[0]][key[1]]
        else:
            raise QtfException('Bad key length')

        if valid:
            extras = self._iopm.results[self._stage].get_stage_extras(key)
            title = f'{self._stage.upper()} - {title}'
            if len(key) == 1:
                PopUpManager().openFigure(extras[key[0]], title)
            elif len(key) == 2:
                PopUpManager().openFigure(extras[key[0]][key[1]], title)

    def _open3dPlane(self) -> None:
        """ Open a stage figure in a new window

        Args:
            key (str, list[str]): Key of the figure in the extra figures dict
            title (str): Title of the dialog to open
        """
        extras = self._iopm.results[self._stage].get_stage_extras(
            'sampled_list'
        )
        sampled_list = extras['sampled_list']

        if sampled_list is not None:
            dds = np.concatenate([s[0] for s in sampled_list], axis=0)
            das = np.concatenate([s[1] for s in sampled_list], axis=0)
            aas = np.concatenate([s[2] for s in sampled_list], axis=0)

            array = np.stack([dds, das, aas], axis=1)

            PopUpManager().openArray(array)
