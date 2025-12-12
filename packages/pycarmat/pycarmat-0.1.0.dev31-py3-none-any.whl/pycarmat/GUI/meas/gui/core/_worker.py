from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QThread, Signal, QObject


class Worker(QThread):
    finished = Signal()
    result_signal = Signal(object)
    progress_signal = Signal(int)
    error_signal = Signal(str)

    def __init__(self, tab, params: dict):
        super().__init__()
        self.tab = tab
        self.params = params
        self._running = False

    def _run(self):
        pass

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.error_signal.emit(str(e))
            self.result_signal.emit(None)
        finally:
            self.finished.emit()
