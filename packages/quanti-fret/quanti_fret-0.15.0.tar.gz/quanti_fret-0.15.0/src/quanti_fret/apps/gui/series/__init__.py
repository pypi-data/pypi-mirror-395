from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.series.regex import RegexBox
from quanti_fret.apps.gui.series.single_series_manager import (
    SingleSeriesManager
)
from quanti_fret.apps.gui.utils import HLine

from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QVBoxLayout,
    QWidget,
)


class SeriesWidget(QWidget):
    """ Handle the selection of the different series by the user.

    they are expected to select the triplet sequences for the following series:
        * Donor sequences
        * Acceptor sequences
        * Standard sequences
        * Experiments sequences

    The widget is split in 3 parts:
        * A Layout containing all the series title widget (showing their
            name, number of sequences, and a button to change settings)
        * A separator line
        * A layout containing the setting of the selected series manager
    """

    def __init__(self, phase: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            phase (str): Phase linked with the widget.
        """
        super().__init__(*args, **kwargs)

        self._phase = phase

        # Gui SetUp
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)  # type: ignore
        self._buildTitleLayout()
        self._buildSeparator()
        self._buildSettingsDetailsLayout()

        # Create one manager by series
        self._seriesGuiManagers: list[SingleSeriesManager] = []
        series_list = IOGuiManager().get_iopm(phase).series._series
        for series in series_list:
            self._addSingleSeriesManager(series, len(series_list))
        if len(self._seriesGuiManagers) == 1:
            self._selectSingleSeriesManager(self._seriesGuiManagers[0])

    def _selectSingleSeriesManager(
        self, seriesGuiManager: SingleSeriesManager
    ) -> None:
        """Select the series manager.

        Select means highlight the manager's title widget and show its settings
        widget.

        Args:
            seriesGuiManager (SingleSeriesManager): The Manager to select.
        """
        for cm in self._seriesGuiManagers:
            if cm is not seriesGuiManager:
                cm.highlight(False)
        seriesGuiManager.highlight(True)

    def _buildTitleLayout(self) -> None:
        """ Build the layout that will contains all the series managers
        title widgets.
        """
        # Layout for series managers
        self._seriesManagerTitlesLayout = QVBoxLayout()
        self._seriesManagerTitlesLayout.setSpacing(0)
        self.layout().addLayout(  # type: ignore
            self._seriesManagerTitlesLayout
        )

        # Regexes
        self._regexes = RegexBox(self._phase, parent=self)
        self.layout().addWidget(self._regexes)  # type: ignore
        self._regexes.reloadTriggered.connect(self._reloadSeries)

    def _buildSeparator(self) -> None:
        """ Build the separator line between titles and settings
        """
        horizontal_line = HLine(parent=self)
        self.layout().addWidget(horizontal_line)  # type: ignore

    def _buildSettingsDetailsLayout(self) -> None:
        """ Build the layout containing the setting widget of the series
        managers.

        Only one widget will be visible at a time.
        """
        self._settingsDetailsLayout = QVBoxLayout()
        self.layout().addLayout(self._settingsDetailsLayout)  # type: ignore
        self._settingsDetailsLayout.setContentsMargins(0, 0, 0, 0)
        self._settingsDetailsLayout.setSpacing(0)

    def _addSingleSeriesManager(self, series: str, nb_series: int) -> None:
        """ Create and add a manager for the given series.

        Args:
            series (str): The series that the manager should represent.
            nb_series (int): Number of series that will be created.
        """
        no_set = nb_series == 1
        manager = SingleSeriesManager(
            series, self._phase, parent=self, no_set=no_set
        )
        self._seriesManagerTitlesLayout.addWidget(manager.titleWidget)
        self._settingsDetailsLayout.addWidget(manager.settingsWidget)
        manager.seriesManagerSelected.connect(self._selectSingleSeriesManager)
        manager.sequenceEnabledStateChanged.connect(
            self._sequenceEnabledStateChanged
        )
        self._seriesGuiManagers.append(manager)

    def _sequenceEnabledStateChanged(
        self, manager: SingleSeriesManager, path: Path
    ) -> None:
        """ propagate the signal that a Sequences's enabled state changed to
        the managers that did not emit the signal

        Args:
            manager (SingleSeriesManager): Manager that emitted the signal
            path (Path): path to the sequence to update
        """
        for m in self._seriesGuiManagers:
            if m is not manager:
                m.externalSeriesSequenceEnabledStateChanged(path)

    def _reloadSeries(self) -> None:
        """ Force to reload the series
        """
        for m in self._seriesGuiManagers:
            m.reloadSeries()
