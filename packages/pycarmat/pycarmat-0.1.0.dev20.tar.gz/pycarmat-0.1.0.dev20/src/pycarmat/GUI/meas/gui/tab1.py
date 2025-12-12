import numpy as np
from PySide6.QtWidgets import QVBoxLayout, QCheckBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets as QTW
from matplotlib.figure import Figure

from skrf import Network

from .core import Tab, is_dark_mode


def moving_average(data: Network, half_window_size=5):
    f = data.f
    S = np.zeros((f.shape[0], 2, 2), dtype=complex) * np.nan

    i_start = half_window_size
    i_end = f.shape[0] - half_window_size

    for i in range(i_start, i_end):
        S[i, 0, 0] = np.mean(data.s[i - half_window_size:i + half_window_size, 0, 0])
        S[i, 0, 1] = np.mean(data.s[i - half_window_size:i + half_window_size, 0, 1])
        S[i, 1, 0] = np.mean(data.s[i - half_window_size:i + half_window_size, 1, 0])
        S[i, 1, 1] = np.mean(data.s[i - half_window_size:i + half_window_size, 1, 1])

    return Network(s=S, frequency=f)


class Tab1(Tab):
    def __init__(self, gui_elements: tuple = (), **kargs):
        super().__init__(gui_elements, **kargs)
        self.ntw = None

    def _init(self):
        layout = QVBoxLayout(self)
        self.smooth_checkbox = QCheckBox("Smoothing")
        self.smooth_checkbox.stateChanged.connect(self.refresh_graph)
        layout.addWidget(self.smooth_checkbox)

        self._main = QTW.QWidget()
        layout_fig = QTW.QVBoxLayout(self._main)
        self.fig = Figure(figsize=(8, 6))
        self.axes = self.fig.subplots(2, 2)
        self.fig.tight_layout()

        for ax in self.axes.flat:
            ax.grid(axis='both', which='both')

        self.axes[0, 0].set_title("S11, S22 mag (dB)", color="white" if is_dark_mode() else "black")
        self.axes[0, 1].set_title("S11, S22 phase", color="white" if is_dark_mode() else "black")
        self.axes[1, 0].set_title("S12, S21 mag (dB)", color="white" if is_dark_mode() else "black")
        self.axes[1, 1].set_title("S12, S21 phase", color="white" if is_dark_mode() else "black")

        self.canvas = FigureCanvas(self.fig)
        layout_fig.addWidget(self.canvas)
        layout.addWidget(self._main)

    def refresh_graph(self):
        if self.ntw is not None:
            self.update_graph(self.ntw)

    def update_graph(self, ntw):
        if ntw is None:
            return

        self.ntw = ntw

        if self.smooth_checkbox.isChecked():
            _ntw = moving_average(self.ntw, half_window_size=5)
        else:
            _ntw = self.ntw

        f_min = np.min(_ntw.f / 1e9)
        f_max = np.max(_ntw.f / 1e9)

        freq = _ntw.f / 1e9
        s_params = _ntw.s

        self.axes[0, 0].clear()
        self.axes[0, 0].plot(freq, 20*np.log10(np.abs(s_params[:, 0, 0])), color="lightcoral", label="S11", linewidth=2)
        self.axes[0, 0].plot(freq, 20*np.log10(np.abs(s_params[:, 1, 1])), color="lightskyblue", label="S22",
                             linewidth=2)
        self.axes[0, 0].set_title("S11, S22 mag (dB)", color="white" if is_dark_mode() else "black")
        l00 = self.axes[0, 0].legend(loc='lower right')
        self.axes[0, 0].set_xlim(f_min, f_max)

        self.axes[0, 1].clear()
        self.axes[0, 1].plot(freq, np.angle(s_params[:, 0, 0], deg=True), color="lightcoral", label="S11", linewidth=2)
        self.axes[0, 1].plot(freq, np.angle(s_params[:, 1, 1], deg=True), color="lightskyblue", label="S22",
                             linewidth=2)
        self.axes[0, 1].set_title("S11, S22 phase", color="white" if is_dark_mode() else "black")
        l01 = self.axes[0, 1].legend(loc='lower right')
        self.axes[0, 1].set_xlim(f_min, f_max)

        self.axes[1, 0].clear()
        self.axes[1, 0].plot(freq, 20*np.log10(np.abs(s_params[:, 1, 0])), color="lightcoral", label="S12", linewidth=2)
        self.axes[1, 0].plot(freq, 20*np.log10(np.abs(s_params[:, 0, 1])), color="lightskyblue", label="S21",
                             linewidth=2)
        self.axes[1, 0].set_title("S12, S21 mag (dB)", color="white" if is_dark_mode() else "black")
        l10 = self.axes[1, 0].legend(loc='lower right')
        self.axes[1, 0].set_xlim(f_min, f_max)

        self.axes[1, 1].clear()
        self.axes[1, 1].plot(freq, np.angle(s_params[:, 1, 0], deg=True), color="lightcoral", label="S12")
        self.axes[1, 1].plot(freq, np.angle(s_params[:, 0, 1], deg=True), color="lightskyblue", label="S21")
        self.axes[1, 1].set_title("S12, S21 phase", color="white" if is_dark_mode() else "black")
        l11 = self.axes[1, 1].legend(loc='lower right')
        self.axes[1, 1].set_xlim(f_min, f_max)

        for ax in self.axes.flat:
            if is_dark_mode():
                ax.grid(color=(.25, .25, .25))
            else:
                ax.grid(color="#bbb")

        def set_legend_style(_legend):
            if is_dark_mode():
                _legend.get_frame().set_facecolor("#222")
                _legend.get_frame().set_edgecolor("#222")
                for text in _legend.get_texts():
                    text.set_color("white")

        set_legend_style(l00)
        set_legend_style(l01)
        set_legend_style(l10)
        set_legend_style(l11)

        self.canvas.draw()


