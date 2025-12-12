from quanti_fret.core import QtfSeries
from quanti_fret.io.base.results import StageResults
from quanti_fret.io.base.validate import (
    BackgroundEngineValidator, BooleanValidator, FloatValidator, IntValidator,
    StringValidator, TupleValidator, Validator
)

from pathlib import Path
import pickle
from typing import Any

import numpy as np
import pandas as pd


class XMResults(StageResults):
    """ Manage the saving of the settings and results of the XM Stage

    The value expected as input are:
        * settings:
            * series name (str)
            * series used (QtfSeries): transformed in size of the series (int)
            * alpha_bt (float)
            * delta_de (float)
            * background for the 3 channels (tuple[float, float, float])
            * percentile rang (tuple[float, float])
            * Save analysis details (bool)
            * Sampling (int)
        * results:
            * beta_x (float)
            * gamma_m (float)
            * redchi_2 (float)
            * r2 (float)
            * q (float)
        * extras (dict):
            * hist2d_s_vs_e (Figure)
            * hist2d_e_vs_iaa (Figure)
            * hist2d_s_vs_iaa (Figure)
            * e_boxplot (Figure)
            * s_boxplot (Figure)
            * inspection (dict):
                * triplets_per_seq (Figure)
                * s_per_seq (Figure)
                * s_vs_e (Figure)
                * scatter_3d (Figure)
            * median_samples (np.ndarray)
            * sampled_list (list[np.ndarray])
        * triplets results: None
        * triplets extra: None
    """

    VALIDATORS: dict[str, dict[str, Validator]] = {
        'settings': {
            'series': StringValidator(),
            'nb_seq': IntValidator(min=0),
            'alpha_bt': FloatValidator(),
            'delta_de': FloatValidator(),
            'background': BackgroundEngineValidator(),
            'percentile_range': TupleValidator(
                FloatValidator(min=0.0, max=100.0), 2
            ),
            'save_analysis_details': BooleanValidator(),
            'analysis_sampling': IntValidator(min=1, max=10000)
        },
        'results': {
            'beta_x': FloatValidator(),
            'gamma_m': FloatValidator(),
            'redchi_2': FloatValidator(),
            'r2': FloatValidator(),
            'q': FloatValidator(),
        }
    }

    def __init__(self, output_dir: Path):
        """Constructor

        Args:
            output_dir (Path): Path to the output directory
        """
        super().__init__(output_dir, self.VALIDATORS)

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
        def load_pickle_key(
            filename: str, extra_key: str, extra_subkey: str = ''
        ) -> None:
            # Check if extra_key needs to be loaded
            if root_key is not None:
                if extra_key != root_key:
                    return
                elif inspection_key is not None:
                    if extra_subkey != inspection_key:
                        return

            # Load key
            if extra_subkey == '':
                path = self._dumps_dir / f'{filename}.pkl'
            else:
                path = self._dumps_dir / extra_key / f'{filename}.pkl'
            val: Any
            if path.is_file():
                if check_only:
                    val = True
                else:
                    with open(path, 'rb') as f:
                        val = pickle.load(f)
            else:
                val = default_value

            # Set value
            if extra_subkey == '':
                extras[extra_key] = val
            else:
                extras[extra_key][extra_subkey] = val

        if check_only:
            default_value = False
        else:
            default_value = None

        # Check key value
        root_key, inspection_key = self._check_xm_extra_key(key)

        # Load extras figures
        extras: dict[str, Any] = {'inspection': {}}
        load_pickle_key('S_vs_E_for_all_cells', 'hist2d_s_vs_e')
        load_pickle_key('E_vs_IAA_intensity_for_all_cells', 'hist2d_e_vs_iaa')
        load_pickle_key('S_vs_IAA_intensity_for_all_cells', 'hist2d_s_vs_iaa')
        load_pickle_key('E_boxplot', 'e_boxplot')
        load_pickle_key('S_boxplot', 's_boxplot')

        # Load inspection figures
        load_pickle_key('triplets_per_seq', 'inspection', 'triplets_per_seq')
        load_pickle_key('S_per_seq', 'inspection', 's_per_seq')
        load_pickle_key('S_vs_E', 'inspection', 's_vs_e')
        load_pickle_key('scatter_3d', 'inspection', 'scatter_3d')

        # Load Median sampled
        if root_key is None or root_key == 'median_sampled':
            path = self._dumps_dir / 'median_sampled.npy'
            if path.is_file():
                if check_only:
                    extras['median_sampled'] = True
                else:
                    extras['median_sampled'] = np.load(path, allow_pickle=True)
            else:
                extras['median_sampled'] = default_value

        # Load sampled
        if root_key is None or root_key == 'sampled_list':
            nb_sampled = len(self.get_triplet_ids())
            sampled_list = []
            sampled_dir = self._dumps_dir / 'sampled'
            if sampled_dir.is_dir():
                for i in range(1, nb_sampled + 1):
                    path = sampled_dir / f'{i}.npy'
                    if path.is_file():
                        if check_only:
                            sampled_list.append(True)
                        else:
                            sampled_list.append(
                                np.load(path, allow_pickle=True)
                            )
            if len(sampled_list) > 0 and len(sampled_list) == nb_sampled:
                if check_only:
                    extras['sampled_list'] = True
                else:
                    extras['sampled_list'] = sampled_list
            else:
                extras['sampled_list'] = default_value

        return extras

    def _get_json_results(self, results: tuple[Any, ...]) -> tuple[Any, ...]:
        """ Return all the results that are supposed to be in the json file.

        Remove the last settings element that are analysis data

        Args:
            results (tuple[Any, ...]): results to save

        Results:
            tuple[Any, ...]: Results to put in the JSON
        """
        return results[:-1]

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
        analysis_data: dict[str, Any] = results[-1]

        def save_fig_if_key(key: str, filename: str) -> None:
            """ Check if a key exists in the dict, if so, save the figure

            Args:
                key (str): key to check
                filename (str): filename to save (without png extension)
            """
            if key in analysis_data:
                path = self._output_dir / f'{filename}.png'
                analysis_data[key].savefig(path)
                dump_path = self._dumps_dir / f'{filename}.pkl'
                with open(dump_path, 'wb') as f:
                    pickle.dump(analysis_data[key], f)

        # plots
        save_fig_if_key('hist2d_s_vs_e', 'S_vs_E_for_all_cells')
        save_fig_if_key('hist2d_e_vs_iaa', 'E_vs_IAA_intensity_for_all_cells')
        save_fig_if_key('hist2d_s_vs_iaa', 'S_vs_IAA_intensity_for_all_cells')
        save_fig_if_key('e_boxplot', 'E_boxplot')
        save_fig_if_key('s_boxplot', 'S_boxplot')

        # Save indices
        if 'e_boxplot' in analysis_data or 's_boxplot' in analysis_data:
            series: QtfSeries = settings[1]
            sit = series.iterator()
            for _ in sit:
                self._save_triplet_id(sit)

        # Median sampled
        if 'median_sampled' in analysis_data:
            df = pd.DataFrame(analysis_data['median_sampled'],
                              columns=['DD', 'DA', 'AA', 'E', 'S'])
            path = self._output_dir / 'median_sampled.csv'
            df.to_csv(path, index=True, index_label='Index')
            path = self._dumps_dir / 'median_sampled.npy'
            analysis_data['median_sampled'].dump(path)

        # sequences sampled
        if 'sampled_list' in analysis_data:
            sampled_dir = self._output_dir / 'sampled'
            sampled_dir.mkdir(parents=True, exist_ok=True)
            sampled_dumps_dir = self._dumps_dir / 'sampled'
            sampled_dumps_dir.mkdir(parents=True, exist_ok=True)
            index = 1
            for sampled in analysis_data['sampled_list']:
                df = pd.DataFrame(sampled.T,
                                  columns=['DD', 'DA', 'AA', 'E', 'S'])
                path = sampled_dir / f'{index}.csv'
                df.to_csv(path, index=False)
                path = sampled_dumps_dir / f'{index}.npy'
                sampled.dump(path)
                index += 1

        # inspection
        if 'inspection' in analysis_data:
            inspection_dir = self._output_dir / 'inspection'
            inspection_dir.mkdir(parents=True, exist_ok=True)
            inspection_dumps_dir = self._dumps_dir / 'inspection'
            inspection_dumps_dir.mkdir(parents=True, exist_ok=True)

            def save_insp_if_key(key: str, filename: str) -> None:
                if key in analysis_data['inspection']:
                    path = inspection_dir / f'{filename}.png'
                    analysis_data['inspection'][key].savefig(path)
                    dump_path = inspection_dumps_dir / f'{filename}.pkl'
                    with open(dump_path, 'wb') as f:
                        pickle.dump(analysis_data['inspection'][key], f)

            save_insp_if_key('triplets_per_seq', 'triplets_per_seq')
            save_insp_if_key('s_per_seq', 'S_per_seq')
            save_insp_if_key('s_vs_e', 'S_vs_E')
            save_insp_if_key('scatter_3d', 'scatter_3d')

    def _check_xm_extra_key(self, key: str | list[str] | None):
        """ Check if the required extra key is valid

        Args:
            key (str | list[str] | None): key to check

        Raised:
            QtfException: The key is not accepted
        """
        # Accepted keys
        accepted = [
            ['hist2d_s_vs_e'],
            ['hist2d_e_vs_iaa'],
            ['hist2d_s_vs_iaa'],
            ['e_boxplot'],
            ['s_boxplot'],
            ['inspection', 'triplets_per_seq'],
            ['inspection', 's_per_seq'],
            ['inspection', 's_vs_e'],
            ['inspection', 'scatter_3d'],
            ['median_samples'],
            ['sampled_list'],
        ]

        self._check_extra_key(key, accepted, 'stage')

        # Check keys
        root_key = None
        inspection_key = None

        if key is not None:
            if type(key) is str:
                root_key = key
            else:
                assert type(key) is list
                assert len(key) <= 2
                root_key = key[0]
                if len(key) == 2:
                    inspection_key = key[1]

        return root_key, inspection_key
