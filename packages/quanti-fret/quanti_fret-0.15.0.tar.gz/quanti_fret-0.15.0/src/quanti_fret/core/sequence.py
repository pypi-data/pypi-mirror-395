from quanti_fret.core.exception import QtfException
from quanti_fret.core.triplet import Triplet

import os
from pathlib import Path
from typing import Iterator

import numpy as np


class TripletSequence:
    """ Sequence of triplet representing either an acquisition of a single
    triplet, or of a video.

    Sequence can be enabled or disabled by the presence of the file
    '.qtf_ignore.txt' in the folder.
    """

    def __init__(
        self, triplets: list[Triplet], folder:  os.PathLike | str,
        series_folder: os.PathLike | str | None = None
    ):
        """ Constructor

        Args:
            triplets (list[Triplet]): List of triplet associated with the
                sequence.
            folder (os.PathLike | str): Folder of the sequence.
            series_folder (os.PathLike | str | None, optional): Folder of
                the series associated with this sequence. This is use to
                determine the subfolder of the sequence whithin the series.
                Defaults to None.
        """
        self._triplets = triplets

        self._folder = Path(folder)
        if series_folder is None:
            self._series_folder = None
        else:
            self._series_folder = Path(series_folder)

        self._ignore_file = self._folder / '.qtf_ignore.txt'

    @property
    def as_numpy(self) -> np.ndarray:
        """ Loads an returns the triplets stacked in a numpy array under the
        shape (nb_triplets, 3, img_height, img_width).
        """
        return np.stack([t.as_numpy for t in self._triplets], axis=0)

    @property
    def mask_cells(self) -> np.ndarray:
        """ Loads an returns the triplets' cell mask stacked in a numpy array
        under the shape (nb_triplets, img_height, img_width).
        """
        return np.stack([t.mask_cell for t in self._triplets], axis=0)

    @property
    def mask_bckgs(self) -> np.ndarray:
        """ Loads an returns the triplets' background mask stacked in a numpy
        array under the shape (nb_triplets, img_height, img_width).
        """
        return np.stack([t.mask_bckg for t in self._triplets], axis=0)

    def have_all_mask_cell(self) -> bool:
        """ Check if all the Triplet have a cell mask

        Returns:
            bool: True if all triplet have a cell mask
        """
        return all([t.has_mask_cell() for t in self._triplets])

    def have_all_mask_bckg(self) -> bool:
        """ Check if all the Triplet have a background mask

        Returns:
            bool: True if all triplet have a background mask
        """
        return all([t.has_mask_bckg() for t in self._triplets])

    def is_enabled(self) -> bool:
        """ Returns True if the sequence is enabled. False otherwise
        """
        return not self._ignore_file.is_file()

    def set_enabled(self, val: bool) -> None:
        """ Set the enabled state of the sequence

        I the sequence goes from disabled to enabled, it deletes the ignore
        file in the sequence's folder. In the other way arround, it creates
        the file.

        Args:
            val (bool): Value to set
        """
        if val:
            self._ignore_file.unlink(missing_ok=True)
        else:
            self._ignore_file.touch(exist_ok=True)

    @property
    def size(self) -> int:
        """ Returns the number of triplets

        Returns:
            int: number of triplets
        """
        return len(self._triplets)

    def __getitem__(self, index: int) -> Triplet:
        if index > len(self._triplets):
            raise QtfException('Index out of range')
        return self._triplets[index]

    def __iter__(self) -> Iterator[Triplet]:
        for triplet in self._triplets:
            yield triplet

    @property
    def folder(self) -> Path:
        """ Returns the folder where the sequence is stored.
        """
        return self._folder

    def folder_crop(self, max_length: int, prefix='[...]') -> str:
        """ Utility to get the folder Path as a string cropped to a given
        max length.

        Args:
            max_length (int): max string length (prefix included)
            prefix (str, optional): prefix to put in front of the cropped path

        Returns:
            str: the string representation of the path cropped
        """
        return self._crop_path(self._folder, max_length, prefix)

    @property
    def subfolder(self) -> Path:
        """ Returns the subfolder compared to the series folder if any.
        """
        if self._series_folder is None:
            return self._folder
        else:
            return self._folder.relative_to(self._series_folder)

    def subfolder_crop(self, max_length: int, prefix='[...]') -> str:
        """ Utility to get the subfolder Path as a string cropped to a given
        max length.

        Args:
            max_length (int): max string length (prefix included)
            prefix (str, optional): prefix to put in front of the cropped path

        Returns:
            str: the string representation of the path cropped
        """
        return self._crop_path(self.subfolder, max_length, prefix)

    def _crop_path(
        self, path: Path, max_length: int, prefix: str = '[...]'
    ) -> str:
        """ Utility to get the a Path as a string cropped to a given max
        length.

        Args:
            path (Path): path to crop
            max_length (int): max string length (prefix included)
            prefix (str, optional): prefix to put in front of the cropped path

        Returns:
            str: the string representation of the path cropped
        """
        if len(prefix) > max_length - 1:
            raise QtfException('Prefix is too big compared to max_length')
        path_s = str(path)
        if len(path_s) > max_length:
            new_path_len = max_length - len(prefix)
            path_s = path_s[-new_path_len:]
            path_s = f'{prefix}{path_s}'
        return path_s
