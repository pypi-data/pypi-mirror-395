from quanti_fret.apps.cli.view.printers import print_bullet_list
from quanti_fret.apps.cli.view.stage_view import StageView

from quanti_fret.io import IOPhaseManager

from pathlib import Path


class SeriesView(StageView):
    """ CLI view that display series loading informations
    """

    def __init__(
        self, iopm: IOPhaseManager, separator_lenth: int, series: list[str]
    ) -> None:
        """ Constructor

        Args:
            iopm (IOPhaseManager): iopmanage used to get the information to
                display
            separator_lenth (int): The expected length for the separators
            series (list[str]): List of series to look for
        """
        super().__init__("Loading Sequences' series", separator_lenth)
        self._iopm = iopm
        self._series = series

    def settings(self) -> None:
        """ Print the settings of the stage

        Nothing to display here
        """
        print('Sequences found:')

    def results(self):
        """ Print the results of the stage

        It displays all the series with their path and number of sequences
        found.
        """
        series_manager = self._iopm.series
        config = self._iopm.config
        for series_name in self._series:
            path = config.get('Series', series_name)
            size = series_manager.get(series_name).size
            self._print_series(series_name, path, size)

    def _print_series(
        self, series: str, path: Path | str, nb_found: int
    ) -> None:
        """ Print a series information

        Args:
            series (str): Name of the series
            path (Path): Series path
            nb_found (int): Number of sequences found for this series
        """
        print_bullet_list(1, [series])
        print_bullet_list(2, [f'Path: {path}', f'Sequences found: {nb_found}'])
