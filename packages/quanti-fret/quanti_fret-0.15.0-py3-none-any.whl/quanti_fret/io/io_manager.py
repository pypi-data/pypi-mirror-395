from quanti_fret.io.base import IOPhaseManager


class IOManager:
    """ Single class having access to the IOPhaseManager for calibration and
    Fret.
    """
    def __init__(
        self, iopm_cali: IOPhaseManager, iopm_fret: IOPhaseManager
    ) -> None:
        """ Constructor

        Args:
            iopm_cali (CalibrationIOPhaseManager | None, optional): The
                IOPhaseManager associated with the calibration.
                Defaults to None.
            iopm_fret (FretIOPhaseManager | None, optional): The IOPhaseManager
                associated with the fret. Defaults to None.
        """
        self._iopm_cali = iopm_cali
        self._iopm_fret = iopm_fret
        iopm_cali.link_iopm(iopm_fret)

    @property
    def cali(self) -> IOPhaseManager:
        """ Getter of the Calibration iopm

        Returns:
            IOPhaseManager: The calibration io manager
        """
        return self._iopm_cali

    @property
    def fret(self) -> IOPhaseManager:
        """ Getter of the Fret iopm

        Returns:
            IOPhaseManager: The fret io manager
        """
        return self._iopm_fret
