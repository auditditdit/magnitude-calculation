import numpy as np
from scipy.signal import detrend

class SeismicSignal:
    def __init__(self, times: np.ndarray, amps: np.ndarray, station=None):
        assert len(times) == len(amps), "times dan amps harus sama panjang"
        self.times = times
        self.amps = amps
        self.station = station

    def sample_rate(self):
        dt = np.diff(self.times)
        if len(dt)==0: return None
        return 1.0 / np.median(dt)

    def window(self, t0, t1):
        mask = (self.times >= t0) & (self.times <= t1)
        return SeismicSignal(self.times[mask], self.amps[mask], station=self.station)

    def max_amplitude(self):
        return np.max(np.abs(self.amps))

    def peak_to_peak(self):
        return np.max(self.amps) - np.min(self.amps)

    def rms(self):
        return np.sqrt(np.mean(self.amps**2))

    def detrended(self):
        return SeismicSignal(self.times, detrend(self.amps), station=self.station)
