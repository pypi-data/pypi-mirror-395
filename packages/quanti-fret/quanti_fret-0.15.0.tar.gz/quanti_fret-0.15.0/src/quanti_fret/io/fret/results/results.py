from quanti_fret.io.base import ResultsManager
from quanti_fret.io.fret.results.fret import FretResults, StageResults

from pathlib import Path


class FretResultsManager(ResultsManager):
    """ Manage the saving of the settings and results of the different stages
    of the Fret.
    """
    def __init__(self, output_path: Path) -> None:
        """Constructor

        Args:
            output_path (Path): Path to the output directory
        """
        self._check_output_dir(output_path)
        managers: dict[str, StageResults] = {
            'fret': FretResults(output_path),
        }
        super().__init__(managers)
