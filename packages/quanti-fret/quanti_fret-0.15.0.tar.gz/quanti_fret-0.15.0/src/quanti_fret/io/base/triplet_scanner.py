from quanti_fret.core import TripletSequence, Triplet, QtfException, QtfSeries

import os
from pathlib import Path
import re


class NumericalSort:
    """ Utility class to sort numerically strings containing numbers.

    It is designed to be used with the `sort()` or `sorted()` function by
    passing the `NumericalSort.key` method to the `key` argument. It splits
    the string into parts, where each part is either a string or an integer.
    The integers are converted to `int` type, so that they are sorted
    numerically rather than lexicographically. This is useful when sorting file
    names or other strings that contain numbers, such as "frame_1", "frame_2",
    "frame_10".
    """
    def __init__(self):
        self.re_numbers = re.compile(r'(\d+)')

    def key(self, value: os.PathLike | str) -> list[str | int]:
        """ key getter for numerical sorting.

        Args:
            value (str): string to be sorted with the other strings

        Returns:
            list[str | int]: string split into parts of strings and integers.
        """
        if isinstance(value, os.PathLike):
            value = str(value)
        parts = self.re_numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts


class TripletSequenceLoader:
    """ Class to Check if a folder contains a valid triplet sequence, and if
    so, loads it into a TripletSequence class.

    To be valid, the folder must contain, for all triplets, the following
    images:
    - DD
    - DA
    - AA
    - MaskCell
    - MaskBkg (optional)
    Note that the sequence can contain only one frame, this mean just one set
    of the above images.

    If one triplet of the sequence has a MaskBkg, we expect all of them to have
    a MaskBkg

    By default, we expect all images
    - to be in a same folder
    - to respect the regex patterns described in DEFAULT_REGEX_PATTERNS
    - to be differenciated by a number in the file name, such as "001_DD.tif",
        if the sequence contains more than one triplet
    The user can overwrite the patterns.
    """

    DEFAULT_REGEX_PATTERNS = {
        'dd_path': r'^.*DD\.tif$',
        'da_path': r'^.*DA\.tif$',
        'aa_path': r'^.*AA\.tif$',
        'mask_cell_path': r'^.*MaskCell\.tif$',
        'mask_bckg_path': r'^.*MaskBkg\.tif$',
    }
    MANDATORIES = [
        'dd_path',
        'da_path',
        'aa_path',
    ]
    OPTIONALS = [
        'mask_cell_path',
        'mask_bckg_path',
    ]

    def __init__(self, regex_patterns: dict[str, str] | None = None):
        """ Constructor

        Initializes the TripletSequenceLoader either with the default regex
        patterns or with the provided ones.

        If you decide to overwrite the default regex patterns, please provide
        a disctionary containing the same keys as `DEFAULT_REGEX_PATTERNS` (not
        all the keys have to be presents). If the value of the overwrite
        dictionarry is an empty string, this key will be ignored

        Args:
            regex_patterns (dict[str, str] | None, optional):
                Overwrite default regex pattern to search for each image
                channel. Defaults to None.
        """
        self._regex_patterns = self.DEFAULT_REGEX_PATTERNS.copy()
        if regex_patterns is not None:
            for key in regex_patterns:
                if key not in self._regex_patterns:
                    raise QtfException(f'Unknown regex pattern key "{key}"')
                else:
                    pattern = regex_patterns[key]
                    if pattern != '':
                        self._regex_patterns[key] = pattern
        self._n_sort = NumericalSort()

    def check_and_load(
        self,
        folder: os.PathLike | str,
        series_folder: os.PathLike | str | None = None,
        verbose: bool = False
    ) -> TripletSequence | None:
        """ Check if a folder contains a valid triplet sequence, and if so,
        loads it into an TripletSequence class.

        Args:
            folder (os.PathLike | str):
                Folder to load the sequence from.
            series_folder (os.PathLike | str):
                If loaded from a series, the path to the series folder.
            verbose (bool, optional):
                To display or not the reason why the sequence is not valid.
                Defaults to False.

        Returns:
            TripletSequence | None:
                The TripletSequence object if the folder is valid,
                otherwise None.
        """

        # Check if the folder is a valid triplet sequence folder
        folder = Path(folder)
        if not folder.is_dir():
            raise ValueError(
                f"The provided path '{folder}' is not a directory.")

        images = self._load_images_matching_patterns(folder)
        triplet_count = self._validate_images(images, folder, verbose)
        if triplet_count == 0:
            return None

        # Sort all file lists in alphebitical and then numerical order
        for key, value in images.items():
            images[key] = sorted(value, key=self._n_sort.key)

        # Fill in optional images with ''
        for key in self.OPTIONALS:
            if len(images[key]) == 0:
                images[key] = [''] * triplet_count

        # Create the Sequence
        triplets = []
        for i in range(triplet_count):
            triplets.append(Triplet(
                dd_path=images['dd_path'][i],
                da_path=images['da_path'][i],
                aa_path=images['aa_path'][i],
                mask_cell_path=images['mask_cell_path'][i],
                mask_bckg_path=images['mask_bckg_path'][i]
            ))
        return TripletSequence(triplets, folder, series_folder)

    def _load_images_matching_patterns(
        self, folder: os.PathLike | str
    ) -> dict[str, list[Path | str]]:
        """ Load all images in the folder that match the regex patterns.

        Args:
            folder (os.PathLike | str): path to the folder to search for images

        Returns:
            dict[str, list[str]]: All images matching all the regex patterns
        """
        # Get all images in the folder
        folder = Path(folder)
        files_in_folder = [f.name for f in folder.iterdir() if f.is_file()]

        # Find all images matching the regex patterns
        found_images: dict[str, list[Path | str]] = \
            {key: [] for key in self._regex_patterns}
        for file_name in files_in_folder:
            for key, pattern in self._regex_patterns.items():
                if re.match(pattern, file_name):
                    found_images[key].append(folder / file_name)
                    break

        return found_images

    def _validate_images(
        self, images: dict[str, list[Path | str]], folder: os.PathLike | str,
        verbose: bool = False
    ) -> int:
        """ Validate if the images found represent a valid triplet sequence.

        For an sequence to be valid, we must have at least one triplet found,
        and all the triplets must include all the required images.

        Either all triplets must have the Background mask, or none of them.

        If verbose is True, it will print the reason why the sequence is not
        valid.

        Args:
            images (dict[str, list[str]]):
                All the images found in the triplet sequence for each type
            folder (os.PathLike | str):
                The folder of the triplet sequence.
            verbose (bool):
                To display or not the reason why the triplet sequence is not
                valid. Defaults to False.

        Returns:
            int: If valid, returns the number of triplets found, otherwise 0.
        """
        # Check if all the required images are found
        if any(len(images[x]) == 0 for x in self.MANDATORIES):
            if verbose:
                print(f'Images not found in forlder "{folder}": ')
                for key in self.MANDATORIES:
                    if len(images[key]) == 0:
                        print(f'- {key[:-5]:<10} with pattern '
                              f'"{self._regex_patterns[key]}"')
            return 0

        # Check if all lists have the same length
        frame_count = len(next(iter(images.values())))
        if not all(len(images[x]) == frame_count for x in self.MANDATORIES):
            if verbose:
                print('Not all channels have the same number of frames.')
                for key in self.MANDATORIES:
                    print(f'- {key[:-5]:<10}: {len(images[key])} frames')
            return 0

        # Check optional values
        if not all(
                    len(images[x]) == 0 or len(images[x]) == frame_count
                    for x in self.OPTIONALS
                ):
            if verbose:
                print('Not all triplets have the same number of optional '
                      'images.')
                for key in self.OPTIONALS:
                    print(f'- {key[:-5]:<10}: {len(images[key])} frames')
            return 0

        return frame_count


class TripletScanner:
    """
    Class to can for all the triplet sequences that can be found in a folder
    and its subfolders.

    The folders are checked recursively, but if one contains an sequence, its
    subfolders are not checked.

    Triplet sequernces are loaded using the default TripletSequenceLoader class
    or the one passed as a parameter to the constructor.
    """

    def __init__(self, loader: TripletSequenceLoader | None = None):
        """Constructor

        Args:
            loader (TripletSequenceLoader | None, optional):
                The loader to use to load the sequences. If None, a default
                TripletSequenceLoader is used with the default regex patterns.
        """
        if loader is None:
            loader = TripletSequenceLoader()
        self.loader = loader
        self._n_sort = NumericalSort()

    def scan(self, folder: os.PathLike | str) -> QtfSeries:
        """ Scan the folder and its subfolders for valid triplet sequences,
        load them with the loader and return them as a list

        Args:
            folder (os.PathLike | str): Path to the parent folder to search in
        Returns:
            QtfSeries: Series containing all the triplet sequences found in
                the folder and its subfolders.
        """
        folder_to_check = [Path(folder)]
        if not folder_to_check[0].is_dir():
            raise ValueError(
                f"The provided path '{folder}' is not a directory.")

        sequences = []
        while len(folder_to_check) > 0:
            # Pop the last folder to check, and if no sequences is found
            # directly in it, add its subfolders to the check list
            current_folder = folder_to_check.pop(0)
            seq = self.loader.check_and_load(current_folder, folder)
            if seq is not None:
                sequences.append(seq)
            else:
                subfolders = [
                    item for item in current_folder.iterdir() if item.is_dir()
                ]
                # Add subfolders to the list for further checking
                subfolders.sort(key=self._n_sort.key)
                folder_to_check.extend(subfolders)

        return QtfSeries(sequences)
