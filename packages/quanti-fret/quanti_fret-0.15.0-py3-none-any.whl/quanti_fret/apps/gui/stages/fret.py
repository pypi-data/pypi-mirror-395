from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.popup import PopUpManager
from quanti_fret.apps.gui.stages.results_table import TripletResultsTable
from quanti_fret.apps.gui.stages.stage_calculation import StageCalculatorWidget
from quanti_fret.apps.gui.utils import BackgroundResultCells, ResultCells

from qtpy.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class StageFretWidget(StageCalculatorWidget):
    """ Handle the stage that computes the BT or DE stages.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Constructor
        """
        # Mandatory in order to prevent saving config even if value didn't
        # change
        self._filterSettingsValues = {
            'sigma_s': 0.0,
            'target_s': 0.0,
            'sigma_gauss': 0.0,
            'weights_threshold': 0.0,
        }
        self._sAnalysisSamplingValue = 0

        IOGuiManager().cali.stateChanged.connect(self._updateSettings)

        super().__init__('fret', IOGuiManager().fret, *args, showProgress=True,
                         **kwargs)

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
        self._sBetaX = ResultCells(
            lockedSettingsBox, 'BetaX', lockedSettingsLayout, 3)
        self._sBetaX.setLocked(True)
        self._sGammaM = ResultCells(
            lockedSettingsBox, 'GammaM', lockedSettingsLayout, 4)
        self._sGammaM.setLocked(True)
        self._sBackground = BackgroundResultCells(
            lockedSettingsBox, 'Background', lockedSettingsLayout, 5)
        self._sBackground.setLocked(True)

        # Gaussian filter settings
        gFilterBox = QGroupBox('Gaussian Filter Settings', parent=parent)
        settingsLayout.addWidget(gFilterBox)
        gFilterLayout = QGridLayout()
        gFilterBox.setLayout(gFilterLayout)
        # SigmaS
        sigmaSLayout, self._sSigmaSBox = self._buildGaussianFilterSettings(
            'Sigma S', 'sigma_s', parent=gFilterBox
        )
        gFilterLayout.addLayout(sigmaSLayout, 0, 0)
        # Target S
        targetSLayout, self._sTargetSBox = self._buildGaussianFilterSettings(
            'Target S', 'target_s', parent=gFilterBox
        )
        gFilterLayout.addLayout(targetSLayout, 1, 0)
        # Sigma Gauss
        sigmaGaussLayout, self._sSigmaGaussBox = \
            self._buildGaussianFilterSettings(
                'Sigma Gauss', 'sigma_gauss', parent=gFilterBox, step=1.)
        gFilterLayout.addLayout(sigmaGaussLayout, 2, 0)
        # Weights threshold
        weightsTLayout, self._sWeightsTBox = self._buildGaussianFilterSettings(
            'Weights Threshold', 'weights_threshold', parent=gFilterBox
        )
        gFilterLayout.addLayout(weightsTLayout, 3, 0)

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

    def _buildGaussianFilterSettings(
        self, title: str, key: str, parent: QWidget, step: float = 0.1
    ) -> tuple[QHBoxLayout, QDoubleSpinBox]:
        """ Build the layout and doublespin box for a single Gaussian Filter
        settings.

        Args:
            title (str): Title to display on the label widget
            key (str): key to save the value in the config
            step (float): Value to add when using the widget + and - arrows

        Returns:
            tuple[QHBoxLayout, QDoubleSpinBox]: the layout and the box created
        """
        layout = QHBoxLayout()
        label = QLabel(title, parent=parent)
        spinBox = QDoubleSpinBox(parent=parent)
        spinBox.setSingleStep(step)
        layout.addWidget(label)
        layout.addWidget(spinBox)
        spinBox.editingFinished.connect(
            lambda: self._setGammaFilterDetails(key, spinBox)
        )

        return layout, spinBox

    def _buildResultsSetting(self, parent: QWidget) -> QLayout | None:
        """ Create the layout that will hold the settings used to compute
        the results

        Args:
            parent(QWidget): Parent widget for all widget created here

        Returns:
            QLayout: Results layout created
        """
        # Result settings box
        layout = QGridLayout()

        self._rSeries = ResultCells(parent, 'Series Name', layout, 0)
        self._rNbSeq = ResultCells(parent, 'Nb Sequences', layout, 1)
        self._rAlphaBt = ResultCells(parent, 'AlphaBT', layout, 2)
        self._rDeltaDe = ResultCells(parent, 'DeltaDE', layout, 3)
        self._rBetaX = ResultCells(parent, 'BetaX', layout, 4)
        self._rGammaM = ResultCells(parent, 'GammaM', layout, 5)
        self._rBackground = BackgroundResultCells(
            parent, 'Background', layout, 6)
        self._rSigmaS = ResultCells(parent, 'SigmaS', layout, 7)
        self._rTargetS = ResultCells(parent, 'TargetS', layout, 8)
        self._rSigmaGauss = ResultCells(parent, 'SigmaGauss', layout, 9)
        self._rWeightsT = ResultCells(parent, 'Weights Threshold', layout, 10)
        self._rAnalysisDetails = ResultCells(
            parent, 'Analysis details', layout, 11)
        self._rSampling = ResultCells(parent, 'Sampling', layout, 12)

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

        # Hist 2D
        self._rHist2dButton = QPushButton('2D Histogram', parent=parent)
        self._rHist2dButton.clicked.connect(
            lambda: self._openStageFigure('hist_2d', '2D Histogram')
        )
        layout.addWidget(self._rHist2dButton)

        # Box plots
        boxplotLayout = QHBoxLayout()
        boxplotLayout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(boxplotLayout)
        self._rEBoxplotButton = QPushButton('E Boxplot', parent=parent)
        self._rEBoxplotButton.clicked.connect(
            lambda: self._openStageFigure('e_boxplot', 'E Boxplot')
        )
        self._rSBoxplotButton = QPushButton('S Boxplot', parent=parent)
        self._rSBoxplotButton.clicked.connect(
            lambda: self._openStageFigure('s_boxplot', 'S Boxplot')
        )
        boxplotLayout.addWidget(self._rEBoxplotButton)
        boxplotLayout.addWidget(self._rSBoxplotButton)

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
            'fret', 'fret', hasResults=True, hasPlot=True, parent=parent,
            detailIndex=11
        )
        rTripletTable.resultsClicked.connect(self._openTripletResult)
        rTripletTable.plotClicked.connect(self._openTripletPlot)
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
        self._sSigmaSBox.blockSignals(val)
        self._sTargetSBox.blockSignals(val)
        self._sSigmaGaussBox.blockSignals(val)
        self._sWeightsTBox.blockSignals(val)
        self._sAnalysisDetailsCheckBox.blockSignals(val)
        self._sAnalysisSamplingBox.blockSignals(val)

    def _updateSettings(self) -> None:
        """ Update the number of sequences for each series
        """
        params = self._iopm.params.get('fret', True)
        _, series, alphaBt, deltaDe, betaX, GammaM, background, SigmaS,  \
            targetS, sigmaGauss, weightsThreshold,  analysisDetails,  \
            analysisSampling = params

        self._filterSettingsValues = {
            'sigma_s': SigmaS,
            'target_s': targetS,
            'sigma_gauss': sigmaGauss,
            'weights_threshold': weightsThreshold,
        }
        self._sAnalysisSamplingValue = analysisSampling

        self._sSeries.setResult(series.size)
        self._sAlphaBt.setResult(self._str_val(alphaBt))
        self._sDeltaDe.setResult(self._str_val(deltaDe))
        self._sBetaX.setResult(self._str_val(betaX))
        self._sGammaM.setResult(self._str_val(GammaM))
        self._sBackground.setResult(background)
        self._sSigmaSBox.setValue(SigmaS)
        self._sTargetSBox.setValue(targetS)
        self._sSigmaGaussBox.setValue(sigmaGauss)
        self._sWeightsTBox.setValue(weightsThreshold)
        self._sAnalysisDetailsCheckBox.setChecked(analysisDetails)
        self._sAnalysisSamplingBox.setValue(analysisSampling)

    def _loadResults(self) -> bool:
        """ Load the results, update the results widget. and inform if results
        were found.

        Returns:
            bool: True if results were loaded, False otherwise
        """
        # Retrieve results
        settings = self._iopm.results['fret'].get_stage_settings()
        if settings is None:
            return False
        series, nb_seq, alphaBt, deltaDe, betaX, gammaM, background, sigmaS,  \
            targetS, sigmaGauss, weightsThreshold,  analysisDetails,  \
            analysisSampling = settings

        # Update settings
        self._rSeries.setResult(series)
        self._rNbSeq.setResult(nb_seq)
        self._rAlphaBt.setResult(alphaBt)
        self._rDeltaDe.setResult(deltaDe)
        self._rBetaX.setResult(betaX)
        self._rGammaM.setResult(gammaM)
        self._rBackground.setResult(background)
        self._rSigmaS.setResult(sigmaS)
        self._rTargetS.setResult(targetS)
        self._rSigmaGauss.setResult(sigmaGauss)
        self._rWeightsT.setResult(weightsThreshold)
        self._rAnalysisDetails.setResult(analysisDetails)
        self._rSampling.setResult(analysisSampling)

        # Update Stage plot buttons
        figures = self._iopm.results[self._stage].get_stage_extras(
            check_only=True
        )
        self._rHist2dButton.setEnabled(figures['hist_2d'])
        self._rEBoxplotButton.setEnabled(figures['e_boxplot'])
        self._rSBoxplotButton.setEnabled(figures['s_boxplot'])

        return True

    def _setGammaFilterDetails(self, key: str, widget: QDoubleSpinBox) -> None:
        """Set the gamma filter value in the config

        Args:
            key (str): Key in the config to set
            widget (QDoubleSpinBox): widget to get the value from
        """
        val = widget.value()
        if self._filterSettingsValues[key] != val:
            self._filterSettingsValues[key] = val
            self._iopm.config.set('Fret', key, val)

    def _setAnalysisDetails(self, _: bool) -> None:
        """Set the analysis details value in the config

        Args:
            _ (bool): Not used, we get the checked directly from widget
        """
        checked = self._sAnalysisDetailsCheckBox.isChecked()
        self._iopm.config.set('Fret', 'save_analysis_details', checked)

    def _setSampling(self) -> None:
        """ Set the analysis sampling value in the config
        """
        sampling = self._sAnalysisSamplingBox.value()
        if sampling != self._sAnalysisSamplingValue:
            self._sAnalysisSamplingValue = sampling
            self._iopm.config.set('Fret', 'analysis_sampling', sampling)

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

    def _openTripletResult(self, id: int) -> None:
        """ Open a triplet id results in a new window

        Args:
            id (int): Id of the triplet to open
        """
        PopUpManager().openFretResult(id, self._iopm.results)

    def _openTripletPlot(self, id: int) -> None:
        """ Open the extra plots of a Triplet in a new window.
        """
        preTitle = f'{self._stage.upper()} - Result #{id}'
        res = self._iopm.results[self._stage].get_triplet_extras(id)
        if res['hist2d_s_vs_e'] is not None:
            title = f'{preTitle} - 2D Histogram S vs E'
            PopUpManager().openFigure(res['hist2d_s_vs_e'], title)
        if res['hist2d_e_vs_iaa'] is not None:
            title = f'{preTitle} - 2D Histogram E vs Iaa'
            PopUpManager().openFigure(res['hist2d_e_vs_iaa'], title)
        if res['hist2d_s_vs_iaa'] is not None:
            title = f'{preTitle} - 2D Histogram S vs Iaa'
            PopUpManager().openFigure(res['hist2d_s_vs_iaa'], title)
