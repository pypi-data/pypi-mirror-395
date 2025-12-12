from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.utils import CollapsibleBox
from quanti_fret.io import TripletSequenceLoader

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class RegexBox(CollapsibleBox):
    """ Widget allowing you to set the regex for all the triplets' files path

    It has a title that you can click to show or hide the regex settings.

    I comes with a reload button allowing the user to reload all the series
    once all the regexes have been set

    Can emit the following signals:
        * reloadTriggered: The reload series button have been triggered
    """
    reloadTriggered = Signal()

    def __init__(self, phase: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            phase (str): phase associated with the regexes
        """
        super().__init__('Regex', *args, **kwargs)

        self._phase = phase

        # Build GUI
        self._fillContent()

    def _fillContent(self) -> None:
        """ Build the content of the widget
        """
        # Content layout
        layout = QVBoxLayout()
        layout.setSpacing(2)
        self.addContentLayout(layout)

        # Regex widgets
        widgets = [
            RegexWidget(self._phase, 'dd', self._content),
            RegexWidget(self._phase, 'da', self._content),
            RegexWidget(self._phase, 'aa', self._content),
            RegexWidget(self._phase, 'mask_cell', self._content),
            RegexWidget(self._phase, 'mask_bckg', self._content),
        ]
        width = max([w.getTitleWidth() for w in widgets])
        for w in widgets:
            w.setTitleWidth(width)
            layout.addWidget(w)

        # Reload button
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(buttonLayout)
        reloadButton = QPushButton('Reload Series', parent=self._content)
        buttonLayout.addWidget(reloadButton)
        reloadButton.clicked.connect(lambda: self.reloadTriggered.emit())


class RegexWidget(QWidget):
    """ Handle the setting of a regex

    Will display a title alongside with a line edit that will update the config
    on change.
    """

    def __init__(
        self, phase: str, config_key: str, *args, **kwargs
    ) -> None:
        """ Constructor

        Args:
            phase (str): Phase linked with the scanner.
            config_key (str): Key associated in the config.
        """
        super().__init__(*args, **kwargs)

        self._phase = phase
        self._config_key = config_key
        self._iopm = IOGuiManager().get_iopm(phase)

        self._buildGui()

        self._iopm.stateChanged.connect(self._updatedConfig)
        self._updatedConfig()

    def setTitleWidth(self, width: int) -> None:
        """ Set the width of the title

        This function helps having all regex title sharing the same width

        Args:
            width (int): width to set
        """
        self._title.setMinimumWidth(width)
        self._title.setMaximumWidth(width)

    def getTitleWidth(self) -> int:
        """ Get the current width of the title

        This function helps having all regex title sharing the same width

        Returns:
            int: The width of the title
        """
        return self._title.minimumSizeHint().width()

    def _buildGui(self) -> None:
        """ Build the GUI
        """
        # Layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        self._title = QLabel(f'{self._config_key.upper()}:', parent=self)
        layout.addWidget(self._title)

        # Line Edit
        self._lineEdit = QLineEdit(parent=self)
        self._lineEdit.setPlaceholderText(
            TripletSequenceLoader.DEFAULT_REGEX_PATTERNS[
                f'{self._config_key}_path'
            ]
        )
        self._lineEdit.setMaxLength(100)
        layout.addWidget(self._lineEdit)
        self._lineEdit.editingFinished.connect(self._updateRegex)

    def _updatedConfig(self) -> None:
        """ Update the line edit with the value from the config
        """
        self._lineEdit.blockSignals(True)
        val = self._iopm.config.get('Regex', self._config_key)
        self._lineEdit.setText(val)
        self._lineEdit.blockSignals(False)

    def _updateRegex(self) -> None:
        """ Update the config with the value from the widget
        """
        val = self._lineEdit.text()
        self._iopm.config.set('Regex', self._config_key, val)
