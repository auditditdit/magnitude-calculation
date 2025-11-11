import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

from magnitude.seismo_io import read_csv_timeseries
from magnitude.signal import SeismicSignal
from magnitude.calculators import MagnitudeCalculator, MLParams, MSParams, MBParams
from magnitude.plot_widget import PlotWidget
from magnitude.utils import find_peak_amplitude

class MagnitudeApp:
    def __init__(self, root):
        self.root = root
        root.title("Kalkulasi Magnitudo (ML, MS, MB) - Demo")
        self.filepath = None
        self.signal = None

        # frame atas: tombol load
        top = tk.Frame(root)
        top.pack(side="top", fill="x")
        tk.Button(top, text="Load CSV", command=self.load_csv).pack(side="left")
        tk.Button(top, text="Compute", command=self.compute_magnitudes).pack(side="left")

        # frame parameter
        param = tk.Frame(root)
        param.pack(side="top", fill="x")
        tk.Label(param, text="Epicentral distance (km):").pack(side="left")
        self.dist_var = tk.DoubleVar(value=10.0)
        tk.Entry(param, textvariable=self.dist_var, width=8).pack(side="left")

        tk.Label(param, text="Amplitude unit note: mm assumed").pack(side="left", padx=10)

        # plot
        self.plot_widget = PlotWidget(root)

        # hasil
        bottom = tk.Frame(root)
        bottom.pack(side="top", fill="x")
        tk.Label(bottom, text="Results:").pack(anchor="w")
        self.result_text = tk.Text(bottom, height=6)
        self.result_text.pack(fill="x")

        # Setup default calculator
        mlp = MLParams(alpha=1.11, beta= -2.0)  # contoh default; ubah sesuai kalibrasi
        msp = MSParams(alpha=0.5, beta=0.0, period_T=20.0)
        mbp = MBParams(alpha=0.7, beta= -0.5, period_T=1.0)
        self.calc = MagnitudeCalculator(ml_params=mlp, ms_params=msp, mb_params=mbp)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv"), ("All files","*.*")])
        if not path:
            return
        try:
            times, amps = read_csv_timeseries(path)
            self.signal = SeismicSignal(times, amps)
            self.filepath = path
            self.plot_widget.plot(self.signal.times, self.signal.amps, title=f"Loaded: {path.split('/')[-1]}")
            messagebox.showinfo("Loaded", f"File loaded. Sample rate ~= {self.signal.sample_rate():.2f} Hz")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def compute_magnitudes(self):
        if self.signal is None:
            messagebox.showwarning("No data", "Silakan muat file CSV dulu.")
            return
        try:
            dist = float(self.dist_var.get())
        except Exception:
            messagebox.showerror("Input error", "Masukkan jarak (km) yang valid.")
            return

        # sederhana: ambil amplitude puncak seluruh trace (lebih baik pilih window sinyal)
        amp = find_peak_amplitude(self.signal.amps)
        # NOTE: pengguna harus pastikan unit amplitude cocok (mm)
        ml = self.calc.compute_ML(amp, max(dist, 0.1))
        ms = self.calc.compute_MS(amp, max(dist, 0.1))
        mb = self.calc.compute_MB(amp, max(dist, 0.1))

        # tampilkan
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f"File: {self.filepath}\n")
        self.result_text.insert("end", f"Peak amplitude (abs): {amp:.6g} (unit sesuai file)\n")
        self.result_text.insert("end", f"Distance: {dist:.2f} km\n\n")
        self.result_text.insert("end", f"Computed magnitudes (model params shown):\n")
        self.result_text.insert("end", f"ML = {ml:.3f}\n")
        self.result_text.insert("end", f"MS = {ms:.3f}\n")
        self.result_text.insert("end", f"MB = {mb:.3f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MagnitudeApp(root)
    root.mainloop()