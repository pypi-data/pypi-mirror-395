from quanti_fret.core.exception import QtfException

import os
from pathlib import Path

import numpy as np
import tifffile


class Triplet:
    """ Class representing a triplet image.

    A triplet is a collection of the 3 (+2) of the following images, called
    channels, and representing a single acquisition of two snapshots:
    - DD: Donor-Donor channel
    - DA: Donor-Acceptor channel
    - AA: Acceptor-Acceptor channel
    - (MaskCell: Cell mask) -> Optional
    - (MaskBckg: Background mask) -> Optional

    All images can be accessed as properties, which will load the images
    from disk at every call. The main 3 channels can also be stacked in a
    numpy.
    The images are expected to be in TIFF format, and the paths to the images
    are provided at initialization.
    """

    def __init__(
        self,
        dd_path: os.PathLike | str,
        da_path: os.PathLike | str,
        aa_path: os.PathLike | str,
        mask_cell_path: os.PathLike | str = '',
        mask_bckg_path: os.PathLike | str = '',
        img_type: np.typing.DTypeLike | None = np.float32
    ) -> None:
        """ Constructor

        Initializes the Triplet with the paths to the channels images.

        Args:
            dd_path (os.PathLike | str): Path to the DD image.
            da_path (os.PathLike | str): Path to the DA image.
            aa_path (os.PathLike | str): Path to the AA image.
            mask_cell_path (os.PathLike | str, optional): Path to the cell
                mask image. If set to "''", consider the Triplet do not have
                cell Mask. Default to ''
            mask_bckg_path (os.PathLike | str, optional): Path to the
                background mask image. If set to "''", consider the Triplet do
                not have background Mask. Default to ''
            img_type (np.dtype | None): Force the type of the dd/da/aa images.
        """
        self._dd_path = Path(dd_path)
        self._da_path = Path(da_path)
        self._aa_path = Path(aa_path)

        self._mask_cell_path: Path | None = None
        if mask_cell_path != '':
            self._mask_cell_path = Path(mask_cell_path)

        self._mask_bckg_path: Path | None = None
        if mask_bckg_path != '':
            self._mask_bckg_path = Path(mask_bckg_path)

        self._img_type = img_type

    @property
    def dd(self) -> np.ndarray:
        """ Loads and returns the DD channel as a numpy array
        """
        dd = tifffile.imread(self._dd_path)
        if self._img_type is not None:
            dd = dd.astype(self._img_type)
        return dd

    @property
    def da(self) -> np.ndarray:
        """ Loads and returns the DA channel as a numpy array
        """
        da = tifffile.imread(self._da_path)
        if self._img_type is not None:
            da = da.astype(self._img_type)
        return da

    @property
    def aa(self) -> np.ndarray:
        """ Loads and returns the AA channel as a numpy array
        """
        aa = tifffile.imread(self._aa_path)
        if self._img_type is not None:
            aa = aa.astype(self._img_type)
        return aa

    @property
    def as_numpy(self) -> np.ndarray:
        """ Loads an returns the DD/DA/AA channels stacked in a numpy array
        under the shape (3, img_height, img_width).
        """
        return np.stack((self.dd, self.da, self.aa), axis=0)

    @property
    def mask_cell(self) -> np.ndarray:
        """ Loads and returns the cell mask as a numpy array

        Raises:
            QtfException: The triplet do not have a cell mask
        """
        if self._mask_cell_path is None:
            raise QtfException('This triplet does not have a cell mask')
        mask_cell = tifffile.imread(self._mask_cell_path).astype(bool)
        return mask_cell

    @property
    def mask_bckg(self) -> np.ndarray:
        """ Loads and returns the background mask as a numpy array

        Raises:
            QtfException: The triplet do not have a background mask
        """
        if self._mask_bckg_path is None:
            raise QtfException('This triplet does not have a background mask')
        mask_bckg = tifffile.imread(self._mask_bckg_path).astype(bool)
        return mask_bckg

    def has_mask_bckg(self) -> bool:
        """ Check if the Triplet have a background mask

        Returns:
            bool: True if triplet have a background mask
        """
        return self._mask_bckg_path is not None

    def has_mask_cell(self) -> bool:
        """ Check if the Triplet have a cell mask

        Returns:
            bool: True if triplet have a cell mask
        """
        return self._mask_cell_path is not None
