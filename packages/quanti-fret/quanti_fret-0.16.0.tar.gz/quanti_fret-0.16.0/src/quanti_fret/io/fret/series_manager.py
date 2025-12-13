from quanti_fret.io.base.series_manager import QtfSeriesManager


class QtfFretSeriesManager(QtfSeriesManager):
    """ Manager of the different TripletSequence Series used by the fret phase.
    """
    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__(['experiments'])
