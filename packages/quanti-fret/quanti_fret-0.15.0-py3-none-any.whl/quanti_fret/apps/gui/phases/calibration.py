from quanti_fret.apps.gui.config import CalibrationConfigManagementWidget
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.phases.phase import PhaseWidget
from quanti_fret.apps.gui.series import SeriesWidget
from quanti_fret.apps.gui.stages import (
    StageBackgroundWidget, StageGammaWidget, StageOutputWidget, StageXmWidget
)

from qtpy.QtWidgets import QTabWidget


class CalibrationWidget(PhaseWidget):
    """ Widget managing the Calibration Phase
    """
    def __init__(self, *args, **kwargs) -> None:
        """Constructor

        Args:
            iopm (IOPhaseGuiManager) IOPM associated with the phase
        """
        super().__init__(IOGuiManager().cali, *args, **kwargs)

    def _buildStagesTab(self) -> None:
        """Create the tab widget that will host the different stages of the
        QuanTI-FRET phase.
        """
        # Create Tab Widget
        self._stages = QTabWidget(parent=self)
        self.layout().addWidget(self._stages)  # type: ignore

        # Add Config management
        self._configWidget = CalibrationConfigManagementWidget(
            parent=self._stages
        )
        self._stages.addTab(self._configWidget, 'Config')

        # Add Series stage
        seriesStageWidget = SeriesWidget('calibration', parent=self._stages)
        self._stages.addTab(seriesStageWidget, 'Series')

        # Add Output selection
        outputStageWidget = StageOutputWidget(
            'calibration', ('Output', 'output_dir'), 'folder',
            'Select Calibration Output folder', parent=self._stages
        )
        self._stages.addTab(outputStageWidget, 'Output')

        # Add Background calculation stage
        backgroundStageWidget = StageBackgroundWidget(parent=self._stages)
        self._stages.addTab(backgroundStageWidget, 'Background')

        # Add BT calculation stage
        btStageWidget = StageGammaWidget('BT', parent=self._stages)
        self._stages.addTab(btStageWidget, 'BT')

        # Add DE calculation stage
        deStageWidget = StageGammaWidget('DE', parent=self._stages)
        self._stages.addTab(deStageWidget, 'DE')

        # Add XM calculation stage
        xmWidget = StageXmWidget(parent=self._stages)
        self._stages.addTab(xmWidget, 'XM')
