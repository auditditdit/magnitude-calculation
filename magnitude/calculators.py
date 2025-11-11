import math
from dataclasses import dataclass

@dataclass
class MLParams:
    # parameter model: bentuk umum ML = log10(A) + alpha*log10(R) + beta
    alpha: float = 1.11   # contoh default (bisa diubah sesuai kalibrasi lokal)
    beta: float = 0.0
    amplitude_unit: str = "mm"  # catatan: harus konsisten

@dataclass
class MSParams:
    # contoh bentuk: Ms = log10(A/T) + sigma(delta)  (here we approximate with linear term)
    alpha: float = 1.0
    beta: float = 0.0
    period_T: float = 20.0  # default periode surface wave (s)

@dataclass
class MBParams:
    # contoh: Mb = log10(A/T) + c1*log10(R) + c2
    alpha: float = 1.0
    beta: float = 0.0
    period_T: float = 1.0

class MagnitudeCalculator:
    def __init__(self, ml_params: MLParams = MLParams(),
                 ms_params: MSParams = MSParams(),
                 mb_params: MBParams = MBParams()):
        self.ml_params = ml_params
        self.ms_params = ms_params
        self.mb_params = mb_params

    def compute_ML(self, amplitude, distance_km):
        """
        amplitude: peak amplitude in mm (or unit sesuai ml_params)
        distance_km: epicentral distance in km
        Formula umum: ML = log10(A) + alpha*log10(distance) + beta
        NOTE: coefficients must be calibrated for the region!
        """
        if amplitude <= 0:
            raise ValueError("amplitude harus > 0")
        A = amplitude
        val = math.log10(A) + self.ml_params.alpha * math.log10(distance_km) + self.ml_params.beta
        return val

    def compute_MS(self, amplitude, distance_km, period=None):
        """
        Ms example: Ms = log10(A/T) + alpha*log10(distance) + beta
        A in mm, T in s
        """
        if period is None:
            period = self.ms_params.period_T
        if amplitude <= 0 or period <= 0:
            raise ValueError("A and T harus > 0")
        val = math.log10(amplitude / period) + self.ms_params.alpha * math.log10(distance_km) + self.ms_params.beta
        return val

    def compute_MB(self, amplitude, distance_km, period=None):
        if period is None:
            period = self.mb_params.period_T
        if amplitude <= 0 or period <= 0:
            raise ValueError("A and T harus > 0")
        val = math.log10(amplitude / period) + self.mb_params.alpha * math.log10(distance_km) + self.mb_params.beta
        return val
