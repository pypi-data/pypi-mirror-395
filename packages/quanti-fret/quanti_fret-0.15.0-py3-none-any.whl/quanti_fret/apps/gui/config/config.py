from quanti_fret.apps.gui.io_gui_manager import IOGuiManager, IOPhaseGuiManager

from quanti_fret.core import QtfException

from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ConfigManagementWidget(QWidget):
    """ Handle the selection and creation of config files of a specific phase.

    The widget works as follow:
        * It opens the current active config file.
        * It provide a combobox that allow selection of all the config files in
            the same folder than the active one
        * It provides 4 buttons to manage config:
            * Browse: Select a custom config file
            * Duplicate: Duplicate the current config file and create a new one
            * New: Create a config file with default values
            * Delete: Delete the current config file, if other config files
                are presents in the active config folder, will select the first
                one in alphabetical order

    It also have a place holder for phase summary information if needed.
    """
    def __init__(self, phase: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            phase (str): Phase linked with the config.
        """
        super().__init__(*args, **kwargs)
        self._iopm = IOGuiManager().get_iopm(phase)

        # Gui SetUp
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)  # type: ignore
        self._buildConfigManagement()
        self._buildSeparator()
        self._buildPhaseSummary()

        # Populate the widgets
        self._populateConfigSelectionBox()
        self._updateResults()
        self._iopm.stateChanged.connect(self._updateResults)

    def newConfigSelected(self) -> None:
        """ Inform the manager that a new config was selected
        """
        self._populateConfigSelectionBox()

    def _buildConfigManagement(self) -> None:
        """ Build the widgets for config management
        """
        # Current Config
        configBox = QGroupBox('Current Config', parent=self)
        boxLayout = QVBoxLayout()
        configBox.setLayout(boxLayout)
        self._configSelectionBox = QComboBox(parent=configBox)
        boxLayout.addWidget(self._configSelectionBox)
        self._configSelectionBox.currentIndexChanged.connect(
            self._changeConfig
        )

        # Config settings button
        crudLayout = QHBoxLayout()
        self._browseButton = QPushButton('Browse', parent=configBox)
        self._duplicateButton = QPushButton('Duplicate', parent=configBox)
        self._newButton = QPushButton('New', parent=configBox)
        self._deleteButton = QPushButton('Delete', parent=configBox)
        crudLayout.addWidget(self._browseButton)
        crudLayout.addWidget(self._duplicateButton)
        crudLayout.addWidget(self._newButton)
        crudLayout.addWidget(self._deleteButton)
        self._browseButton.clicked.connect(self._browseConfig)
        self._newButton.clicked.connect(self._newConfig)
        self._duplicateButton.clicked.connect(self._duplicateConfig)
        self._deleteButton.clicked.connect(self._deleteConfig)
        boxLayout.addLayout(crudLayout)

        self.layout().addWidget(configBox)  # type: ignore

    def _buildSeparator(self) -> None:
        """ Build the separator line between config management and results
        """
        pass

    def _buildPhaseSummary(self) -> None:
        """ Build the widgets to show the Calibration results
        """
        pass

    def _changeConfig(self, index: int) -> None:
        """ Change the config to the one of the ComboBox selected index.

        Args:
            index (int): Index of the new config to select in the combobox
        """
        path_str = self._configSelectionBox.itemData(index)
        self._iopm.change_config(
            Path(path_str),
            IOPhaseGuiManager.ConfigChangeMode.CHANGE)
        self._populateConfigSelectionBox()

    def _browseConfig(self) -> None:
        """ Browse the user's file to select a config file

        Open a file save dialog to select the file to use for the config.

        The combobox will be filled with all the config files from the same
        folder as the config selected.
        """
        currentConfigPath = self._iopm.get_active_config_path()
        if currentConfigPath is None:
            currentConfigDir = None
        else:
            currentConfigDir = str(currentConfigPath.parent)

        path_str, _ = QFileDialog.getOpenFileName(
            self, 'Open Config File', currentConfigDir, 'Config (*.ini)'
        )
        if path_str:
            self._iopm.change_config(
                Path(path_str),
                IOPhaseGuiManager.ConfigChangeMode.CHANGE)
            self._populateConfigSelectionBox()

    def _newConfig(self) -> None:
        """ Create a new Config with default values.

        Open a file save dialog to select the file where to save the config

        The combobox will be filled with all the config files from the same
        folder as the config selected
        """
        currentConfigPath = self._iopm.get_active_config_path()
        if currentConfigPath is None:
            currentConfigDir = None
        else:
            currentConfigDir = str(currentConfigPath.parent)

        path_str, _ = QFileDialog.getSaveFileName(
            self, 'New Config File', currentConfigDir, 'Config (*.ini)'
        )
        if path_str:
            self._iopm.change_config(
                Path(path_str),
                IOPhaseGuiManager.ConfigChangeMode.NEW)
            self._populateConfigSelectionBox()

    def _duplicateConfig(self) -> None:
        """ Duplicate the current config

        Open a file save dialog to select the file where to save the config

        The combobox will be filled with all the config files from the same
        folder as the config selected
        """
        currentConfigDir = self._iopm.get_active_config_path()
        if currentConfigDir is None:
            return

        currentConfigDir = currentConfigDir.parent
        path_str, _ = QFileDialog.getSaveFileName(
            self, 'Duplicate Config File', str(currentConfigDir),
            'Config (*.ini)'
        )
        if path_str:
            self._iopm.change_config(
                Path(path_str),
                IOPhaseGuiManager.ConfigChangeMode.DUPLICATE)
            self._populateConfigSelectionBox()

    def _deleteConfig(self) -> None:
        """ Delete the current config after displaying a message box

        Will select the first config present (in alphabetical order) in the
        Combobox. If no config is present, will display the "no config found"
        selection box.
        """
        configPath = self._iopm.get_active_config_path()
        if configPath is None:
            return
        configName = configPath.name

        # Display message box
        msgBox = QMessageBox(parent=self)
        msgBox.setText('Are you sure you want to delete the config?')
        msgBox.setInformativeText(f'Name: {configName}')
        msgBox.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        msgBox.setDefaultButton(QMessageBox.StandardButton.No)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        ret = msgBox.exec()

        # Delete the config
        if ret == QMessageBox.StandardButton.Yes:
            index = self._configSelectionBox.currentIndex()
            length = self._configSelectionBox.count()
            if length >= 2:
                if index == 0:
                    new_path = Path(self._configSelectionBox.itemData(1))
                else:
                    new_path = Path(self._configSelectionBox.itemData(0))
            else:
                new_path = None

            self._iopm.change_config(
                new_path,
                IOPhaseGuiManager.ConfigChangeMode.DELETE)
            self._populateConfigSelectionBox()

    def _populateConfigSelectionBox(self) -> None:
        """ Populate the combobox with all the ini files that are present in
        the same folder than the current selected config.
        """
        self._configSelectionBox.blockSignals(True)

        # Get current config
        current_config_path = self._iopm.get_active_config_path()
        if current_config_path is None:
            self._configSelectionBox.blockSignals(False)
            return

        current_config_dir = current_config_path.parent
        if current_config_path.name[-4:] != '.ini':
            err = f'Config file "{current_config_path}" is not a ".ini".'
            raise QtfException(err)

        # Load all config names
        available_configs = list(current_config_dir.glob('*.ini'))
        available_configs.sort()
        index = available_configs.index(current_config_path)

        # Update config selection box
        self._configSelectionBox.clear()
        for path in available_configs:
            self._configSelectionBox.addItem(str(path.name), path)
        self._configSelectionBox.setCurrentIndex(index)

        self._configSelectionBox.blockSignals(False)

    def _updateResults(self) -> None:
        """Update the calibration results
        """
        pass
