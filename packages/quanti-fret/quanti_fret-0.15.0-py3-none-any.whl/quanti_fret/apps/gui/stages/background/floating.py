from quanti_fret.apps.gui.io_gui_manager import IOGuiManager

from qtpy.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QVBoxLayout,
)


class FloatingBackgroundBox(QGroupBox):
    """ Group Box for Background floating selection

    Disaplay a checkbox to activate or deactivate the floating background.
    """

    def __init__(self, phase: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            phase (str): Phase associated with the widget
        """
        super().__init__('Floating Background', *args, **kwargs)

        self._phase = phase
        self._iopm = IOGuiManager().get_iopm(phase)

        self._buildGui()

        self._iopm.stateChanged.connect(self._updateSettings)
        self._updateSettings()

    def _buildGui(self) -> None:
        """ Build the GUI interface
        """
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Checkbox
        self._checkBox = QCheckBox('Activate', parent=self)
        self._checkBox.stateChanged.connect(self._select_floating_background)
        layout.addWidget(self._checkBox)

    def _updateSettings(self) -> None:
        """ Update the checkbox and background results
        """
        # Floating state
        self._checkBox.blockSignals(True)

        floating = self._iopm.config.get('Background', 'floating')
        self._checkBox.setChecked(floating)

        self._checkBox.blockSignals(False)

    def _select_floating_background(self, _: int) -> None:
        """ Select the floating background to the given value
        """
        checked = self._checkBox.isChecked()
        self._iopm.config.set('Background', 'floating', checked)
