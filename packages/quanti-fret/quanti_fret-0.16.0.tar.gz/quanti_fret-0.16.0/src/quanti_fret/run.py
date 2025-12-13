from quanti_fret.algo import (
    compute_background, BTCalculator, DECalculator, XMCalculator,
    FretCalculator
)
from quanti_fret.core import QtfSeries
from quanti_fret.io import IOManager

from typing import Callable


def _notify_disabled(msg: str) -> None:
    """ Default notify to use. Does nothing

    Args:
        msg (str): message to send (to the void)
    """
    pass


class QtfRunner:
    """ Manage the run of all the differents stages of the QuanTI-FRET
    algorithm.

    It gets its inputs and save its outputs using the IOPhaseManager passed to
    the constructor.
    """

    def __init__(self, iom: IOManager):
        """Constructor

        Args:
            iom (IOPhaseManager): IOManager to get params and retrive the
                results of each stage run for each phase.
        """
        self._iom = iom
        self._bt_calculator = BTCalculator()
        self._de_calculator = DECalculator()
        self._xm_calculator = XMCalculator()
        self._fret_calculator = FretCalculator()

    def run_all(self) -> None:
        """ Run the QuanTI-FRET stages
        """
        self.run_calibration()
        self.run_fret()

    def run_calibration(self) -> None:
        """ Run the QuanTI-FRET calibration stages
        """
        self.run_background()
        self.run_bt()
        self.run_de()
        self.run_xm()

    def run_background(self) -> None:
        """Run the Background computation

        Raises:
            QtfException: If it can't be run.
        """
        params = self._iom.cali.params.get('background')
        self._iom.cali.results['background'].clean_output()
        result = (compute_background(*params[1:]),)
        self._iom.cali.results['background'].save_stage(params, result)

    def run_bt(self, notify: Callable[[str], None] = _notify_disabled) -> None:
        """Run the BT calculation

        Args:
            notify (Callable[[str], None]): Callback that will be called
                between each steps to inform the user of the progress. Please
                note that the run will be paused while the callback is being
                called.

        Raises:
            QtfException: If it can't be run.
        """
        # Setup
        notify('Initialization')
        params = self._iom.cali.params.get('bt')
        series: QtfSeries = params[1]
        self._bt_calculator.reset()
        self._bt_calculator.params(*params[2:])  # type: ignore
        self._iom.cali.results['bt'].clean_output()

        # Adding the triplets one by one
        sit = series.iterator(sample_sequences=True)
        for triplet in sit:
            notify(f'Computing Triplet ({sit.current}/{sit.size})')
            figures = self._bt_calculator.add_triplet(
                triplet, sit.current_sequence.subfolder_crop(40)
            )
            self._iom.cali.results['bt'].save_triplet(sit, (figures,))

        # Computing Results
        notify('Computing Results')
        result = self._bt_calculator.compute_results()
        self._iom.cali.results['bt'].save_stage(params, result)

        # Done
        notify('Done')

    def run_de(self, notify: Callable[[str], None] = _notify_disabled) -> None:
        """Run the DE calculation

        Args:
            notify (Callable[[str], None]): Callback that will be called
                between each steps to inform the user of the progress. Please
                note that the run will be paused while the callback is being
                called.

        Raises:
            QtfException: If it can't be run.
        """
        # Setup
        notify('Initialization')
        params = self._iom.cali.params.get('de')
        series: QtfSeries = params[1]
        self._de_calculator.reset()
        self._de_calculator.params(*params[2:])  # type: ignore
        self._iom.cali.results['de'].clean_output()

        # Adding the triplets one by one
        sit = series.iterator(sample_sequences=True)
        for triplet in sit:
            notify(f'Computing Triplet ({sit.current}/{sit.size})')
            figures = self._de_calculator.add_triplet(
                triplet, sit.current_sequence.subfolder_crop(40)
            )
            self._iom.cali.results['de'].save_triplet(sit, (figures,))

        # Computing Results
        notify('Computing Results')
        result = self._de_calculator.compute_results()
        self._iom.cali.results['de'].save_stage(params, result)

        # Done
        notify('Done')

    def run_xm(self, notify: Callable[[str], None] = _notify_disabled) -> None:
        """Run the XM calculation

        Args:
            notify (Callable[[str], None]): Callback that will be called
                between each steps to inform the user of the progress. Please
                note that the run will be paused while the callback is being
                called.

        Raises:
            QtfException: If it can't be run.
        """
        # Setup
        notify('Initialization')
        params = self._iom.cali.params.get('xm')
        series: QtfSeries = params[1]
        self._xm_calculator.reset()
        self._xm_calculator.params(*params[2:])  # type: ignore
        self._iom.cali.results['xm'].clean_output()

        # Adding the triplets one by one
        sit = series.iterator(sample_sequences=True)
        for triplet in sit:
            notify(f'Computing Triplet ({sit.current}/{sit.size})')
            self._xm_calculator.add_triplet(triplet)

        # Computing Results
        notify('Computing Results')
        result = self._xm_calculator.compute_results()
        self._iom.cali.results['xm'].save_stage(params, result)

        # Done
        notify('Done')

    def run_fret(
        self, notify: Callable[[str], None] = _notify_disabled
    ) -> None:
        """Run the Fret calculation on the whole dataset

        Args:
            notify (Callable[[str], None]): Callback that will be called
                between each steps to inform the user of the progress. Please
                note that the run will be paused while the callback is being
                called.

        Raises:
            QtfException: If it can't be run.
        """
        # Setup
        notify('Initialization')
        params = self._iom.fret.params.get('fret')
        series: QtfSeries = params[1]
        self._fret_calculator.series_reset()
        self._fret_calculator.series_params(*params[2:])  # type: ignore
        self._iom.fret.results['fret'].clean_output()

        # Running fret on all the triplets
        sit = series.iterator()
        for triplet in sit:
            notify(f'Computing Fret ({sit.current}/{sit.size})')
            result = self._fret_calculator.series_run(triplet)
            self._iom.fret.results['fret'].save_triplet(sit, result)

        # Computing analysis
        notify('Performing analysis')
        analysis = self._fret_calculator.series_analysis(),
        self._iom.fret.results['fret'].save_stage(params, analysis)

        # Done
        notify('Done')
