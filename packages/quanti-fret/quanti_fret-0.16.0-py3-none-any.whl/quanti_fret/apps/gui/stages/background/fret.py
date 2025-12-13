from quanti_fret.apps.gui.stages.background.mode import BackgroundModeBox
from quanti_fret.apps.gui.stages.background.floating import (
    FloatingBackgroundBox
)
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.utils import BackgroundResultCells

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QVBoxLayout,
    QWidget
)


class BackgroundFretWidget(QWidget):
    """ Handle the background settings for the Fret
    """

    def __init__(self, *args, **kwargs) -> None:
        """Constructor
        """
        super().__init__(*args, **kwargs)
        self._phase = 'fret'
        self._iopm = IOGuiManager().fret
        self._buildGui()
        self._iopm.stateChanged.connect(self._updateSettings)
        self._updateSettings()

    def _buildGui(self) -> None:
        """ Create the GUI
        """
        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # Calibration Value Box
        caliBox = QGroupBox('From Calibration', parent=self)
        layout.addWidget(caliBox)
        caliLayout = QGridLayout()
        caliBox.setLayout(caliLayout)
        self._caliBckgLabel = BackgroundResultCells(
            caliBox, 'Background', caliLayout, 0
        )
        self._caliBckgLabel.setLocked(True)

        # Floating Box
        floatingBox = FloatingBackgroundBox(self._phase, parent=self)
        layout.addWidget(floatingBox)

        # Mode Box
        self._modeBox = BackgroundModeBox(self._phase, parent=self)
        layout.addWidget(self._modeBox)

    def _updateSettings(self) -> None:
        """ Enable or Disable the mode box
        """
        # Disabled what is needed
        floating = self._iopm.config.get('Background', 'floating')
        self._modeBox.setEnabled(floating)
        self._caliBckgLabel.setEnabled(not floating)

        # Update Calibration Background
        (engine,) = self._iopm.params.get('cali_background',
                                          allow_none_values=True)
        self._caliBckgLabel.setResult(engine)
