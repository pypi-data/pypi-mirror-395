from quanti_fret.apps.gui.config import ConfigManagementWidget
from quanti_fret.apps.gui.io_gui_manager import IOPhaseGuiManager

from quanti_fret.io import CalibrationConfig

import abc
from pathlib import Path
import traceback

from qtpy.QtCore import QObject, Qt
from qtpy.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class QABCMeta(abc.ABCMeta, type(QObject)):  # type: ignore
    """ Metaclass to allow a QObject to have an abc.ABCMeta metaclass
    """
    pass


class PhaseWidget(QWidget, metaclass=QABCMeta):
    """ Widget managing a whole phase of the App

    It contains two widgets that are never shown at the same time.
        * A QTabWidget named self._stages containing the differents widget of
            the phase.
        * A Widget named self._configErrorWidget that handle the case where no
            valid configuration is available.

    If no config is available, this widget provides 3 options:
        * Use the default config
        * Open a custom config
        * Create a new empty config.
    If the selected config is invalid, in addition to the 3 options above, this
        widget also provides the following options:
        * Traceback: Get the traceback of the error
        * Try fix: Try to fix the error in the config
        * Reset to Default: Set the config values to the defaults ones.
    """
    def __init__(self, iopm: IOPhaseGuiManager, *args, **kwargs) -> None:
        """Constructor

        Args:
            iopm (IOPhaseGuiManager) IOPM associated with the phase
        """
        super().__init__(*args, **kwargs)

        # Setup  iom
        self._iopm = iopm
        self._iopm.noConfig.connect(self._showMissingConfig)
        self._iopm.errorConfig.connect(self._showErrorConfig)

        # Setup attribute for config error
        self._traceback = ""
        self._errorConfigPath: Path | None = None

        # Gui
        self._stages: QTabWidget | None = None
        self._configWidget: ConfigManagementWidget | None = None
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)  # type: ignore
        self._buildConfigError()
        if self._iopm.load_active_config():
            self._configErrorWidget.hide()
            self._buildStagesTab()

    @abc.abstractmethod
    def _buildStagesTab(self) -> None:
        """Create the tab widget that will host the different stages of the
        QuanTI-FRET phase.
        """
        pass

    def _buildConfigError(self) -> None:
        """ Build the widgets to show when no config files is found or when
        a config contains errors
        """
        mainLayout = self.layout()
        assert mainLayout is not None

        # Config Error Widget
        self._configErrorWidget = QWidget(parent=self)
        mainLayout.addWidget(self._configErrorWidget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self._configErrorWidget.setLayout(layout)

        # Message to Display
        self._configMessage = QLabel(
            'No Config File Found!', parent=self._configErrorWidget
        )
        self._configMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._configMessage)

        # Button to fix the config
        self._fixButtonWidget = QWidget(parent=self._configErrorWidget)
        fixButtonLayout = QHBoxLayout()
        fixButtonLayout.setContentsMargins(0, 0, 0, 0)
        fixButtonLayout.setSpacing(20)
        self._fixButtonWidget.setLayout(fixButtonLayout)
        layout.addWidget(self._fixButtonWidget)
        tracebackButton = QPushButton(
            'Traceback', parent=self._fixButtonWidget
        )
        fixButtonLayout.addWidget(tracebackButton)
        tracebackButton.clicked.connect(self._showTraceback)
        tryfixButton = QPushButton(
            'Try Fix', parent=self._fixButtonWidget
        )
        fixButtonLayout.addWidget(tryfixButton)
        tryfixButton.clicked.connect(self._tryFix)
        defaultButton = QPushButton(
            'Reset to Default', parent=self._fixButtonWidget
        )
        fixButtonLayout.addWidget(defaultButton)
        defaultButton.clicked.connect(self._setToDefault)
        self._fixButtonWidget.hide()

        # Buttons to select a new config
        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)
        useBaseButton = QPushButton(
            'Use Default Config', parent=self._configErrorWidget
        )
        buttonLayout.addWidget(useBaseButton)
        useBaseButton.clicked.connect(self._openDefaultConfig)
        createCustomButton = QPushButton(
            'Create Custom File', parent=self._configErrorWidget
        )
        buttonLayout.addWidget(createCustomButton)
        createCustomButton.clicked.connect(self._createCustomConfig)
        openCustomButton = QPushButton(
            'Open Custom File', parent=self._configErrorWidget
        )
        buttonLayout.addWidget(openCustomButton)
        openCustomButton.clicked.connect(self._openCustomConfig)

    def _openDefaultConfig(self) -> None:
        """ Open the default (base) config file.
        """
        if self._iopm.load_base_config():
            self._showStage()

    def _createCustomConfig(self) -> None:
        """ Create a new config file at the user's custom location.
        """
        # Get current config dir to start the fileDialog at the same location
        path = self._iopm.get_active_config_path()
        if path is None:
            dir = None
        else:
            dir = str(path.parent)

        # Select the file
        path_str, _ = QFileDialog.getSaveFileName(
            self, 'Open Config File', dir, 'Config (*.ini)'
        )

        # Change the config to this file
        if path_str:
            if self._iopm.change_config(
                Path(path_str), IOPhaseGuiManager.ConfigChangeMode.CHANGE
            ):
                self._showStage()

    def _openCustomConfig(self) -> None:
        """ Open the user's custom config file.
        """
        # Get current config dir to start the fileDialog at the same location
        path = self._iopm.get_active_config_path()
        if path is None:
            dir = None
        else:
            dir = str(path.parent)

        # Select the file
        path_str, _ = QFileDialog.getOpenFileName(
            self, 'Open Config File', dir, 'Config (*.ini)'
        )

        # Change the config to this file
        if path_str:
            if self._iopm.change_config(
                Path(path_str), IOPhaseGuiManager.ConfigChangeMode.CHANGE
            ):
                self._showStage()

    def _showMissingConfig(self) -> None:
        """ Show the widgets associated when the active config is missing
        """
        if self._stages is not None:
            self._stages.hide()
        self._configMessage.setText('No Config File Found!')
        self._fixButtonWidget.hide()
        self._configErrorWidget.show()

    def _showErrorConfig(self, path: Path, error: str, traceback: str) -> None:
        """ Show the widget associated when an error was found in the config

        Args:
            path (Path): Path to the config that was loaded
            error (str): Error incontered
            traceback (str): traceback when the error occured
        """
        self._traceback = traceback
        self._errorConfigPath = path
        if self._stages is not None:
            self._stages.hide()
        text = f'Error Found in Config File\n{path}\n\n{error}'
        self._configMessage.setText(text)
        self._fixButtonWidget.show()
        self._configErrorWidget.show()

    def _showTraceback(self) -> None:
        """ Show the trace of the last error incontered in the config
        """
        msgBox = QMessageBox(parent=self)
        msgBox.setText(self._traceback)
        msgBox.setStandardButtons(
            QMessageBox.StandardButton.Close
        )
        msgBox.exec()

    def _setToDefault(self) -> None:
        """ Set default values to the last config that raised an error
        """
        if self._iopm.change_config(
            self._errorConfigPath, IOPhaseGuiManager.ConfigChangeMode.NEW
        ):
            self._showStage()

    def _tryFix(self) -> None:
        """ Try to fix the last config that had an error
        """
        config = CalibrationConfig()
        try:
            assert self._errorConfigPath is not None
            config.load(self._errorConfigPath, accept_missing_keys=True)
            config.save(self._errorConfigPath)
            if self._iopm.change_config(
                self._errorConfigPath,
                IOPhaseGuiManager.ConfigChangeMode.CHANGE
            ):
                self._showStage()
        except Exception:
            msgBox = QMessageBox(parent=self)
            msgBox.setText(traceback.format_exc())
            msgBox.setStandardButtons(
                QMessageBox.StandardButton.Close
            )
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()

    def _showStage(self):
        """ Hide the configErrorWidget and show the stages widget
        """
        self._configErrorWidget.hide()
        if self._stages is None:
            self._buildStagesTab()
        assert self._stages is not None
        self._stages.show()
        assert self._configWidget is not None
        self._configWidget.newConfigSelected()
