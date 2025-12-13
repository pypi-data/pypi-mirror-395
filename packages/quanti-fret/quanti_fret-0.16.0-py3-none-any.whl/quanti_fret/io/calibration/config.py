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


class CalibrationConfig(Config):
    """ Config class for calibration
    """
    VALIDATORS: dict[str, dict[str, tuple[Validator, str]]] = {
        'Series': {
            'donors': (PathValidator('folder'), ''),
            'acceptors': (PathValidator('folder'), ''),
            'standards': (PathValidator('folder'), ''),
        },
        'Output': {
            'output_dir': (PathValidator('folder', allow_non_existing=True,
                                         allow_empty=False), 'calibration'),
            'clean_before_run': (BooleanValidator(), 'True'),
        },
        'Background': {
            'floating': (BooleanValidator(), 'False'),
            'mode': (EnumValidator(BackgroundMode), '1'),
            'percentile': (FloatValidator(min=0.0, max=100.0), '10'),
            'fixed_background': (TupleValidator(FloatValidator(min=0), size=3),
                                 '0, 0, 0'),
            'use_donors': (BooleanValidator(), 'False'),
            'use_acceptors': (BooleanValidator(), 'False'),
            'use_standards': (BooleanValidator(), 'True'),
        },
        'BT': {
            'discard_low_percentile': (FloatValidator(min=0.0, max=100.0),
                                       '70'),
            'plot_sequence_details': (BooleanValidator(), 'False'),
        },
        'DE': {
            'discard_low_percentile': (FloatValidator(min=0.0, max=100.0),
                                       '70'),
            'plot_sequence_details': (BooleanValidator(), 'False'),
        },
        'XM': {
            'discard_low_percentile': (FloatValidator(min=0.0, max=100.0),
                                       '20'),
            'discard_high_percentile': (FloatValidator(min=0.0, max=100.0),
                                        '99'),
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
