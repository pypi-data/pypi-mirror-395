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
        self._default_axis_labels = ['Triplet #', 'y', 'x']
        self._3d_plane_axis_labels = ['DD', 'DA', 'AA']
        self._sequence_colormap = 'gray'
        self._fret_colormap = 'plasma'

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
        names = [
            f'Seq - {subfolder} [DD]',
            f'Seq - {subfolder} [DA]',
            f'Seq - {subfolder} [AA]',
            f'Seq - {subfolder} [Cell]',
            f'Seq - {subfolder} [Bckg]',
        ]

        # Load the triplets if needed
        if any(self._getImageId(names[i]) == -1 for i in range(3)):
            array = seq.as_numpy
            shape = array.shape
        else:
            array = self._viewer.layers[0].data
            shape = self._viewer.layers[0].data.shape

        # Display the 3 channels if not already opened
        for i in range(3):
            if self._getImageId(names[i]) == -1:
                self._viewer.add_image(
                    array[:, i, ...],
                    name=names[i],
                    colormap=self._sequence_colormap,
                )

        # Load the mask cell if needed
        if seq.have_all_mask_cell():
            if self._getImageId(names[3]) == -1:
                cells = np.expand_dims(seq.mask_cells, axis=1)
                self._viewer.add_image(
                    cells,
                    name=names[3],
                    colormap=self._sequence_colormap,
                )

        if seq.have_all_mask_bckg():
            if self._getImageId(names[4]) == -1:
                bckgs = np.expand_dims(seq.mask_bckgs, axis=1)
                self._viewer.add_image(
                    bckgs,
                    name=names[4],
                    colormap=self._sequence_colormap,
                )

        # Set the axis and select the triplet
        self._2d_viewer()
        self._viewer.dims.current_step = (
            0,
            int(shape[-2] / 2),
            int(shape[-1] / 2)
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
        res_ids = [i for i in ids if i[1] == seq_id]
        min_triplet_id = min(res_ids)[0]
        max_triplet_id = max(res_ids)[0]
        if len(res_ids) > 1:
            fret_id = f'(#{min_triplet_id} -> #{max_triplet_id})'
        else:
            fret_id = f'#{min_triplet_id}'
        names = [
            f'Fret {fret_id} - {seq_path} [E]',
            f'Fret {fret_id} - {seq_path} [Ew]',
            f'Fret {fret_id} - {seq_path} [S]',
        ]

        # Load the result if needed
        if any(self._getImageId(names[i]) == -1 for i in range(len(names))):
            array_list = []
            for i in res_ids:
                res = resultManager['fret'].get_triplet_results(i[0])
                assert res is not None
                array = np.stack(res, axis=0)
                array_list.append(array)
            array = np.stack(array_list, axis=0)
            shape = array.shape
        else:
            array = None
            shape = self._viewer.layers[0].data.shape

        # Display the 3 layers if not already opened
        for name_id in range(len(names)):
            napari_id = self._getImageId(names[name_id])
            if napari_id == -1:
                # Plot the array
                assert array is not None
                self._viewer.add_image(
                    array[:, name_id, ...],
                    name=names[name_id],
                    colormap=self._fret_colormap,
                )

        # Set the axis and select the triplet
        self._2d_viewer()
        self._viewer.dims.current_step = (
            triplet_id - 1,
            int(shape[-2] / 2),
            int(shape[-1] / 2)
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
            scale_factors = array[:, 0].max() / array.max(axis=0)
            self._viewer.add_points(
                array,
                name=name,
                scale=scale_factors,
                border_width_is_relative=True,
                border_width=0.,
            )

        self._3d_viewer()
        self._viewer.camera.angles = (90, 45, 45)
        self._viewer.camera.zoom = 1.5

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

    def _2d_viewer(self) -> None:
        """ Put the viewer in 2D mode
        """
        self._viewer.dims.axis_labels = self._default_axis_labels
        self._viewer.dims.ndisplay = 2
        self._viewer.axes.visible = False

    def _3d_viewer(self) -> None:
        """ Put the viewer in 3D mode
        """
        self._viewer.dims.axis_labels = self._3d_plane_axis_labels
        self._viewer.dims.ndisplay = 3
        self._viewer.axes.visible = True
