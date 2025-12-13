from quanti_fret.io.base.series_manager import QtfSeriesManager


class QtfCalibrationSeriesManager(QtfSeriesManager):
    """ Manager of the different TripletSequence Series used by the calibration
    phase.
    """
    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(['donors', 'acceptors', 'standards'])
