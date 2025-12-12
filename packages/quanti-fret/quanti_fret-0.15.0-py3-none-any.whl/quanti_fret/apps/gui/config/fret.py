from quanti_fret.apps.gui.config.config import ConfigManagementWidget


class FretConfigManagementWidget(ConfigManagementWidget):
    """ Handle the selection and creation of config files of fret phase.
    """
    def __init__(self, *args, **kwargs) -> None:
        """ Constructor
        """
        super().__init__('fret', *args, **kwargs)
