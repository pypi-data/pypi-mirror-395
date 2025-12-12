from quanti_fret.algo import (
    BackgroundEngine, BackgroundEngineFixed, BackgroundEnginePercentile,
    BackgroundMode, create_background_engine
)

from quanti_fret.core import QtfException
from quanti_fret.io.base.validate.enum import EnumValidator
from quanti_fret.io.base.validate.float import FloatValidator
from quanti_fret.io.base.validate.tuple import TupleValidator
from quanti_fret.io.base.validate.validators import Validator

from typing import Any


class BackgroundEngineValidator(Validator):
    """ Validator for Background Engine values

    For now, this is not compatible for Ini format

    It expect the following:
        * Types:
            * Ini is an str (But will fail validation)
            * Json is a dict
        * The value inside the dict contains a 'mode' key, and all the keys
            associated with the mode
    """

    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(str, dict)
        self._background_mode_validator = EnumValidator(BackgroundMode)
        self._percentile_validator = FloatValidator(min=0., max=100.)
        self._fixed_validator = TupleValidator(FloatValidator(min=0.), size=3)

    def _validate(self, format: str, value: Any) -> None:
        """ Validate that the value passed is valid.

        Only format accepted is 'json'.

        Args:
            format (str): Whether the value comes from 'ini' or 'json' file.
            value (str): Value loaded and cast

        Raises:
            QtfException: If the value is not valid
        """
        if format == "ini":
            err = 'BackgroundEngineResultsValidator is not implemented for ini'
            raise QtfException(err)

        if type(value) is not dict:
            err = f'Invalid Background engine type for {value}. Expected dict'
            raise QtfException(err)

        if 'mode' not in value:
            err = 'Missing key "mode" for the background engine'
            raise QtfException(err)

        self._background_mode_validator.validate_from_json(value['mode'])
        mode = self._background_mode_validator.convert_from_json(value['mode'])
        if mode == BackgroundMode.PERCENTILE:
            if 'percentile' not in value:
                err = 'Missing key "percentile" for the background engine'
                raise QtfException(err)
            self._percentile_validator.validate_from_json(value['percentile'])
        elif mode == BackgroundMode.FIXED:
            if 'value' not in value:
                err = 'Missing key "value" for the background engine'
                raise QtfException(err)
            self._fixed_validator.validate_from_json(value['value'])

    def _convert_from_format(self, format: str, value: Any) -> Any:
        """ Convert the value loaded from the given format into the type
        expected in the quanti_fret module.

        Only format accepted is 'jsons'.

        Args:
            format (str): Whether the value comes from 'ini' or 'json'
            value (Any): Value loaded and cast

        returns:
            Any: value converted in the type expected in the quanti_fret
                module, or None if the value is empty.
        """
        if format == "ini":
            raise QtfException('TupleValidator is not implemented for ini')

        # Automatic converter transforms 'disabled' into ('d', 'i', 's', ...)
        mode = self._background_mode_validator.convert_from_json(value['mode'])
        percentile = -1
        background = None
        if mode == BackgroundMode.PERCENTILE:
            percentile = self._percentile_validator.convert_from_json(
                value['percentile']
            )
        elif mode == BackgroundMode.FIXED:
            background = self._fixed_validator.convert_from_json(
                value['value']
            )
        return create_background_engine(mode, background, percentile)

    def _convert_to_format(self, format: str, value: Any) -> Any:
        """ Convert the value comming from the quanti_fret module into a type
        understood by the targeted format.


        Only format accepted is 'sjons'


        Args:
            format (str): Whether the target is a 'ini' or 'json'
            value (Any): Value to set to the config

        Raises:
            QtfException: If the value is not valid

        returns:
            Any: A representation of the value in a format understood by the
                target file format
        """
        if format == "ini":
            raise QtfException('TupleValidator is not implemented for ini')

        if not isinstance(value, BackgroundEngine):
            err = f'Value {value} is not a Background Engine'
            raise QtfException(err)

        mode = value.mode
        ret = {}
        ret['mode'] = self._background_mode_validator.convert_to_json(mode)
        if isinstance(value, BackgroundEnginePercentile):
            ret['percentile'] = \
                self._percentile_validator.convert_to_json(
                    value._percentile
                )
        elif isinstance(value, BackgroundEngineFixed):
            ret['value'] = self._fixed_validator.convert_to_json(
                value.background
            )

        return ret


class BackgroundResultsValidator(Validator):
    """ Validator for Background Results values

    It will create:
        * A BackgroundEngineFixed if the value is a background tuple
        * A BackgroundEngineDisabled if the value is 'disabled'
    For now, this is not compatible for Ini format

    It expect the following:
        * Types:
            * Ini is an str (But will fail validation)
            * Json is a tuple or a str
        * The value inside the tuple pass the validation of the element
            Validator
    """

    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(str, [tuple, list, str])
        self._tuple_validator = TupleValidator(FloatValidator(min=0), 3)

    def _validate(self, format: str, value: Any) -> None:
        """ Validate that the value passed is valid.

        Only format accepted is 'json'.

        Args:
            format (str): Whether the value comes from 'ini' or 'json' file.
            value (str): Value loaded and cast

        Raises:
            QtfException: If the value is not valid
        """
        if format == "ini":
            err = 'BackgroundEngineResultsValidator is not implemented for ini'
            raise QtfException(err)

        if type(value) is str:
            if value != 'disabled':
                err = f'Unknown Background Results {value}. Expected a tuple' \
                      ' or "disabled".'
                raise QtfException(err)
        elif type(value) is tuple or type(value) is list:
            self._tuple_validator.validate_from_json(value)
        else:
            err = 'Invalid Background Results type'
            raise QtfException(err)

    def _convert_from_format(self, format: str, value: Any) -> Any:
        """ Convert the value loaded from the given format into the type
        expected in the quanti_fret module.

        Only format accepted is 'jsons'.

        Args:
            format (str): Whether the value comes from 'ini' or 'json'
            value (Any): Value loaded and cast

        returns:
            Any: value converted in the type expected in the quanti_fret
                module, or None if the value is empty.
        """
        if format == "ini":
            raise QtfException('TupleValidator is not implemented for ini')

        # Automatic converter transforms 'disabled' into ('d', 'i', 's', ...)
        if len(value) == 8 and type(value[0]) is str:
            return create_background_engine(mode=BackgroundMode.DISABLED)
        else:
            background = self._tuple_validator.convert_from_json(value)
            return create_background_engine(mode=BackgroundMode.FIXED,
                                            background=background)

    def _convert_to_format(self, format: str, value: Any) -> Any:
        """ Convert the value comming from the quanti_fret module into a type
        understood by the targeted format.


        Only format accepted is 'sjons'


        Args:
            format (str): Whether the target is a 'ini' or 'json'
            value (Any): Value to set to the config

        Raises:
            QtfException: If the value is not valid

        returns:
            Any: A representation of the value in a format understood by the
                target file format
        """
        if format == "ini":
            raise QtfException('TupleValidator is not implemented for ini')

        if value is None:
            return 'disabled'

        return self._tuple_validator.convert_to_json(value)
