from quanti_fret.core import QtfException, QtfSeries


class QtfSeriesManager:
    """ Manager of the different TripletSequence Series used by the Qtf apps.
    """
    def __init__(self, series_name: list[str]) -> None:
        """ Constructor
        """
        self._series: dict[str, QtfSeries] = {}
        for name in series_name:
            self._series[name] = QtfSeries([])

    def set(self, name: str, series: QtfSeries) -> None:
        """ Set the given series

        Args:
            name (str): the name of the series to add
            sequences (QtfSeries): the list of the sequences
                contained by the series
        """
        if name not in self._series.keys():
            raise QtfException(f'Unknown series "{name}"')
        self._series[name] = series

    def get(self, name: str | list[str]) -> QtfSeries:
        """ Get the series associated with the given name

        Args:
            name (str): name of the series

        Raises:
            QtfException: if the name is not valid

        Returns:
            QtfSeries: A QtfSeries created from the series sequence list
        """
        if type(name) is str:
            name = [name]

        series = QtfSeries([])
        for key in name:
            if key not in self._series.keys():
                raise QtfException(f'Unknown series "{key}"')
            series += self._series[key]
        return series
