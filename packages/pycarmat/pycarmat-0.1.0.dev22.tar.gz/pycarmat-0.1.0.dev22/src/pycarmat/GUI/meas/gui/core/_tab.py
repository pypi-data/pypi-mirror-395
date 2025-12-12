from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QMessageBox, QWidget, QApplication
from PySide6.QtCore import QThread


def is_dark_mode():
    app = QApplication.instance() or QApplication([])
    palette = app.palette()

    # Get system background and text color
    bg_color = palette.color(QPalette.Window).lightness()
    text_color = palette.color(QPalette.WindowText).lightness()

    # If background is darker than text, dark mode is active
    return bg_color < text_color


class Tab(QWidget):
    def __init__(self, gui_elements: tuple, **kargs):
        super().__init__()
        self.tabs = gui_elements
        self.gui = object()
        self.vars = object()
        self.worker = None
        self.thread = None
        self.progress_bar = None

        if 'min_width' in kargs:
            self.setMinimumWidth(kargs['min_width'])
        if 'width' in kargs:
            self.setFixedWidth(kargs['width'])
        if 'min_height' in kargs:
            self.setMinimumHeight(kargs['min_height'])
        if 'height' in kargs:
            self.setFixedHeight(kargs['height'])

        self._init()

    def _init(self):
        pass

    def _start_worker(self, worker):
        self.worker = worker
        self.thread = QThread()
        self.thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error_signal.connect(self.show_error_dialog)
        self.worker.progress_signal.connect(self.progress_bar.setValue)

        self.thread.start()

    def show_error_dialog(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()
