from quanti_fret.io.base.results import StageResults
from quanti_fret.io.base.validate import (
    BackgroundEngineValidator, BooleanValidator, FloatValidator, IntValidator,
    StringValidator, Validator
)
from quanti_fret.core import QtfException, SeriesIterator

from pathlib import Path
import pickle
from typing import Any

import pandas as pd
import numpy as np
import tifffile


class FretResults(StageResults):
    """ Manage the saving of the settings and results of the Fret Stage

    The value expected as input are:
        * settings:
            * series name (str)
            * series used (QtfSeries): transformed in size of the series (int)
            * alpha_bt (float)
            * delta_de (float)
            * beta_x (float)
            * gamma_m (float)
            * background for the 3 channels (tuple[float, float, float])
            * sigma_s (float)
            * target_s (float)
            * sigma_gauss (float)
            * weights_threshold (float)
            * Save analysis details (bool)
            * Sampling (int)
        * results: None
        * extras (dict):
            * e_boxplot (Figure)
            * s_boxplot (Figure)
            * hist2d (Figure)
            * median_samples (np.ndarray)
        * triplets results:
            * E (numpy): Fret
            * Ew (numpy): Fret Filtered
            * S (numpy): Stochiometry
        * triplets extra (dict):
            * hist2d_s_vs_e (Figure)
            * hist2d_e_vs_iaa (Figure)
            * hist2d_s_vs_iaa (Figure)
            * sampled (np.ndarray)
    """

    VALIDATORS: dict[str, dict[str, Validator]] = {
        'settings': {
            'series': StringValidator(),
            'nb_seq': IntValidator(min=0),
            'alpha_bt': FloatValidator(),
            'delta_de': FloatValidator(),
            'beta_x': FloatValidator(),
            'gamma_m': FloatValidator(),
            'background': BackgroundEngineValidator(),
            'sigma_s': FloatValidator(),
            'target_s': FloatValidator(),
            'sigma_gauss': FloatValidator(),
            'weights_threshold': FloatValidator(),
            'save_analysis_details': BooleanValidator(),
            'analysis_sampling': IntValidator(min=1, max=10000)
        },
    }

    def __init__(self, output_dir: Path):
        """Constructor

        Args:
            output_dir (Path): Path to the output directory
        """
        super().__init__(output_dir, self.VALIDATORS, 'settings.json')

    def _get_json_results(self, results: tuple[Any, ...]) -> tuple[Any, ...]:
        """ Return all the results that are supposed to be in the json file.

        No results on this stage

        Args:
            results (tuple[Any, ...]): results to save

        Results:
            tuple[Any, ...]: Results to put in the JSON
        """
        return ()

    def save_triplet(
        self, sit: SeriesIterator, results: tuple[Any, ...]
    ) -> None:
        """ Save the results of the computation of a single triplet.

        Values saved and their order are described in each StageResults
        implementation class.

        We expect the results to be in the same order than the one returned by
        the function computing one triplet at a time.

        The final optional element of the tuple can be a dictionary containing
        all the extras values to save to the folder. Each keys can be optional.

        Args:
            sit (SeriesIterator): The series iterator to get the triplet id.
                Make sure that the sit is in the proper state.
            results (tuple[Any, ...]): Results to save
        """
        def save_fig_if_key(key: str, filename: str) -> None:
            if key in extras:
                # png
                path = results_dir / f'{filename}.png'
                extras[key].savefig(path)
                # pickle
                dump_path = dump_dir / f'{filename}.pkl'
                with open(dump_path, 'wb') as f:
                    pickle.dump(extras[key], f)

        folder_name = self._get_triplet_folder_name(sit.current, sit.size)
        results_dir = self._output_dir / 'Results' / folder_name
        results_dir.mkdir(parents=True, exist_ok=True)
        dump_dir = self._dumps_dir / 'Results' / folder_name
        dump_dir.mkdir(parents=True, exist_ok=True)

        E, Ew, S, extras = results
        self._write_tiff(E, results_dir / 'E.tif')
        self._write_tiff(S, results_dir / 'S.tif')
        self._write_tiff(Ew, results_dir / 'E_filtered.tif')

        save_fig_if_key('hist2d_s_vs_e', 'S_vs_E')
        save_fig_if_key('hist2d_e_vs_iaa', 'E_vs_IAA')
        save_fig_if_key('hist2d_s_vs_iaa', 'S_vs_IAA')

        if 'sampled' in extras:
            df = pd.DataFrame(extras['sampled'].T,
                              columns=['DD', 'DA', 'AA', 'E', 'Ew', 'S'])
            path = results_dir / 'sampled.csv'
            df.to_csv(path, index=False, index_label='Index')
            path = dump_dir / 'sampled.npy'
            extras['sampled'].dump(path)

        self._save_triplet_id(sit)

    def get_stage_extras(
        self, key: str | list[str] | None = None, check_only: bool = False
    ) -> dict[str, Any]:
        """ Get the extra results of the given stage

        If exists, the returned value is the same dictionary as the one passed
        as last element of the result parameter to `save_stage`.

        You can load only one extra value by specifying the key to load (or the
        list of keys for nested disctionaries)

        if `check_only` is set to True, values of the dictionary will be
        booleans telling the user if the extra value exists or not.

        See class comments for more information on the dictionary layout

        Args:
            key (str | list[str] | None, optional): If not None, load only the
                element associated with the given key (or with the given keys
                if the dictionary is nested. Default is None.
            check_only (bool, optional): If True, will only check if the extras
                results exists. Default is False

        Raise:
            QtfException: The keys are invalid

        Returns:
            dict[str, Any]: Dictionary containing the extra results
        """
        def load_key(target_key: str, filename: str, type: str) -> None:
            """ Load the given target key to the extras dictionary if needed

            Args:
                target_key (str): Key to check if it need loading
                filename (str): file associated with the key
                type (str): type of the file to load (in ['pickle', 'numpy'])
            """
            if key is None or key == target_key:
                path = self._dumps_dir / filename
                if path.is_file():
                    if check_only:
                        extras[target_key] = True
                    else:
                        if type == 'pickle':
                            with open(path, 'rb') as f:
                                extras[target_key] = pickle.load(f)
                        elif type == 'numpy':
                            extras[target_key] = np.load(
                                path, allow_pickle=True
                            )
                        else:
                            raise QtfException(f'Unknown type {type}')

        # Check inputs
        accepted = [
            ['e_boxplot'], ['s_boxplot'], ['hist_2d'], ['median_samples'],
        ]
        self._check_extra_key(key, accepted, 'stage')

        # Create the extras dict
        if check_only:
            default_value = False
        else:
            default_value = None
        if type(key) is list:
            key_str = key[0]
        elif key is None:
            key_str = ''
        else:
            assert type(key) is str
            key_str = key
        if key is None:
            extras = {
                'e_boxplot': default_value,
                's_boxplot': default_value,
                'hist_2d': default_value,
                'median_sampled': default_value
            }
        else:
            assert type(key_str) is str
            extras = {
                key_str: default_value
            }

        # Load all keys
        load_key('e_boxplot', 'E_boxplot.pkl', 'pickle')
        load_key('s_boxplot', 'S_boxplot.pkl', 'pickle')
        load_key('hist_2d', 'S_vs_E.pkl', 'pickle')
        load_key('median_sampled', 'median_sampled.npy', 'numpy')

        return extras

    def get_triplet_results(self, id: int) -> tuple[Any, ...] | None:
        """ Get the results of the computation of a given triplet

        Values saved and their order are described in each StageResults
        implementation class.

        We expect the results to be in the same order than the one returned by
        the function computing one triplet at a time, excluding the optional
        extra results.

        Args:
            id (int): Id of the triplet to retrieve

        Raise:
            QtfException: ID is invalid

        Returns:
            tuple[Any, ...]: results values or None if no results found
        """
        # Find triplet folder
        triplet_dir = self.get_triplet_results_path(id)

        # Check if all files are presents
        e_file = triplet_dir / 'E.tif'
        if not e_file.is_file():
            raise QtfException(f'{e_file} cannot be opened')
        e_filtered_file = triplet_dir / 'E_filtered.tif'
        if not e_filtered_file.is_file():
            raise QtfException(f'{e_filtered_file} cannot be opened')
        s_file = triplet_dir / 'S.tif'
        if not s_file.is_file():
            raise QtfException(f'{s_file} cannot be opened')

        # Open all files
        E = tifffile.imread(e_file)
        Ew = tifffile.imread(e_filtered_file)
        S = tifffile.imread(s_file)

        return E, Ew, S

    def get_triplet_results_path(self, id: int) -> Path:
        """ Get the folder containing the results of the computation of a given
        triplet

        Args:
            id (int): Id of the triplet to retrieve

        Raise:
            QtfException: The ID is incorrect

        Returns:
            Path: The path to the folder containing the result
        """
        # Find triplet folder
        results_dir = self._output_dir / 'Results'
        ids = self.get_triplet_ids()
        id_str = self._get_triplet_folder_name(id, ids[-1][0])
        triplet_dir = results_dir / id_str
        if not triplet_dir.is_dir():
            raise QtfException(f'{triplet_dir} is not a valid folder')
        return triplet_dir

    def get_triplet_extras(
        self,
        id: int,
        key: str | list[str] | None = None,
        check_only: bool = False
    ) -> dict[str, Any]:
        """ Get the extra results of a computation of a given triplet

        If exists, the returned value is the same dictionary as the one passed
        as last element of the result parameter og `save_triplet`.

        You can load only one extra value by specifying the key to load (or the
        list of keys for nested disctionaries)

        if `check_only` is set to True, values of the dictionary will be
        booleans telling the user if the extra value exists or not.

        See class comments for more information on the dictionary layout

        Args:
            id (int): Id of the triplet to retrieve
            key (str | list[str] | None, optional): If not None, load only the
                element associated with the given key (or with the given keys
                if the dictionary is nested. Default is None.
            check_only (bool, optional): If True, will only check if the extras
                results exists. Default is False

        Raise:
            QtfException: The id is invalid
            QtfException: The keys are invalid

        Returns:
            dict[str, Any]: Dictionary containing the extra results
        """
        def load_key(target_key: str, filename: str, type: str) -> None:
            """ Load the given target key to the extras dictionary if needed

            Args:
                target_key (str): Key to check if it need loading
                filename (str): file associated with the key
                type (str): type of the file to load (in ['pickle', 'numpy'])
            """
            if key is None or key == target_key:
                path = triplet_dir / filename
                if path.is_file():
                    if check_only:
                        extras[target_key] = True
                    else:
                        if type == 'pickle':
                            with open(path, 'rb') as f:
                                extras[target_key] = pickle.load(f)
                        elif type == 'numpy':
                            extras[target_key] = np.load(
                                path, allow_pickle=True
                            )
                        else:
                            raise QtfException(f'Unknown type {type}')

        # Check inputs
        accepted = [
            ['hist2d_s_vs_e'], ['hist2d_e_vs_iaa'], ['hist2d_s_vs_iaa'],
            ['sampled'],
        ]
        self._check_extra_key(key, accepted, 'triplet')

        # Create the extras dict
        if check_only:
            default_value = False
        else:
            default_value = None
        if type(key) is list:
            key_str = key[0]
        elif key is None:
            key_str = ''
        else:
            assert type(key) is str
            key_str = key
        if key is None:
            extras = {
                'hist2d_s_vs_e': default_value,
                'hist2d_e_vs_iaa': default_value,
                'hist2d_s_vs_iaa': default_value,
                'sampled': default_value
            }
        else:
            assert type(key_str) is str
            extras = {
                key_str: default_value
            }

        # Find results dir
        results_dir = self._dumps_dir / 'Results'
        ids = self.get_triplet_ids()
        id_str = self._get_triplet_folder_name(id, ids[-1][0])
        triplet_dir = results_dir / id_str
        if not triplet_dir.is_dir():
            raise QtfException(f'{triplet_dir} is not a valid folder')

        # Load all keys
        load_key('hist2d_s_vs_e', 'S_vs_E.pkl', 'pickle')
        load_key('hist2d_e_vs_iaa', 'E_vs_IAA.pkl', 'pickle')
        load_key('hist2d_s_vs_iaa', 'S_vs_IAA.pkl', 'pickle')
        load_key('sampled', 'sampled.npy', 'numpy')

        return extras

    def _write_tiff(self, img: np.ndarray, path: Path):
        data_tif = np.copy(img)
        mask = np.logical_or(data_tif < 0, data_tif > 100)
        data_tif[mask] = np.nan
        tifffile.imwrite(path, data_tif.astype(np.float32))

    def _save_extra(
        self, settings: tuple[Any, ...], results: tuple[Any, ...]
    ) -> None:
        """ Write every results that are not in the JSON.

        Save the figures and the CSVs

        Args:
            settings (tuple[Any, ...]): Settings to save
            results (tuple[Any, ...]): All the results to save, included the
                one already saved in the JSON.
        """
        def save_fig_if_key(key: str, filename: str) -> None:
            """ Save the figure associated with the given key if it exists

            Args:
                key (str): Key to save
                filename (str): Destination file
            """
            if key in extras:
                # Png
                path = self._output_dir / f'{filename}.png'
                extras[key].savefig(path)
                # Pickle
                dump_path = self._dumps_dir / f'{filename}.pkl'
                with open(dump_path, 'wb') as f:
                    pickle.dump(extras[key], f)

        # Check input
        extras = results[-1]
        if extras is None:
            return
        if type(extras) is not dict:
            raise QtfException('Extra results must be a dict')

        # Save all figures
        save_fig_if_key('e_boxplot', 'E_boxplot')
        save_fig_if_key('s_boxplot', 'S_boxplot')
        save_fig_if_key('hist_2d', 'S_vs_E')

        # Save the median sampled
        if 'median_sampled' in extras:
            # CSV
            df = pd.DataFrame(
                extras['median_sampled'],
                columns=['DD', 'DA', 'AA', 'E', 'Ew', 'S']
            )
            path = self._output_dir / 'median_sampled.csv'
            df.to_csv(path, index=True, index_label='Index')
            # Numpy
            dump_path = self._dumps_dir / 'median_sampled.npy'
            extras['median_sampled'].dump(dump_path)
