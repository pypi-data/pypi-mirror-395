from quanti_fret.core import QtfException
from quanti_fret.io.base.validate.validators import Validator

from typing import Any


class StringValidator(Validator):
    """ Simple string validator

    It expect the following:
        * Types:
            * Ini is an string
            * Json is an string
    """

    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(str, str)

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
                target file format. For ini, it is expected to be castable to
                string.
        """
        if type(value) is not str:
            raise QtfException(f'{value} is not a str')

        return value
