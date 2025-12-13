from quanti_fret.core import QtfException, TripletSequence
from quanti_fret.io import ResultsManager

from qtpy.QtCore import QUrl
from qtpy.QtGui import QDesktopServices

import numpy as np


class StandalonePopUpManager:
    """ PopUp manager for the Standalone Mode
    """

    def openSequence(self, seq: TripletSequence) -> None:
        """ Open the given Triplet sequence

        This will launch the OS's file manager at the sequence's location

        Args:
            seq (TripletSequence): sequence to open
        """
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(seq.folder)))

    def openFretResult(self, id: int, resultManager: ResultsManager) -> None:
        """ Open the given Triplet results

        Args:
            id (int): Id of the triplet to open
        """
        path = resultManager['fret'].get_triplet_results_path(id)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def openArray(self, array: np.ndarray) -> None:
        """ Open a multidimentional array

        Implemented only in napari mode

        Args:
            array_list (Figure): 3D Array to open
        """
        err = '`openArray` is not implemented for StandalonePopUpManager'
        raise QtfException(err)
