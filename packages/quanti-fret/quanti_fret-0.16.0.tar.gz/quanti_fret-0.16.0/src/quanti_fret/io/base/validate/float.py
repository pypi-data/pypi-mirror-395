from quanti_fret.core import QtfException
from quanti_fret.io.base.validate.validators import Validator

from typing import Any

import numpy as np


class FloatValidator(Validator):
    """ Simple float validator

    It expect the following:
        * Types:
            * Ini is an float
            * Json is an float or an int
    """

    def __init__(
        self, min: float | None = None, max: float | None = None
    ) -> None:
        """ Constructor

        Args:
            min (float | None): If not None, minimum value accepted
            max (float | None): If not None, maximum value accepted
        """
        super().__init__(float, [float, int])
        self._min = min
        self._max = max

    def _validate(self, format: str, value: Any) -> None:
        """ Validate that the value passed is valid.

        I set in the constructor, Value must be between self._min and self._max

        Args:
            format (str): Whether the value comes from 'ini' or 'json' file.
            value (str): Value loaded and cast

        Raises:
            QtfException: If the value is not valid
        """
        # value is float
        if self._min is not None:
            if value < self._min:
                error = f'"{value}" is below the min "{self._min}"'
                raise QtfException(error)
        if self._max is not None:
            if value > self._max:
                error = f'"{value}" is above the max "{self._max}"'
                raise QtfException(error)

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
        if type(value) is int or \
           isinstance(value, np.floating) or \
           isinstance(value, np.integer):
            value = float(value)
        if type(value) is not float:
            raise QtfException(f'{value} is not a float')

        self._validate(format, value)

        if format == 'ini':
            return str(value)
        else:
            return value
