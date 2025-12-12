from quanti_fret.algo import BackgroundMode

from quanti_fret.io.base import Config
from quanti_fret.io.base.validate import (
    BooleanValidator,
    EnumValidator,
    FloatValidator,
    IntValidator,
    PathValidator,
    StringValidator,
    TupleValidator,
    Validator,
)


class FretConfig(Config):
    """ Config class for Fret
    """
    VALIDATORS: dict[str, dict[str, tuple[Validator, str]]] = {
        'Series': {
            'experiments': (PathValidator('folder'), ''),
        },
        'Output': {
            'output_dir': (PathValidator('folder', allow_non_existing=True,
                                         allow_empty=False), 'fret'),
            'clean_before_run': (BooleanValidator(), 'True'),
        },
        'Calibration': {
            'config_file': (PathValidator('file'), ''),
        },
        'Background': {
            'floating': (BooleanValidator(), 'False'),
            'mode': (EnumValidator(BackgroundMode), '1'),
            'percentile': (FloatValidator(min=0.0, max=100.0), '10'),
            'fixed_background': (TupleValidator(FloatValidator(min=0), size=3),
                                 '0, 0, 0'),
        },
        'Fret': {
            'sigma_s': (FloatValidator(), '0.1'),
            'target_s': (FloatValidator(), '0.5'),
            'sigma_gauss': (FloatValidator(), '1.5'),
            'weights_threshold': (FloatValidator(), '0.6'),
            'save_analysis_details': (BooleanValidator(), 'False'),
            'analysis_sampling': (IntValidator(min=1, max=10000), '100'),
        },
        'Regex': {
            'dd': (StringValidator(), ''),
            'da': (StringValidator(), ''),
            'aa': (StringValidator(), ''),
            'mask_cell': (StringValidator(), ''),
            'mask_bckg': (StringValidator(), ''),
        },
    }

    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(self.VALIDATORS)
