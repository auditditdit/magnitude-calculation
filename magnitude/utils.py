import numpy as np
from scipy.signal import butter, filtfilt

def bandpass_filter(amps, fs, low, high, order=4):
    ny = 0.5 * fs
    lowcut = low / ny
    highcut = high / ny
    b, a = butter(order, [lowcut, highcut], btype='band')
    return filtfilt(b, a, amps)

def find_peak_amplitude(amps):
    return np.max(np.abs(amps))