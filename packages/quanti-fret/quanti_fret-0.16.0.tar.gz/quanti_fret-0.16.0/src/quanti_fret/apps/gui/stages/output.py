from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.path import PathWidget

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QVBoxLayout,
    QWidget
)


class StageOutputWidget(QWidget):
    """ Widget handling the output folder settings.
    """

    def __init__(
        self, phase: str, configKey: tuple[str, str], type: str,
        dialogTitle: str, *args, boxTitle: str = '',
        dialogFileFilter: str = '', **kwargs
    ) -> None:
        """ Constructor

        Args:
            phase (str): Phase of the widget
            configKey (tuple[str, str]): Config's section and key associated
                with the option
            type (str): Type of path to look for. Either 'file' or 'folder'
            dialogTitle (str): Title to put on the dialog selection window
            boxTitle (str, optional): Title to put on the widget box. If not
                set, a default title will be created. Default is ''.
            dialogFileFilter (str, optional): Filter to select pecific file
                type. Default is ''.
        """
        super().__init__(*args, **kwargs)

        # Create main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Folder selection
        pathWidget = PathWidget(
            phase, configKey, type, dialogTitle, boxTitle=boxTitle,
            dialogFileFilter=dialogFileFilter,
            parent=self
        )
        layout.addWidget(pathWidget)

        # Clean before run
        cleanBox = QGroupBox('Clean Policy', parent=self)
        cleanLayout = QVBoxLayout()
        cleanBox.setLayout(cleanLayout)
        self._cleanResultsCheckBox = QCheckBox(
            'Clean Previous Results Before Run', parent=cleanBox)
        self._cleanResultsCheckBox.stateChanged.connect(
            self._setCleanBeforeRun)
        cleanLayout.addWidget(self._cleanResultsCheckBox)
        layout.addWidget(cleanBox)

        # Connect to IOPM
        self._iopm = IOGuiManager().get_iopm(phase)
        self._iopm.stateChanged.connect(self._updateCheckBox)
        self._updateCheckBox()

    def _setCleanBeforeRun(self, _: bool) -> None:
        """Set the clean before run value in the config

        Args:
            _ (bool): Not used, we get the checked directly from widget
        """
        checked = self._cleanResultsCheckBox.isChecked()
        self._iopm.config.set('Output', 'clean_before_run', checked)

    def _updateCheckBox(self) -> None:
        """ Update the checkbox with the config
        """
        self._cleanResultsCheckBox.blockSignals(True)
        checked = self._iopm.config.get('Output', 'clean_before_run')
        self._cleanResultsCheckBox.setChecked(checked)
        self._cleanResultsCheckBox.blockSignals(False)
