from quanti_fret.apps.gui.stages.background.mode_radio_button import (
    BckgModeRadioButton
)
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.utils import PercentileSpinBox

from quanti_fret.algo import BackgroundMode

from qtpy.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class BackgroundModeBox(QGroupBox):
    """ Group Box for background mode selection.

    I consists of a set of radio button for each mode, followed by spinboxes
    to set the percentile or fixed background values.

    Percentile values can be changed only if in percentile mode
    Fixed background value can be changed only on Fix mode
    """

    def __init__(self, phase: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            phase (str): Phase associated with the widget
        """
        super().__init__('Mode', *args, **kwargs)

        self._phase = phase
        self._iopm = IOGuiManager().get_iopm(phase)
        self._modeButtons: dict[BackgroundMode, BckgModeRadioButton] = {}

        self._buildGui()

        self._iopm.stateChanged.connect(self._updateSettings)
        self._updateSettings()

    def _buildGui(self) -> None:
        """ Build the GUI interface
        """
        # Layout
        modeLayout = QGridLayout()
        self.setLayout(modeLayout)

        # DISABLED Buttons
        disabledButton = BckgModeRadioButton(
            self._phase, BackgroundMode.DISABLED, parent=self
        )
        modeLayout.addWidget(disabledButton, 0, 0)
        self._modeButtons[BackgroundMode.DISABLED] = disabledButton

        # Masked Buttons
        maskButton = BckgModeRadioButton(
            self._phase, BackgroundMode.MASK, parent=self
        )
        modeLayout.addWidget(maskButton, 1, 0)
        self._modeButtons[BackgroundMode.MASK] = maskButton

        # Percentile Buttons
        percentileButton = BckgModeRadioButton(
            self._phase, BackgroundMode.PERCENTILE, parent=self
        )
        modeLayout.addWidget(percentileButton, 2, 0)
        self._modeButtons[BackgroundMode.PERCENTILE] = percentileButton
        self._percentileSpinBox = PercentileSpinBox(parent=self)
        self._percentileSpinBox.valueChanged.connect(self._set_percentile)
        modeLayout.addWidget(self._percentileSpinBox, 2, 1)

        # Fixed Button
        maskButton = BckgModeRadioButton(
            self._phase, BackgroundMode.FIXED, parent=self
        )
        modeLayout.addWidget(maskButton, 3, 0)
        self._modeButtons[BackgroundMode.FIXED] = maskButton
        self._fixBackgroundLayout = QHBoxLayout()
        modeLayout.addLayout(self._fixBackgroundLayout, 4, 0, 1, 2)
        self._fixedDDSpinbox = self._addFixBackgroundChannel('DD', 0)
        self._fixedDASpinbox = self._addFixBackgroundChannel('DA', 1)
        self._fixedAASpinbox = self._addFixBackgroundChannel('AA', 2)

    def _updateSettings(self) -> None:
        """ Update the number of sequences for each series
        """
        self._blockAllSignals(True)

        # Radiobuttons will update themselves
        mode = self._iopm.config.get('Background', 'mode')

        # Percentile
        percentile = self._iopm.config.get('Background', 'percentile')
        self._percentileSpinBox.setValue(percentile)
        if mode == BackgroundMode.PERCENTILE:
            self._percentileSpinBox.setEnabled(True)
        else:
            self._percentileSpinBox.setEnabled(False)

        # Fixed Background
        fixed_bckg = self._iopm.config.get('Background', 'fixed_background')
        self._fixedDDSpinbox.setValue(fixed_bckg[0])
        self._fixedDASpinbox.setValue(fixed_bckg[1])
        self._fixedAASpinbox.setValue(fixed_bckg[2])
        if mode == BackgroundMode.FIXED:
            self._fixedDDSpinbox.setEnabled(True)
            self._fixedDASpinbox.setEnabled(True)
            self._fixedAASpinbox.setEnabled(True)
        else:
            self._fixedDDSpinbox.setEnabled(False)
            self._fixedDASpinbox.setEnabled(False)
            self._fixedAASpinbox.setEnabled(False)

        self._blockAllSignals(False)

    def _blockAllSignals(self, val: bool) -> None:
        """ Call the `blockSignal` method of all widget whose signal is
        connected to a slot.

        The purpose of this method is to prevent slots to call config save
        while being updated by it.

        Args:
            val (bool): The value to pass to the `blockSignal` method
        """
        self._percentileSpinBox.blockSignals(val)
        self._fixedDDSpinbox.blockSignals(val)
        self._fixedDASpinbox.blockSignals(val)
        self._fixedAASpinbox.blockSignals(val)

    def _addFixBackgroundChannel(
        self, name: str, index: int
    ) -> QDoubleSpinBox:
        """ Add a FixBackground channel label and spinbox

        Args:
            name (str): Name of the channel
            index (int): index of the channel

        Returns:
            QDoubleSpinBox: SpinBox created
        """
        layout = QVBoxLayout()
        self._fixBackgroundLayout.addLayout(layout)
        label = QLabel(name, parent=self)
        layout.addWidget(label)
        spinBox = QDoubleSpinBox(parent=self)
        spinBox.setMinimum(0.0)
        spinBox.setSingleStep(0.1)
        spinBox.valueChanged.connect(
            lambda val, index=index: self._set_background(index, val)
        )
        layout.addWidget(spinBox)
        return spinBox

    def _set_percentile(self, val: float) -> None:
        """ Set the percentile value in the config

        Args:
            val (float): Value to set
        """
        self._iopm.config.set('Background', 'percentile', val)

    def _set_background(self, index: int, val: float) -> None:
        """ Set the fixed background value in the config

        Args:
            index (int): Index of the value to set
            val (float): Value to set
        """
        bckg = list(self._iopm.config.get('Background', 'fixed_background'))
        bckg[index] = val
        self._iopm.config.set('Background', 'fixed_background', bckg)
