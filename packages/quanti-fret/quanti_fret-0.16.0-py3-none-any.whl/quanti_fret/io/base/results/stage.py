from quanti_fret.core import QtfException, QtfSeries, SeriesIterator
from quanti_fret.io.base.results.json import JsonResultsManager
from quanti_fret.io.base.validate import Validator

import abc
import math
from pathlib import Path
import shutil
from typing import Any

import pandas as pd


class StageResults(abc.ABC):
    """ Handle the results saving and loading of a specific stage.

    It is expected to be inherited. The child class must provide:
        * a `validators` parameter to create a proper JsonResultsManager.

    To specialize the class even more, the user is encourrage to override:
        * `_get_json_settings`
        * `_get_json_results`
        * `save_triplet`
        * `get_stage_extras`
        * `has_stage_extras`
        * `get_triplet_results`
        * `get_triplet_extras`
        * `has_triplet_extras`
    """

    def __init__(
        self, output_dir: Path, validators: dict[str, dict[str, Validator]],
        json_name: str = 'results.json'
    ) -> None:
        """_summary_

        Args:
            output_dir (Path): Path to the output directory
            validators (dict[str, dict[str, Validator]]): Validators to
                validate, get and save json data
            json_name (str): To set the name of the json file to create
        """
        self._output_dir = output_dir
        self._dumps_dir = output_dir / 'dumps'
        self._indices_file = self._output_dir / 'indices.csv'
        self._clean_all_output = True
        self._check_dir()
        json_path = self._output_dir / json_name
        self._validators = validators
        self._json_res_manager = JsonResultsManager(json_path, validators)

    @property
    def output_dir(self) -> Path:
        """ Directory where are stored the results
        """
        return self._output_dir

    def set_clean_all_output(self, val: bool) -> None:
        """ Set the clean all output value.

        If set to True, all the output folder will be deleted when calling
        `clean_output`. If set to False, only the dump folder will be deleted.

        Args:
            val (bool): Value to set
        """
        self._clean_all_output = val

    def clean_output(self) -> None:
        """ Clean the output dir by deleting the folder and creating it
        again
        """
        if self._clean_all_output:
            shutil.rmtree(self._output_dir)
        else:
            shutil.rmtree(self._dumps_dir)
        self._check_dir()

    def save_stage(
        self, settings: tuple[Any, ...], results: tuple[Any, ...]
    ) -> None:
        """ Save the stage's settings and results.

        Values saved and their order are described in each StageResults
        implementation class.

        For the settings, we expect them to be the same as the ones returned by
        StageParams.

        For the results we expect the first elements to be the results to put
        in the Json files (also described in the stage's self._validators), in
        the same order. The final optional element of the tuple can be a
        dictionary containing all the extras values to save to the folder with
        each keys optional.

        Args:
            settings (tuple[Any, ...]): Settings to save
            results (tuple[Any, ...]): Results to save
        """
        # Create output dir
        self._check_dir()
        # Generate and save json
        json_settings = self._get_json_settings(settings)
        json_results = self._get_json_results(results)
        json_data = self._generate_json(json_settings, json_results)
        self._json_res_manager.save(json_data)
        # Save extra data
        self._save_extra(settings, results)

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

        By default, is not implemented

        Args:
            sit (SeriesIterator): The series iterator to get the triplet id.
                Make sure that the sit is in the proper state.
            results (tuple[Any, ...]): Results to save

        Raise:
            QtfException: The function is not implemented
        """
        raise QtfException('`save_index` was not implemented for this stage')

    def get_stage_settings(self) -> tuple[Any, ...] | None:
        """ Get the settings of the given stage

        Values returned are the one from the Json files, in the same order.
        They are also the one described in the stage's self._validators and
        class comments.

        Returns:
            tuple[Any, ...]] | None: (settings) or None if no settings found
        """
        # Check dir
        self._check_dir()
        if not self._output_dir.is_dir():
            return None

        # Load data
        data = self._json_res_manager.get()
        if data is None:
            return None
        if 'settings' in data:
            return tuple(data['settings'].values())
        else:
            return ()

    def get_stage_results(self) -> tuple[Any, ...] | None:
        """ Get the results of the given stage

        Values returned are the one from the Json files, in the same order.
        They are also the one described in the stage's self._validators and
        class comments.

        Returns:
            tuple[Any, ...]] | None: (results) or None if no results found
        """
        # Check dir
        self._check_dir()
        if not self._output_dir.is_dir():
            return None

        # Load data
        data = self._json_res_manager.get()
        if data is None:
            return None
        if 'results' in data:
            return tuple(data['results'].values())
        else:
            return ()

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

        By default, is not implemented

        Args:
            key (str | list[str] | None, optional): If not None, load only the
                element associated with the given key (or with the given keys
                if the dictionary is nested. Default is None.
            check_only (bool, optional): If True, will only check if the extras
                results exists. Default is False

        Raise:
            QtfException: The function is not implemented
            QtfException: The keys are invalid

        Returns:
            dict[str, Any]: Dictionary containing the extra results
        """
        err = '`get_stage_extra` was not implemented for this stage'
        raise QtfException(err)

    def get_triplet_ids(self) -> list[tuple[int, int, int, Path]]:
        """ Get the triplet ids

        Returns:
            list[tuple[int, int, int, Path]]: list of ids. An element if the
                list is ('Id', 'SeqId', 'TripletId', 'Path')
        """
        path = self._indices_file
        if not path.is_file():
            return []

        indices = pd.read_csv(path)
        return [tuple(row) for row in indices.values.tolist()]

    def get_triplet_results(self, id: int) -> tuple[Any, ...] | None:
        """ Get the results of the computation of a given triplet

        Values saved and their order are described in each StageResults
        implementation class.

        We expect the results to be in the same order than the one returned by
        the function computing one triplet at a time, excluding the optional
        extra results.

        By default, is not implemented

        Args:
            id (int): Id of the triplet to retrieve

        Raise:
            QtfException: The function is not implemented

        Returns:
            tuple[Any, ...]: results values or None if no results found
        """
        err = '`get_triplet_results` was not implemented for this stage'
        raise QtfException(err)

    def get_triplet_results_path(self, id: int) -> Path:
        """ Get the folder containing the results of the computation of a given
        triplet

        By default, is not implemented

        Args:
            id (int): Id of the triplet to retrieve

        Raise:
            QtfException: The function is not implemented
            QtfException: The ID is incorrect

        Returns:
            Path: The path to the folder containing the result
        """
        err = '`get_triplet_results_path` was not implemented for this stage'
        raise QtfException(err)

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

        By default, is not implemented

        Args:
            id (int): Id of the triplet to retrieve
            key (str | list[str] | None, optional): If not None, load only the
                element associated with the given key (or with the given keys
                if the dictionary is nested. Default is None.
            check_only (bool, optional): If True, will only check if the extras
                results exists. Default is False

        Raise:
            QtfException: The function is not implemented
            QtfException: The keys are invalid

        Returns:
            dict[str, Any]: Dictionary containing the extra results
        """
        err = '`get_triplet_extras` was not implemented for this stage'
        raise QtfException(err)

    def _get_json_settings(self, settings: tuple[Any, ...]) -> tuple[Any, ...]:
        """ Return all the settings that are supposed to be in the json file.

        By default, turn every `QtfSeries` elements to an integer representing
        the size of the series. Override this to change the behavior.

        Args:
            settings (tuple[Any, ...]): Settings to save

        Results:
            tuple[Any, ...]: Settings to put in the JSON
        """
        return tuple(
            [s.size if type(s) is QtfSeries else s for s in settings]
        )

    def _get_json_results(self, results: tuple[Any, ...]) -> tuple[Any, ...]:
        """ Return all the results that are supposed to be in the json file.

        Overwritte this if you want to filter out results

        Args:
            results (tuple[Any, ...]): results to save

        Results:
            tuple[Any, ...]: Results to put in the JSON
        """
        return results

    def _save_extra(
        self, settings: tuple[Any, ...], results: tuple[Any, ...]
    ) -> None:
        """ Write every results that are not in the JSON.

        Overwritte this if you want to save something outside the JSON

        Args:
            settings (tuple[Any, ...]): Settings to save
            results (tuple[Any, ...]): All the results to save, included the
                one already saved in the JSON.
        """
        pass

    def _check_dir(self):
        """ Check if the directory is Valid

        Raises:
            QtfException: Check failed
        """
        if not isinstance(self._output_dir, Path):
            err = f'Output dir "{self._output_dir}" is not an instance of Path'
            raise QtfException(err)
        if self._output_dir.exists() and not self._output_dir.is_dir():
            err = f'Output dir {self._output_dir} exists and is not a dir'
            raise QtfException(err)
        self._output_dir.mkdir(exist_ok=True)
        self._dumps_dir.mkdir(exist_ok=True)

    def _generate_json(
        self, settings: tuple[Any, ...], results: tuple[Any, ...]
    ) -> dict[str, dict[str, Any]]:
        """ Generate the JSON file to dump.

        About the parameters: Settings and results are supposed to have the
        same elements in the same order than the validators keys

        Args:
            settings (tuple[Any, ...]): Settings to save
            results (tuple[Any, ...]): Results to save
        """
        ret: dict[str, dict[str, Any]] = {}
        if len(settings) > 0:
            ret['settings'] = self._generate_json_section('settings', settings)
        if len(results) > 0:
            ret['results'] = self._generate_json_section('results', results)
        return ret

    def _generate_json_section(
        self, section: str, values: tuple[Any, ...]
    ) -> dict[str, Any]:
        """ Generate the JSON file to dump.

        About the parameters: value is supposed to have the same elements in
        the same order than the validators[section] keys

        Args:
            values (tuple[Any, ...]): values used to put in the section
        """
        ret: dict[str, Validator] = {}
        validator_keys = list(self._validators[section].keys())
        if len(values) != len(validator_keys):
            err = f'Incorrect number of values for section {values}. '
            err += f'Got {len(values)}, expected {len(validator_keys)} ('
            err += f'{validator_keys})'
            raise QtfException(err)
        for i in range(len(values)):
            ret[validator_keys[i]] = values[i]
        return ret

    def _save_triplet_id(self, sit: SeriesIterator) -> None:
        """ Save the triplet id into a file containing the path of the
        sequence associated with the triplet.

        Either create the file, or append the triplet to the data.

        Args:
            sit (SeriesIterator): The series iterator to get the triplet id.
                Make sure that the tit is in the proper state.
        """
        path = self._indices_file
        if path.is_file() and sit.id[0] != 1:
            indices = pd.read_csv(path)
        else:
            indices = pd.DataFrame(
                columns=['Id', 'SeqId', 'TripletId', 'Path']
            )
        row: list[int | str] = [
            sit.id[0],
            sit.id[1],
            sit.id[2],
            str(sit.current_sequence.folder)
        ]
        indices.loc[len(indices)] = row

        indices.to_csv(path, index=False)

    def _get_triplet_folder_name(self, id: int, max_id: int) -> str:
        """ get the folder name associated with the triplet's id

        Args:
            id (int): Triplet's id
            max_id (int): Maximul of the Triplet's id

        Returns:
            str: the name of the folder
        """
        nb_digits = math.floor(math.log10(abs(max_id))) + 1
        return f'{id:0{nb_digits}}'

    def _check_extra_key(
        self,
        key: str | list[str] | None,
        accepted: list[list[str]],
        check_type: str
    ):
        """ Check if the required extra key is valid

        Keys can either be a single string, or a list of string for nested
        dictionaries.

        Accepted keys are supposed to be a list whose last element are the leaf
        of the keys in the dictionarries, and first element their parents.
        Here is an example:
            * Dictionary is: {
                "key1": ...
                "key2": {
                    "key21": ...
                    "key22": {
                        "key221": ...
                        "key222": ...
                    }
                }
            }
            * accepted is [
                ["key1"],
                ["key2", "key21"],
                ["key2", "key22", "key221"],
                ["key2", "key22", "key222"],
            ]

        Args:
            key (str | list[str] | None): key to check
            accepted (list[str]): accepted keys
            check_type (str): Type of the check in ['stage', 'triplet']. Used
                for error message.

        Raised:
            QtfException: The key is invalid
        """
        if key is None:
            return

        if type(key) is str:
            key_list = [key]
        else:
            assert type(key) is list
            key_list = key

        if key_list not in accepted:
            err = f'Invalid key(s) for {check_type} extras: {key}'
            raise QtfException(err)
