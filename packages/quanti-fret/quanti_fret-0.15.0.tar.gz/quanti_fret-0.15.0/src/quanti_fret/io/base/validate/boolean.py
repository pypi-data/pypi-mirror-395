from quanti_fret.core import QtfException
from quanti_fret.io.base.validate.validators import Validator

from typing import Any


class BooleanValidator(Validator):
    """ Validator for boolean values

    It expect the following:
        * Types:
            * Ini is an str
            * Json is an bool
        * For 'ini' format, value is 'True' or 'False'
    """

    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(str, bool)

    def _validate(self, format: str, value: Any) -> None:
        """ Validate that the value passed is valid.

        For ini format, value is either 'True' or 'False'

        Args:
            format (str): Whether the value comes from 'ini' or 'json' file.
            value (str): Value loaded and cast

        Raises:
            QtfException: If the value is not valid
        """
        if format == 'ini':
            # value is str
            if value.lower() not in ['true', 'false']:
                error = f'"{value}" should be "true" or "false"'
                raise QtfException(error)

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
        if format == 'ini':
            # value is str
            if value.lower() == 'true':
                return True
            else:
                return False
        else:
            # value is bool
            return value

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
        if not isinstance(value, bool):
            raise QtfException(f'Value {value} is not a bool')
        return value
