from quanti_fret.apps.gui.io_gui_manager import IOGuiManager
from quanti_fret.apps.gui.utils import EyeWidget


from pathlib import Path
from typing import Any

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
)


class TripletResultsTable(QTableWidget):
    """ Table that display the results of a stage associated with triplets.

    It comes with the following signal:
        * resultsClicked: The results button of the triplet represented by the
            given id has been clicked
        * plotClicked: The plot button of the triplet represented by the
            given id has been clicked
    """
    resultsClicked = Signal(int)
    plotClicked = Signal(int)

    def __init__(
        self, phase: str, stage: str, *args,
        hasResults: bool = False, hasPlot: bool = False,
        detailIndex: int = -1, **kwargs
    ) -> None:
        """ Constructor

        Args:
            phase (str): Phase linked with the results.
            stage (str): Name of the stage of the result.
            hasResults (bool, optional): Enable the results column. Default to
                False
            hasPlot (bool, optional): Enable the plot column. Default to False
            detailIndex (int, optional): Index on the settings returned by the
                results manager that describe if we can expect extra results or
                not. If -1, will always be activated. If Default to -1
        """
        super().__init__(*args, **kwargs)

        # Internal setup
        self._iopm = IOGuiManager().get_iopm(phase)
        self._stage = stage
        self._hasResults = hasResults
        self._hasPlot = hasPlot
        self._detailIndex = detailIndex

        # Table columns
        col = 0
        self._tableHeaders = []
        # Id
        self._idColumnIndex = col
        self._tableHeaders.append('Id')
        col += 1
        # Results
        if hasResults:
            self._resColumnIndex = col
            self._tableHeaders.append('Res')
            col += 1
        else:
            self._resColumnIndex = -1
        # Plot
        if hasPlot:
            self._plotsColumnIndex = col
            self._tableHeaders.append('Plots')
            col += 1
        else:
            self._plotsColumnIndex = -1
        # Path
        self._pathColumnIndex = col
        col += 1
        self._tableHeaders.append('Sequence (Triplet)')
        # Col count
        self._columnsCount = col

        # Column width
        self.setColumnCount(self._columnsCount)
        self.setColumnWidth(self._idColumnIndex, 25)
        if self._hasResults:
            self.setColumnWidth(self._resColumnIndex, 50)
        if self._hasPlot:
            self.setColumnWidth(self._plotsColumnIndex, 50)
        self.verticalHeader().hide()  # type: ignore

        # Cells settings
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.setWordWrap(False)
        self.setTextElideMode(Qt.TextElideMode.ElideLeft)

        # Fill table
        self._fillTable()

        # Connect  Signals
        self.cellClicked.connect(self._tableClicked)
        self._iopm.stateChanged.connect(self._fillTable)

    def _fillTable(self) -> None:
        """ Create the table using the result manager
        """
        self.blockSignals(True)

        # Get tripelts ids
        ids = self._iopm.results[self._stage].get_triplet_ids()

        # Reset table
        self.clear()
        self.setRowCount(len(ids))

        # Check if we need to enable the plot column:
        enablePlots = True
        if self._detailIndex != -1:
            settings = self._iopm.results[self._stage].get_stage_settings()
            if settings is not None:
                enablePlots = settings[self._detailIndex]
            else:
                enablePlots = False

        # Add all triplets
        for row in range(len(ids)):
            self._addTableRow(ids[row], row, enablePlots)

        # Table settings
        self.setHorizontalHeaderLabels(self._tableHeaders)
        header = self.horizontalHeader()
        assert header is not None
        header.setStretchLastSection(True)

        # Table height
        header = self.horizontalHeader()
        assert header is not None
        # Normally, the correct formula is without the height multiplied by 1.5
        # but it fails on napti I don't know why so I leave it like that
        total = header.height() * 1.5 + self.frameWidth() * 2
        row = 0
        for row in range(self.rowCount()):
            total += self.rowHeight(row)
            if row >= 10:
                break
        self.setFixedHeight(int(total))

        self.blockSignals(False)

    def _addTableRow(
        self, ids: tuple[int, int, int, Path], row: int, enablePlots: bool
    ) -> None:
        """ Add the row to the table.

        Args:
            ids (tuple[int, int, int, Path]): Ids associated with the triplet
                to add
            row (int): row index to add
            enablePlots (bool): If set to False, will set the plot column to
                disable mode
        """
        # Id Column
        idItem = QTableWidgetItem(str(ids[0]))
        idItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, self._idColumnIndex, idItem)

        # Results Column
        if self._hasResults:
            resItem = EyeWidget(parent=self)
            self.setCellWidget(row, self._resColumnIndex, resItem)

        # plot Column
        if self._hasPlot:
            plotItem = EyeWidget(parent=self)
            plotItem.setEnabled(enablePlots)
            self.setCellWidget(row, self._plotsColumnIndex, plotItem)

        # Path column
        path = f'{ids[3]} ({ids[2]})'
        pathItem = QTableWidgetItem(path)
        pathItem.setToolTip(path)
        self.setItem(row, self._pathColumnIndex, pathItem)

    def _tableClicked(self, row: int, col: int) -> None:
        """ Handle user that clicked on the Table.

        It will emit different triggers depending on the cell that was clicked:
            * plot cell: display the triplets plots
        """
        if col == self._resColumnIndex and self._hasResults:
            idItem = self.item(row, self._idColumnIndex)
            resItem = self.cellWidget(row, self._resColumnIndex)
            if idItem is None or resItem is None:
                return
            if resItem.isEnabled():
                id = int(idItem.text())
                self.resultsClicked.emit(id)
        if col == self._plotsColumnIndex and self._hasPlot:
            idItem = self.item(row, self._idColumnIndex)
            plotItem = self.cellWidget(row, self._plotsColumnIndex)
            if idItem is None or plotItem is None:
                return
            if plotItem.isEnabled():
                id = int(idItem.text())
                self.plotClicked.emit(id)

    def _extras_enabled(self, dictonary: dict[str, Any]) -> bool:
        """ Check if the extra values given match an enabled extra button in
        the table.

        A button is enabled if any extra value exists

        Args:
            dictonary (dict[str, Any]): The extra values to check

        Returns:
            bool: True if enabled.
        """
        if not dictonary:
            return False
        for val in dictonary.values():
            if type(val) is dict:
                ret = self._extras_enabled(val)
                if ret:
                    return True
            else:
                if val:
                    return True
        return False
