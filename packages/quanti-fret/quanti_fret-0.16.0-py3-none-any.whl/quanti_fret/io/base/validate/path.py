from quanti_fret.core import QtfException
from quanti_fret.io.base.validate.validators import Validator

from pathlib import Path
from typing import Any


class PathValidator(Validator):
    """ Validator for path values

    It expect the following:
        * Types:
            * Ini is an str
            * Json is an str
        * The value is one of the following
            * A File or a Directory
            * An existing path
            * A non existing path if allow_non_existing is set to True
            * An empty value if allow_empty is set to True
    """

    def __init__(
        self, type: str, allow_non_existing: bool = False,
        allow_empty: bool = True
    ) -> None:
        """ Constructor

        Args:
            type (str): Weaether the path represents a file of a folder. Must
                be in ['file', 'folder'].
            allow_non_existing (bool): allow or not the path to point to a non
                existing location if not empty.
            allow_empty (bool): allow the value to be empty
        """
        super().__init__(str, str)
        self._type = type
        if type not in ['file', 'folder']:
            raise QtfException(f'Unknown PathValidator type "{type}"')
        self._allow_non_existing = allow_non_existing
        self._allow_empty = allow_empty

    def _validate(self, format: str, value: Any) -> None:
        """ Validate that the value passed is valid.

        Value is expected to be empty, or a valid path (Depending on class
        parameters)

        Args:
            format (str): Whether the value comes from 'ini' or 'json' file.
            value (str): Value loaded and cast

        Raises:
            QtfException: If the value is not valid
        """
        # value is str
        if value == "":
            self._validate_path(None)
        else:
            path = Path(value)
            self._validate_path(path)

    def _convert_from_format(self, format: str, value: Any) -> Any:
        """ Convert the value loaded from the given format into the type
        expected in the quanti_fret module.

        Args:
            format (str): Whether the value comes from 'ini' or 'json'
            value (Any): Value loaded and cast

        returns:
            Any: value converted in the type expected in the quanti_fret
                module, or None if the value is empty.
        """
        # value is str
        if value == "":
            return None
        else:
            return Path(value)

    def _convert_to_format(self, format: str, value: Any) -> Any:
        """ Convert the value comming from the quanti_fret module into a type
        understood by the targeted format.

        Args:
            format (str): Whether the target is a 'ini' or 'json'
            value (Any): Value to set to the config

        Raises:
            QtfException: If the value is not valid

        returns:
            Any: A representation of the value in a format understood by the
                target file format
        """
        # value is str
        if value is None:
            self._validate_path(None)
            return ''
        if not isinstance(value, Path):
            raise QtfException(
                f'Value "{value} has type "{type(value)}" that is not a Path')
        path = Path(value)
        self._validate_path(path)
        return str(path)

    def _validate_path(self, path: Path | None):
        """ Validate that the path is correct

        Args:
            path (Path): The Path to validate

        Raises:
            QtfException: If the path is not valid
        """
        if path is None:
            if self._allow_empty:
                return
            else:
                error = 'Path cannot have an empy value'
                raise QtfException(error)
        if not path.exists():
            if not self._allow_non_existing:
                error = f'"{path}" is not an existing path'
                raise QtfException(error)
        else:
            if self._type == 'folder':
                if not path.is_dir():
                    error = f'"{path}" is not a valid directory'
                    raise QtfException(error)
            if self._type == 'file':
                if not path.is_file():
                    error = f'"{path}" is not a valid file'
                    raise QtfException(error)
