from enum import Enum


class BackgroundMode(Enum):
    """ Mode to select on which series to perform the Background computation
    for the calibration phase.
    """
    DISABLED = 0
    MASK = 1
    PERCENTILE = 2
    FIXED = 3
    __order__ = 'DISABLED MASK PERCENTILE FIXED'

    def __str__(self) -> str:
        """ to string convertor

        Returns:
            str: the mode as a string
        """
        name_list = self.name.split('_')
        name_list = [word.capitalize() for word in name_list]
        name = ' + '.join(name_list)
        return name
