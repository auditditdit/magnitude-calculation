import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PlotWidget:
    def __init__(self, parent):
        self.fig = Figure(figsize=(6,3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot(self, times, amps, picks=None, title="Seismogram"):
        self.ax.clear()
        self.ax.plot(times, amps)
        if picks:
            for p in picks:
                self.ax.axvline(p, color='red', linestyle='--')
        self.ax.set_title(title)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()
