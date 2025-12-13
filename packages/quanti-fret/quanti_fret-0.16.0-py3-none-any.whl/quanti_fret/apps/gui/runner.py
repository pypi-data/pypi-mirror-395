from quanti_fret.apps.gui.io_gui_manager import IOGuiManager

from quanti_fret.core import QtfException
from quanti_fret.run import QtfRunner

from qtpy.QtCore import QMutex, QObject, QThread, Signal


class SingletonQObject(type(QObject)):  # type: ignore
    """ Class that provides a singleton compatible with QObject
    """
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CalculatorRunner(QObject, metaclass=SingletonQObject):
    """ Class that perform the run of the differents calculation stages.

    It control the access to the ressourced by allowing only one run to be
    performed at a time.

    It delegates the actual run to the `CalculatorWorker` that is working in a
    thread.

    To inform other widgets of its state, it provides the following signals:
        * `runAvailable`: Signaling that the run is currently available
        * `runDisabled`: Signaling that the run is currently disabled
        * `finished`: Signaling that the run is finished. Also gives the stage
            that was run so that the widget can know if they were concerned
            or not.
        * `progress`: Signaling the progress of the run (not used in all
            stages)
    It also have the following signal for internal use:
        `_runWorker`: Ask the worker to start the run on the given stage.
    """
    runAvailable = Signal()
    runDisabled = Signal()
    finished = Signal(str)
    progress = Signal(str)
    _runWorker = Signal(str)

    def __init__(self):
        """ Constructor
        """
        super().__init__()

        self._mutex = QMutex()

    def run(self, stage: str) -> None:
        """ Run the computation for the given stage.

        It perform the following steps:
            * Locks the run
            * Emit the signal `runDisabled`
            * Create the worker and the thread it will run inside
            * Run the worker by emitting the signal `_runWorker`

        If the run is already locked, does nothing

        Args:
            stage (str): Stage to Run
        """
        if self._mutex.tryLock():
            # Disable other buttons
            self.runDisabled.emit()

            # Instanciate the Thread and the workers and link them
            self._worker = CalculatorWorker()
            self._thread = QThread()
            self._worker.moveToThread(self._thread)
            self._worker.finished.connect(self._worker.deleteLater)
            self._worker.finished.connect(self._thread.quit)
            self._thread.finished.connect(self._thread.deleteLater)

            # Connect the app signals
            self._runWorker.connect(self._worker.run)
            self._thread.finished.connect(lambda: self._finished(stage))
            self._worker.progress.connect(self._progress)

            # Start the Thread
            self._thread.start()

            # Start the worker (We can't use the Thread started signal as we
            # would need a lambda function that doesn't run in the thread and
            # freezes the GUI)
            self._runWorker.emit(stage)

    def _finished(self, stage):
        """ Free the run and notify that the calculation is finished.

        It perform the following steps:
            * Emit the signal `finished` with the stage associated
            * Emit the signal `runAvailable` to say that the run is now
                available
            * Unlock the run

        Args:
            stage (str): Stage to that was run
        """
        self.runAvailable.emit()
        self.finished.emit(stage)
        self._mutex.unlock()

    def _progress(self, msg: str):
        """ Emit the progress signal to inform of the runner's progress.

        Args:
            msg (str): Progress message to send
        """
        self.progress.emit(msg)


class CalculatorWorker(QObject):
    """ Worker class to perform calculation in a thread.

    It delegates the run to the `QtfRunner` class by selecting the proper
    mehtod to call depending on the stage name passed as parameter to its
    `run` method.

    Use it as follow:
        * Attach the worker to a thread
        * Connect the thread's `finished` signal to `self.deleteLater`
        * Trigger the worker connecting the `run()` function to a signal
        * Retrieve the finish state by connecting to the signal `finished`
        * Retrieve the progress state by connecting to the signal `progress`
            (Used only for Fret stage)
        * Start the thread
    """
    finished = Signal(str)
    progress = Signal(str)

    def __init__(self) -> None:
        """ Constructor
        """
        super().__init__()
        self._runner = QtfRunner(IOGuiManager().iom)

    def run(self, stage: str) -> None:
        """ Run the computation for the given run.

        Once finished, emit the signal `finished`.

        Args:
            stage (str): Stage to Run
        """
        if stage == 'background':
            self._runner.run_background()
        elif stage == 'bt':
            self._runner.run_bt(notify=self.emit_progress)
        elif stage == 'de':
            self._runner.run_de(notify=self.emit_progress)
        elif stage == 'xm':
            self._runner.run_xm(notify=self.emit_progress)
        elif stage == 'fret':
            self._runner.run_fret(notify=self.emit_progress)
        else:
            raise QtfException(f'Unknown stage to run: {stage}')
        self.finished.emit(stage)

    def emit_progress(self, msg: str) -> None:
        """ Emit the progress of a run

        used only for the Fret stage

        Args:
            msg (str): Progress to display
        """
        self.progress.emit(msg)
