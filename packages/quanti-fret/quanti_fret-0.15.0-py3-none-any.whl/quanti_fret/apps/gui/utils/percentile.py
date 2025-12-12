from qtpy.QtWidgets import QDoubleSpinBox


class PercentileSpinBox(QDoubleSpinBox):
    """ SpinBox for percentile
    """
    def __init__(self, *args, **kwargs):
        """ Constructor
        """
        super().__init__(*args, **kwargs)
        self.setRange(0.0, 100.0)
        self.setSingleStep(1.)
        self.setSuffix('%')
