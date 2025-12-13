from quanti_fret.core import QtfException
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.utils import PathLabel

from pathlib import Path
import traceback

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class PathWidget(QGroupBox):
    """ Handle the selection of a file or folder path.
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
                set, a default title will be created
            dialogFileFilter (str): Filter to select pecific file type
        """
        super().__init__(*args, **kwargs)

        if type not in ['file', 'folder']:
            err = f'Unknow type {type}. Must be in ["file", "folder"]'
            raise QtfException(err)

        self._iopm = IOGuiManager().get_iopm(phase)
        self._configKey = configKey
        self._type = type
        if boxTitle:
            self.setTitle(boxTitle)
        else:
            self.setTitle(f'Select {self._type.capitalize()}')
        self._dialogTitle = dialogTitle
        self._dialogFileFilter = dialogFileFilter

        # GUI
        self._mainLayout = QVBoxLayout()
        self.setLayout(self._mainLayout)
        self._mainLayout.setSpacing(20)
        self._mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._buildPathSelection()

        # Populate with previous value
        self._updateDisplay()
        self._iopm.stateChanged.connect(self._updateDisplay)

    def _buildPathSelection(self) -> None:
        """ Build the folder selection GUI
        """
        # Path Label
        self._fSelectLabel = PathLabel("Path:", parent=self)
        self._mainLayout.addWidget(self._fSelectLabel)

        # Folder select Button
        self._buttonLayout = QVBoxLayout()
        self._buttonLayout.setSpacing(5)
        self._mainLayout.addLayout(self._buttonLayout)
        self._fSelectButton = QPushButton(
            f'Select a {self._type.capitalize()}',
            parent=self)
        self._buttonLayout.addWidget(self._fSelectButton)
        self._fSelectButton.clicked.connect(self._openPath)

        # Detach select Label from top
        margin = self._mainLayout.contentsMargins()
        margin.setTop(margin.top() + 10)
        self._mainLayout.setContentsMargins(margin)

    def _openPath(self) -> None:
        """ Let the user choose a directory with a directory selection window,
        and update the output folder.
        """
        current_path = self._iopm.config.get(*self._configKey)
        if current_path is not None:
            parent = str(current_path.parent)
        else:
            parent = ""

        # Select user's path
        if self._type == 'file':
            path_str, _ = QFileDialog.getOpenFileName(
                self, self._dialogTitle, parent, self._dialogFileFilter
            )
        else:
            path_str = QFileDialog.getExistingDirectory(
                self, self._dialogTitle, parent
            )

        # Manage results
        if path_str:
            self._updatePath(Path(path_str))

    def _updatePath(self, path: Path | None) -> None:
        """ Update the path with the one chosen

        Args:
            path (Path | None): Path to set
        """
        current_path = self._iopm.config.get(*self._configKey)
        if path != current_path:
            try:
                self._iopm.config.set(*self._configKey, path)
            except Exception:
                msgBox = QMessageBox(parent=self)
                msgBox.setText('Error while loading the file...')
                msgBox.setInformativeText(traceback.format_exc())
                msgBox.setStandardButtons(
                    QMessageBox.StandardButton.Close
                )
                msgBox.setIcon(QMessageBox.Icon.Critical)
                self._iopm.config.set(*self._configKey, current_path)
                msgBox.exec()

    def _updateDisplay(self) -> None:
        """ Update the current output folder value
        """
        current_path = self._iopm.config.get(*self._configKey)
        if current_path is None:
            buttonTitle = f'Select a {self._type.capitalize()}'
        else:
            buttonTitle = f'Select a New {self._type.capitalize()}'
        self._fSelectLabel.setPath(current_path)
        self._fSelectButton.setText(buttonTitle)


class FretCaliConfigFileWidget(PathWidget):
    """ Widget handling the Calibration config file selection for the Fret
    phase.
    """
    def __init__(self, *args, **kwargs) -> None:
        """ Constructor
        """
        super().__init__(
            'fret', ('Calibration', 'config_file'), 'file',
            'Select Calibration Results folder', *args,
            dialogFileFilter='Config (*.ini)',
            boxTitle='Select Calibration Config File', **kwargs)

        self._iopm_cali = IOGuiManager().cali

        # Add Button to set to the current calibrations
        self._toCurrentButton = QPushButton(
            'Use the Current Calibration Config',
            parent=self)
        self._buttonLayout.addWidget(self._toCurrentButton)
        self._toCurrentButton.clicked.connect(self._setToCurrentCaliConfig)

        self._updateButton()
        self._iopm.stateChanged.connect(self._updateButton)
        self._iopm_cali.stateChanged.connect(self._updateButton)
        self._iopm_cali.noConfig.connect(self._remove_config_if_non_existing)
        self._iopm_cali.errorConfig.connect(
            self._remove_config_if_non_existing)

    def _setToCurrentCaliConfig(self):
        new_path = self._iopm_cali.get_active_config_path()
        assert new_path is not None
        self._updatePath(new_path)
        self._updateButton()

    def _updateButton(self) -> None:
        """ Update the current output folder value
        """
        active_cali_path = self._iopm_cali.get_active_config_path()
        fret_cali_path = self._iopm.config.get(*self._configKey)

        if active_cali_path is None:
            enable = False
            text = 'No Current Calibration Config'
            link = None
        else:
            if active_cali_path == fret_cali_path:
                enable = False
                text = 'Already Using the Current Calibration Config'
                link = self._iopm
            else:
                enable = True
                text = 'Use the Current Calibration Config'
                link = None
        self._toCurrentButton.setEnabled(enable)
        self._toCurrentButton.setText(text)
        self._iopm_cali.link_iopm(link)
        self._remove_config_if_non_existing()

    def _remove_config_if_non_existing(self) -> None:
        """ Remove the calibration config file if the file doesn't exists
        anymore
        """
        fret_cali_path: Path | None = self._iopm.config.get(*self._configKey)
        if fret_cali_path is not None:
            if not fret_cali_path.exists():
                self._updatePath(None)
                self._updateButton()
