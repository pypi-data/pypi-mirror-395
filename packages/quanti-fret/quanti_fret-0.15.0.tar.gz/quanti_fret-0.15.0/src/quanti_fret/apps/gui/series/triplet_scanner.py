from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.path import PathWidget
from quanti_fret.apps.gui.popup import PopUpManager
from quanti_fret.apps.gui.utils import EyeWidget
from quanti_fret.core import QtfSeries, TripletSequence
from quanti_fret.io import TripletSequenceLoader, TripletScanner


from pathlib import Path

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QGroupBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class TripletScannerWidget(QWidget):
    """ Handle the the selection of the folder on which to look for
    triplet sequences.

    The user will be ask to select a folder, and then select the sequences
    he wants to be used from the list displayed.

    It comes with the following signals:
        * sequenceEnabledStateChanged: Signal that a sequence enable state
            was updated, giving the path to the sequence folder.
    """
    sequenceEnabledStateChanged = Signal(Path)

    def __init__(self, name: str, phase: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            name (str): Name of the series of sequences to look for.
            phase (str): Phase linked with the scanner.
        """
        super().__init__(*args, **kwargs)

        # Internal setup
        self._name = name
        self._folder: Path | None = None
        self._series: QtfSeries = QtfSeries([])
        self._puManager = PopUpManager()
        self._phase = phase

        # Manage table displayed with enabled column or not
        self._exclude_disabled_seq = phase == 'calibration'
        self._viewColumnIndex = 0
        if self._exclude_disabled_seq:
            self._tableHeaders = ['View', 'Enabled', 'Triplets', 'Path']
            self._columnsCount = 4
            self._enabledColumnIndex = 1
            self._tripletsColumnIndex = 2
            self._pathColumnIndex = 3
        else:
            self._tableHeaders = ['View', 'Triplets', 'Path']
            self._columnsCount = 3
            self._enabledColumnIndex = -1
            self._tripletsColumnIndex = 1
            self._pathColumnIndex = 2

        # Gui SetUp
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self._buildTitle()
        self._buildFolderSelectorBox()
        self._buildResultsBox()

        # Retrieve previous config
        self._iopm = IOGuiManager().get_iopm(phase)
        self._config = self._iopm.config
        self._updateSeriesFromConfig()
        self._iopm.stateChanged.connect(self._updateSeriesFromConfig)

    def externalSeriesSequenceEnabledStateChanged(self, path: Path) -> None:
        """ Update the series if an external series with a same sequence
        updated it's enabled state value

        Args:
            path (Path): Path to the sequence that was updated
        """
        if self._exclude_disabled_seq:
            for seq in self._series:
                if seq.folder == path:
                    self._fillTripletSequencesListWidget()
                    return

    def reloadSeries(self) -> None:
        """ Force to reload the series
        """
        self._seqTableWidget.blockSignals(True)

        self._setSeriesFolder(
            self._config.get('Series', self._name),
            force_reset=True
        )

        self._seqTableWidget.blockSignals(False)

    def _buildTitle(self) -> None:
        """ Build the TripletSequence series title
        """
        title = QLabel(self._name.capitalize(), parent=self)
        self.layout().addWidget(title)  # type: ignore

    def _buildFolderSelectorBox(self) -> None:
        """ Build the selector box widget where the user will choose the
        folder containing the triplet sequences.
        """
        # Box
        fSelectBox = PathWidget(
            self._phase, ('Series', self._name), 'folder',
            f"Select Folder for {self._name.capitalize()}'s Series",
            parent=self
        )
        self.layout().addWidget(fSelectBox)  # type: ignore

    def _buildResultsBox(self) -> None:
        """ Create the box that display the result of the triplet scan, and
        let the user decide which sequences to keep or remove.
        """
        # Box
        self._resultBox = QGroupBox('Sequences', parent=self)
        self.layout().addWidget(self._resultBox)  # type: ignore

        # Layout inside the box
        resultLayout = QVBoxLayout()
        self._resultBox.setLayout(resultLayout)

        # Layout for summary information
        rSummaryLayout = QGridLayout()
        resultLayout.addLayout(rSummaryLayout)

        # TripletSequences found label
        self._seqCountLabel = QLabel(parent=self._resultBox)
        rSummaryLayout.addWidget(self._seqCountLabel, 0, 0)

        # TripletSequences selected label
        self._seqSelectedLabel = QLabel(parent=self._resultBox)
        rSummaryLayout.addWidget(self._seqSelectedLabel, 1, 0)

        # Detail table
        self._seqTableWidget = QTableWidget(parent=self._resultBox)
        self._seqTableWidget.setColumnCount(self._columnsCount)
        self._seqTableWidget.setColumnWidth(0, 50)
        self._seqTableWidget.setColumnWidth(1, 50)
        self._seqTableWidget.setColumnWidth(2, 50)
        self._seqTableWidget.verticalHeader().hide()  # type: ignore
        self._seqTableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self._seqTableWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self._seqTableWidget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self._seqTableWidget.cellClicked.connect(self._seqTableClicked)
        self._seqTableWidget.setWordWrap(False)
        resultLayout.addWidget(self._seqTableWidget)

        # Hide by default
        self._resultBox.hide()

    def _setSeriesFolder(self, folder: Path | None, force_reset: bool) -> None:
        """ Set the folder of the series associated with this widget.

        If the folder is different from the previous one, and is not None, it:
            - scan for triplet sequences inside the folder
            - Change the button label to "Change"
            - Create the triplet sequences table widget (which emits the
                seqSelectedChanged signal)
            - Update the triplet sequences count labels
            - Display the result box widget

        Args
            folder (Path | None): Folder to set for the series
            force_reset (bool): If true, force the relead of the series even
                if folder didn't change.
        """
        if self._folder != folder or force_reset:
            self._folder = folder
            if folder is None:
                self._series = QtfSeries([])
            else:
                regex = {
                    'dd_path': '',
                    'da_path': '',
                    'aa_path': '',
                    'mask_cell_path': '',
                    'mask_bckg_path': '',
                }
                for key in regex:
                    regex[key] = self._iopm.config.get('Regex', key[:-5])
                tsl = TripletSequenceLoader(regex)
                self._series = TripletScanner(tsl).scan(folder)
            msg = f"Sequences found: {self._series.size}"
            self._seqCountLabel.setText(msg)
            self._fillTripletSequencesListWidget()
            self._resultBox.show()

    def _updateSeriesFromConfig(self) -> None:
        """ Update the series using the config

        It checks if the config file changed. In this case, it will rescan the
        folders even if the path didn't change
        """
        self._seqTableWidget.blockSignals(True)

        config = self._iopm.config
        if config is self._config:
            force_reset = False
        else:
            force_reset = True
            self._config = config

        self._setSeriesFolder(
            config.get('Series', self._name),
            force_reset=force_reset
        )

        self._seqTableWidget.blockSignals(False)

    def _fillTripletSequencesListWidget(self) -> None:
        """ Fill the sequences table with all the sequencess found by the
        scanner, and select all of them.
        """
        # Reset table
        self._seqTableWidget.clear()
        self._seqTableWidget.setRowCount(self._series.size)

        # Add all sequences
        row = 0
        for seq in self._series:
            self._addSeqTableRow(seq, row)
            row += 1

        # Table settings
        self._seqTableWidget.setHorizontalHeaderLabels(self._tableHeaders)
        header = self._seqTableWidget.horizontalHeader()
        assert header is not None
        header.setStretchLastSection(True)

        # Update Series Manager
        self._update_iopm_series()

    def _addSeqTableRow(self, sequence: TripletSequence, row: int) -> None:
        """ Add the sequence to the seqTableWidget.

        Args:
            sequence (TripletSequence): Sequence to add
            row (int): row to add
        """
        # View Column
        viewItem = EyeWidget(parent=self._seqTableWidget)
        self._seqTableWidget.setCellWidget(
            row, self._viewColumnIndex, viewItem
        )

        # Enabled column
        if self._exclude_disabled_seq:
            enabled_text = 'X' if sequence.is_enabled() else ''
            enabledItem = QTableWidgetItem(enabled_text)
            enabledItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._seqTableWidget.setItem(
                row, self._enabledColumnIndex, enabledItem
            )

        # Triplet Count column
        tripletItem = QTableWidgetItem(str(sequence.size))
        tripletItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self._seqTableWidget.setItem(
            row, self._tripletsColumnIndex, tripletItem
        )

        # Path Column
        subfolder = str(sequence.subfolder)
        if subfolder == "" or subfolder == '.':
            subfolder = sequence.folder.name
        pathItem = QTableWidgetItem(subfolder)
        pathItem.setToolTip(subfolder)
        self._seqTableWidget.setItem(
            row, self._pathColumnIndex, pathItem
        )

    def _seqTableClicked(self, row: int, col: int) -> None:
        """ Handle user that clicked on the seqTable.

        It performs different action depending on the cell that was clicked:
            * View cell: display the sequence
            * Enabled cell: enable or disable the sequence
        """
        if col == self._viewColumnIndex:
            # View button
            self._puManager.openSequence(self._series[row])
        elif col == self._enabledColumnIndex and self._exclude_disabled_seq:
            # Enabled button
            item = self._seqTableWidget.item(row, col)
            assert item is not None
            currentChecked = item.text() == 'X'
            newChecked = not currentChecked
            if newChecked:
                item.setText('X')
            else:
                item.setText('')
            self._series[row].set_enabled(newChecked)
            self.sequenceEnabledStateChanged.emit(self._series[row].folder)
            self._update_iopm_series()

    def _update_iopm_series(self):
        """ Update the IOPM with the current series

        Exclude or not the sequence disabled depending on the value of
        `self._exclude_disabled_seq`.
        """
        if self._exclude_disabled_seq:
            series = self._series.get_only_enabled()
        else:
            series = self._series
        self._iopm.series.set(self._name, series)
