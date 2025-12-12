from quanti_fret.apps.cli.view.printers import print_title

import abc


class StageView(abc.ABC):
    """ Handle the view of a specific stage.
    """

    def __init__(self, title: str, separator_lenth: int) -> None:
        """ Constructor

        Args:
            title (str): Title of the view
            separator_lenth (int): The expected length for the separators
        """
        self._stage_title = title
        self._separator_length = separator_lenth

    def title(self):
        """ Print the title of the stage

        It surround the title with "#"s and limit the width to
        `self._separator_length`.
        """
        print_title(self._stage_title, self._separator_length)

    @abc.abstractmethod
    def settings(self) -> None:
        """ Print the settings of the stage
        """
        pass

    def results(self):
        """ Print the results of the stage
        """
        pass
