from quanti_fret.core import QtfException
from quanti_fret.io.base.validate import Validator

import json
from pathlib import Path
from typing import Any


class JsonResultsManager:
    """ Handle the checking, loading and saving of Results data in Json files

    It is expected to be provided with a `validators` parameter that is a
    dictionary whose keys are describing the layout of the json to save, and
    whose values are Validator that handle the checking, loading and saving
    of specific types.
    """

    def __init__(
        self, json_file: Path,
        validators: dict[str, dict[str, Validator]]
    ) -> None:
        """ Constructor

        Args:
            json_file (Path): Path to the json file
            validators (dict[str, dict[str, Validator]]): Validators to
                validate, get and save all data
        """
        self._json_file = json_file
        self._validators = validators
        self._check_json_file()

    def save(self, data: dict[str, dict[str, Any]]) -> None:
        """ Save the data to the json file

        Check the data, convert the it into a dictionary serializable in Json,
        and save it to the Json file.

        Args:
            data (dict[str, dict[str, Any]]): data to save
        """
        self._check_json_file()
        self._check_keys(data, 'save')
        json_data: dict[str, dict[str, Any]] = {}
        for section, keys in self._validators.items():
            json_data[section] = {}
            for key, validator in keys.items():
                val = data[section][key]
                json_val = validator.convert_to_json(val)
                json_data[section][key] = json_val
        with open(self._json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def get(self) -> dict[str, dict[str, Any]] | None:
        """ Load the data to the json file

        Check the data, convert the it into quanti_fret module types and,
        and returns it.

        Returns:
            dict[str, dict[str, Any]]: data loaded
        """
        self._check_json_file()
        if not self._json_file.is_file():
            return None
        with open(self._json_file, 'r') as f:
            json_data = json.load(f)
        self._check_keys(json_data, 'load')
        data: dict[str, dict[str, Any]] = {}
        for section, keys in self._validators.items():
            data[section] = {}
            for key, validator in keys.items():
                json_val = json_data[section][key]
                val = validator.convert_from_json(json_val)
                data[section][key] = val
        return data

    def _check_json_file(self) -> None:
        """ Check is the json file has good type, and if it exists that is it
        a proper file.

        Raises:
            QtfException: Check failed
        """
        if not isinstance(self._json_file, Path):
            err = f'json file "{self._json_file}" is not an instance of Path'
            raise QtfException(err)
        if self._json_file.exists() and not self._json_file.is_file():
            err = f'json path {self._json_file} exists and is not a file'
            raise QtfException(err)

    def _check_keys(self, data: dict[str, dict[str, Any]], mode: str) -> None:
        """ Check if the given dictionary contains all sections and keys that
        are expected by the self._validators

        Args:
            data (dict[str, dict[str, Any]]): Dictionary to check
            mode (str): Mode for error display. Either 'save' or 'load'

        Raises:
            QtfException: Check failed
        """
        for section, keys in self._validators.items():
            if section not in data:
                err = f'Missing section "{section}" on data to {mode}'
                raise QtfException(err)
            for key, value in keys.items():
                if key not in data[section]:
                    err = f'Missing key "[{section}][{key}]" on data to {mode}'
                    raise QtfException(err)
            if len(keys) != len(data[section]):
                err = f'Data contains extra keys on section {section}'
                raise QtfException(err)
        if len(self._validators) != len(data):
            err = 'Data contains extra sections'
            raise QtfException(err)
