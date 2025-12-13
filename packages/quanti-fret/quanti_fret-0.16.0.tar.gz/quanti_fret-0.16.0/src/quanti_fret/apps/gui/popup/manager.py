from quanti_fret.apps.gui.popup.figure import FigureDialog
from quanti_fret.apps.gui.popup.napari import NapariPopUpManager
from quanti_fret.apps.gui.popup.standalone import StandalonePopUpManager
from quanti_fret.io import ResultsManager

from quanti_fret.core import Singleton, TripletSequence

from typing import Any

from matplotlib.figure import Figure
import numpy as np


class PopUpManager(metaclass=Singleton):
    """ Manage actions that open QuanTI-FRET elements outside of the main
    GUI.

    There are two modes of the manager:
        * Standalone mode (default): Used as a standalone applcation
        * Napari mode: to be used insde Napari as a plugin and to interract
            with Napari

    This manager is a singleton, which means that if you need to set the
    Napari mode, you have to do it only once.

    This does not handle the files/folders Dialogs popup.

    To close all dialogs opened when closing the app, call
    PopUpManager.closeAll() at the en of your program
    """

    def __init__(self) -> None:
        self._viewer: StandalonePopUpManager | NapariPopUpManager
        self._viewer = StandalonePopUpManager()
        self._dialogs: list[FigureDialog] = []

    def setNapariMode(self, viewer: Any) -> None:
        """ Set the Mode to Napari

        Args:
            viewer (napari.viewer.Viewer): Napari Viewer associated with the
                plugin
        """
        self._viewer = NapariPopUpManager(viewer)

    def hasNapariMode(self) -> bool:
        """ Check if the popupmanager is in napari mode or not

        Returns:
            bool: True if in napari mode
        """
        return type(self._viewer) is NapariPopUpManager

    def openSequence(self, seq: TripletSequence) -> None:
        """ Open the given Triplet sequence

        Args:
            seq (TripletSequence): sequence to open
        """
        self._viewer.openSequence(seq)

    def openFretResult(self, id: int, resultManager: ResultsManager) -> None:
        """ Open the given Triplet results

        Args:
            id (int): Id of the triplet to open
        """
        self._viewer.openFretResult(id, resultManager)

    def openFigure(self, figure: Figure, title: str = '') -> None:
        """ Open a Figure into a QDialog

        Args:
            figure (Figure): Figure to open
            title (str, optional): title to set. Default is ''
        """
        dialog = FigureDialog(figure)
        if title != '':
            dialog.setWindowTitle(title)
        dialog.show()
        dialog.closed.connect(self._deleteDialog)
        self._dialogs.append(dialog)

    def openArray(self, array: np.ndarray) -> None:
        """ Open a multidimentional array plane

        Implemented only in napari mode

        Args:
            array_list (Figure): 3D Array to open
        """
        self._viewer.openArray(array)

    def closeAll(self) -> None:
        """Close all opened windows
        """
        self._dialogs.clear()

    def _deleteDialog(self, dialog: FigureDialog) -> None:
        """ Delete the given FigureDialog from the list

        Args:
            dialog (FigureDialog): dialog to delete
        """
        self._dialogs.remove(dialog)
