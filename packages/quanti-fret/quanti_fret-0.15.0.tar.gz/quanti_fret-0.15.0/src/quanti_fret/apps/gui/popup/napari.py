from quanti_fret.core import QtfException, TripletSequence
from quanti_fret.io import ResultsManager

from typing import TYPE_CHECKING

import numpy as np


if TYPE_CHECKING:
    import napari  # type: ignore


class NapariPopUpManager:
    """ Popup manager for the Napari mode
    """

    def __init__(self, viewer: "napari.viewer.Viewer") -> None:
        """ Constructor

        Args:
            viewer (napari.viewer.Viewer): Napari viewer linked with the plugin
        """
        self._viewer = viewer
        self._axis_labels = ['triplet', 'channel', 'y', 'x']
        self._colormap = 'plasma'

    def openSequence(self, seq: TripletSequence) -> None:
        """ Open the given Triplet sequence

        This will add the sequence to the viewer

        Args:
            seq (TripletSequence): sequence to open
        """
        # Create name
        subfolder = str(seq.subfolder)
        if subfolder == '' or subfolder == '.':
            subfolder = seq.folder.name
        name = f'Sequence - {subfolder}'

        # Check if image is already opened
        napari_id = self._getImageId(name)

        if napari_id != -1:
            # Juste select the image id
            array = self._viewer.layers[napari_id].data
        else:
            # Load the sequence
            array = seq.as_numpy
            if seq.have_all_mask_cell():
                cells = np.expand_dims(seq.mask_cells, axis=1)
                array = np.append(array, cells, axis=1)
            if seq.have_all_mask_bckg():
                bckgs = np.expand_dims(seq.mask_bckgs, axis=1)
                array = np.append(array, bckgs, axis=1)
            self._viewer.add_image(
                array,
                name=name,
                colormap=self._colormap,
            )

        # Set the axis and select the triplet
        self._viewer.dims.axis_labels = self._axis_labels
        self._viewer.dims.ndisplay = 2
        self._viewer.dims.current_step = (
            0,
            0,
            int(array.shape[-2] / 2),
            int(array.shape[-1] / 2)
        )

    def openFretResult(self, id: int, resultManager: ResultsManager) -> None:
        """ Open the given Triplet results

        Args:
            id (int): Id of the triplet to open
        """
        # Find sequence id and path
        ids = resultManager['fret'].get_triplet_ids()
        matches = [i for i in ids if i[0] == id]
        if len(matches) != 1:
            raise QtfException(f'Error while fetching id #{id}')
        seq_id = matches[0][1]
        seq_path = matches[0][3]
        triplet_id = matches[0][2]

        # Create the image name
        name = f'Fret Result #{id} - {seq_path}'

        # Check if the image is not already displayed
        napari_id = self._getImageId(name)

        if napari_id != -1:
            # Just select the image
            array = self._viewer.layers[napari_id].data
        else:
            # Create array and plot it
            array_list = []
            for i in [i for i in ids if i[1] == seq_id]:
                res = resultManager['fret'].get_triplet_results(i[0])
                assert res is not None
                array = np.stack(res, axis=0)
                array_list.append(array)
            array = np.stack(array_list, axis=0)
            self._viewer.add_image(
                array,
                name=name,
                colormap=self._colormap
            )

        # Set the axis and select the triplet
        self._viewer.dims.axis_labels = self._axis_labels
        self._viewer.dims.ndisplay = 2
        self._viewer.dims.current_step = (
            triplet_id - 1,
            0,
            int(array.shape[-2] / 2),
            int(array.shape[-1] / 2)
        )

    def openArray(self, array: np.ndarray) -> None:
        """ Open a multidimentional array

        Implemented only in napari mode

        Args:
            array_list (Figure): 3D Array to open
        """
        # Create the image name
        name = 'XM - 3D Plane'

        # Check if the image is not already displayed
        napari_id = self._getImageId(name)

        # Open it if not already opened
        if napari_id == -1:
            self._viewer.add_points(
                array,
                name=name,
            )
        self._viewer.dims.ndisplay = 3

    def _getImageId(self, name: str) -> int:
        """ Check if the id of the image represented by the given name

        Args:
            name (str): name used to look for the image

        Returns:
            int: Id of the image. If the image doesn't exists, returns -1
        """
        napari_id = -1
        i = 0
        for image in self._viewer.layers:
            if image.name == name:
                napari_id = i
                break
            i += 1
        return napari_id
