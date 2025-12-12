from quanti_fret.core import QtfException
from quanti_fret.io.base.results.stage import StageResults

from pathlib import Path


class ResultsManager:
    """ Manage the saving of the different stages settings and results.
    """
    def __init__(self, stages_managers: dict[str, StageResults]) -> None:
        """Constructor

        Args:
            stages_managers (dict[str, StageResults]): Dictionary containing
                all the stages available to store the results, with their
                StageResults associated.
        """
        self._managers = stages_managers

    def set_clean_all_output(self, val: bool) -> None:
        """ Decide whether or not to clean all the output folder of the
        different stages when calling their `clean_output` method.

        If set to True, all the output folder will be deleted when calling
        `clean_output`. If set to False, only the dump folder will be deleted.

        Args:
            val (bool): Value to set
        """
        for manager in self._managers.values():
            manager.set_clean_all_output(val)

    def __getitem__(self,  stage: str) -> StageResults:
        """ Get the StageResult associated with the given stage

        Args:
            stage (str): Stage name in ['background', 'bt', 'de', 'xm', 'fret']

        Raises:
            QtfException: If the stage is unknown.

        Returns:
            StageResults: The StageResults associated.
        """
        if stage not in self._managers:
            err = f'No StageManager exists for stage "{stage}"'
            raise QtfException(err)
        return self._managers[stage]

    def _check_output_dir(self, output_dir: Path) -> None:
        """ Check if the output dir is valid

        Args:
            output_dir (Path): path to test

        Raises:
            QtfException: If the output dir is invalid
        """
        if not isinstance(output_dir, Path):
            err = 'Output path is not an instance of Path'
            raise QtfException(err)
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        if not output_dir.is_dir():
            err = f'Output path {output_dir} exists and is not a directory'
            raise QtfException(err)
