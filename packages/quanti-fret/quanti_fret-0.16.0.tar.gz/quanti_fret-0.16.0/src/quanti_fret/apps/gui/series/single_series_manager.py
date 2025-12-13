from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.series.triplet_scanner import TripletScannerWidget

from pathlib import Path

from qtpy.QtCore import QObject, Signal
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)


class SingleSeriesManager(QObject):
    """ Manage triplet sequences settings for a specific series.

    It provides two widgets:
        * A title widget that can be highlighted and that contains the
            following informations:
            * series name
            * Number of sequences selected for this series
            * A button to select this manager
        * A settings widget allowing you to select the sequences for this
            series

    This class provides the following signals
        * seriesManagerSelected: emitted when the user pressed the manager's
            title `set` button. The manager's object is passed as parameter.
        * sequenceEnabledStateChanged: Signal that a sequence enable state
            was updated, giving the path to the sequence folder.
    """
    seriesManagerSelected = Signal(object)
    sequenceEnabledStateChanged = Signal(object, Path)

    def __init__(
        self, series: str, phase: str, parent: QWidget, no_set: bool = False
    ) -> None:
        """ Constructor

        Args:
            series (str): Name of the series managed by this manager.
            phase (str): Phase linked with the manager.
            parent (QWidget): Parent to associate to the widgets created.
            no_set (bool): If no_set is True, we expect the series to be always
                visible, so no set button will be shown, and no highlight f
                frame can be displayed
        """
        super().__init__()
        self._series = series
        self._parent = parent
        self._no_set = no_set
        self._highlighted = False
        self._iopm = IOGuiManager().get_iopm(phase)
        self._titleWidget = self._buildTitleWidget()
        self._title_id = f'Title_{phase}_{series}'
        self._titleWidget.setObjectName(self._title_id)
        self._iopm.stateChanged.connect(self._update_title)
        self._settingsWidget = TripletScannerWidget(
            self._series, phase, parent=parent
        )
        self._settingsWidget.sequenceEnabledStateChanged.connect(
            lambda path: self.sequenceEnabledStateChanged.emit(self, path)
        )
        self._update_title()
        self.highlight(False)
        if self._no_set:
            self._detailsButton.hide()

    @property
    def titleWidget(self) -> QWidget:
        """Getter of the title widget

        Returns:
            QWidget: The title widget
        """
        return self._titleWidget

    @property
    def settingsWidget(self) -> QWidget:
        """Getter of the settings widget

        Returns:
            QWidget: The settings widget
        """
        return self._settingsWidget

    def highlight(self, value: bool) -> None:
        """Highlight or not the title widget and display or not the settings.

        A highlighted title will surround itself with a frame box.

        If the widget is already highlighted, will unhighlight it instead

        Args:
            value (bool): True to highlight, False to unhighlight.
        """
        # If no set, ignore
        if self._no_set:
            return

        # Check if the title needs to be highlighted or not
        if value:
            if not self._highlighted:
                highlight = True
            else:
                highlight = False
        else:
            highlight = False

        # Highlight or not the title
        if highlight:
            self._titleWidget.setStyleSheet(
                f'QFrame#{self._title_id} {{ border: 1px solid gray;}}'
            )
            self._titleWidget.layout().setContentsMargins(  # type: ignore
                0, 0, 0, 0)
            self._detailsButton.setText('-')
            self._settingsWidget.show()
            self._highlighted = True
        else:
            self._titleWidget.setStyleSheet(
                f'QFrame#{self._title_id} {{ border: 0px solid gray;}}'
            )
            self._titleWidget.layout().setContentsMargins(  # type: ignore
                1, 1, 1, 1)
            self._detailsButton.setText('+')
            self._settingsWidget.hide()
            self._highlighted = False

    def externalSeriesSequenceEnabledStateChanged(self, path: Path) -> None:
        """ Update the series if an external series with a same sequence
        updated it's enabled state value

        Args:
            path (Path): Path to the sequence that was updated
        """
        self._settingsWidget.externalSeriesSequenceEnabledStateChanged(path)

    def reloadSeries(self) -> None:
        """ Force to reload the series
        """
        self._settingsWidget.reloadSeries()

    def _buildTitleWidget(self) -> QFrame:
        """ Builds and returns the title widget.

        Returns:
            QFrame: The title widget
        """
        # Widget
        widget = QFrame(parent=self._parent)
        widget.setFrameShadow(QFrame.Shadow.Plain)

        # Layout
        titleWidget = QHBoxLayout()
        titleWidget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(titleWidget)

        # Series label
        self._titleLabel = QLabel(parent=widget)
        titleWidget.addWidget(self._titleLabel)

        # Set Button
        self._detailsButton = QPushButton(parent=widget)
        font = self._detailsButton.font()
        font.setBold(True)
        font.setPointSize(int(font.pointSize() * 1.4))
        self._detailsButton.setFont(font)
        self._detailsButton.setMinimumSize(25, 25)
        self._detailsButton.setMaximumSize(50, 50)
        titleWidget.addWidget(self._detailsButton)
        self._detailsButton.clicked.connect(
            lambda: self.seriesManagerSelected.emit(self))

        return widget

    def _update_title(self):
        """Update the title label

        Args:
            nb_frames (int): the number of selected frames
        """
        nb_frames = self._iopm.series.get(self._series).size
        msg = f'{self._series.capitalize()} ({nb_frames})'
        self._titleLabel.setText(msg)
