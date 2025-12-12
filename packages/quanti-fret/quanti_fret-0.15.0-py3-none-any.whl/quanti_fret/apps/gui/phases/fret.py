from quanti_fret.apps.gui.config import FretConfigManagementWidget
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.phases.phase import PhaseWidget
from quanti_fret.apps.gui.series import SeriesWidget
from quanti_fret.apps.gui.stages import (
    BackgroundFretWidget, StageFretCaliConfigFileWidget, StageFretWidget,
    StageOutputWidget
)

from qtpy.QtWidgets import (
    QTabWidget,
)


class FretWidget(PhaseWidget):
    """ Widget managing the Fret Phase
    """
    def __init__(self, *args, **kwargs) -> None:
        """Constructor
        """
        super().__init__(IOGuiManager().fret, *args, **kwargs)

    def _buildStagesTab(self) -> None:
        """Create the tab widget that will host the different stages of the
        QuanTI-FRET process.
        """
        # Create Tab Widget
        self._stages = QTabWidget(parent=self)
        self.layout().addWidget(self._stages)  # type: ignore

        # Add Config management
        self._configWidget = FretConfigManagementWidget(parent=self._stages)
        self._stages.addTab(self._configWidget, 'Config')

        # Add Calibration selection
        calibrationStageWidget = StageFretCaliConfigFileWidget(
            parent=self._stages
        )
        self._stages.addTab(calibrationStageWidget, 'Calibration')

        # Add Series stage
        seriesStageWidget = SeriesWidget('fret', parent=self._stages)
        self._stages.addTab(seriesStageWidget, 'Series')

        # Add Output selection
        outputStageWidget = StageOutputWidget(
            'fret', ('Output', 'output_dir'), 'folder',
            'Select Fret Output folder', parent=self._stages
        )
        self._stages.addTab(outputStageWidget, 'Output')

        # Add Background selection
        backgroundWidget = BackgroundFretWidget(parent=self._stages)
        self._stages.addTab(backgroundWidget, 'Background')

        # Add Fret Stage
        fretStageWidget = StageFretWidget(parent=self._stages)
        self._stages.addTab(fretStageWidget, 'Fret')
