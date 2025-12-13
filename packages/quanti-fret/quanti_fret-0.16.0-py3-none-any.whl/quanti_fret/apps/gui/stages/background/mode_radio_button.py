from quanti_fret.algo import BackgroundMode
from quanti_fret.apps.gui.io_gui_manager import IOGuiManager

from qtpy.QtWidgets import QRadioButton


class BckgModeRadioButton(QRadioButton):
    """ Radio Button representing a Background mode.

    It keeps in memory the BackgroundMode associated with itself.
    """
    def __init__(
        self, phase: str, mode: BackgroundMode, *args, **kwargs
    ) -> None:
        """Constructor

        Args:
            phase (str): Phase of the widget
            mode (BackgroundMode): mode associated with the button
        """
        super().__init__(f'{mode}', *args, **kwargs)
        self._iopm = IOGuiManager().get_iopm(phase)
        self._mode = mode
        self._nbSequences = 0
        self.toggled.connect(self.switchMode)
        self._iopm.stateChanged.connect(self._updateSettings)

        self._updateSettings()

    @property
    def mode(self) -> BackgroundMode:
        """ mode getter.

        Returns:
            BackgroundMode: the mode associated with the button
        """
        return self._mode

    def switchMode(self, checked: bool) -> None:
        """ Set the config mode to this button mode if `checked` is set to
        True.

        Args:
            checked (bool): Weather or not the button is checked
        """
        if checked:
            self._iopm.config.set('Background', 'mode', self.mode)

    def _updateSettings(self) -> None:
        """ Tell the button that the settings changed.

        The button will update the number of sequences, and its toogling
        """
        self.blockSignals(True)
        # Set config mode
        current_mode = self._iopm.config.get('Background', 'mode')
        if current_mode == self.mode:
            self.setChecked(True)
        else:
            self.setChecked(False)
        self.blockSignals(False)
