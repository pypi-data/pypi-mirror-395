from quanti_fret import __version__ as qtf_version
from quanti_fret.apps.gui.phases import CalibrationWidget, FretWidget
from quanti_fret.apps.gui.popup import PopUpManager  # noqa: F401

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class QtfMainWidget(QWidget):
    """ Top level widget for QuanTI-FRET Gui application.

    Can be called inside a window, or passed to Napari.
    """
    def __init__(self, *args, **kwargs) -> None:
        """Constructor
        """
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self._buildStagesTab()
        self._buildVersionFooter()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 5, 5)

    def _buildStagesTab(self) -> None:
        """Create the tab widget that will host the different stages of the
        QuanTI-FRET process.
        """
        # Create Tab Widget
        operations = QTabWidget(self)
        operations.setDocumentMode(True)
        tabBar = operations.tabBar()
        assert tabBar is not None
        tabBar.setExpanding(True)
        self.layout().addWidget(operations)  # type: ignore

        # Add Calibration Operation tab
        calibrationWidget = CalibrationWidget(parent=tabBar)
        operations.addTab(calibrationWidget, 'Calibration')

        # Add Fret Operation tab
        fretWidget = FretWidget(parent=tabBar)
        operations.addTab(fretWidget, 'Fret')

    def _buildVersionFooter(self) -> None:
        layout = self.layout()
        assert layout is not None

        version = QLabel(f'Version: {qtf_version}')
        version.setEnabled(False)
        version.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(version)


__ALL__ = [
    'PopUpManager',
    'QtfMainWidget',
]
