import math
from magnitude.calculators import MagnitudeCalculator, MLParams

def test_ml_basic():
    mlp = MLParams(alpha=1.0, beta=0.0)
    calc = MagnitudeCalculator(ml_params=mlp)
    # jika amplitude=10 mm, distance=10 km -> ML = log10(10) + 1*log10(10) = 1 + 1 = 2
    val = calc.compute_ML(10.0, 10.0)
    assert abs(val - 2.0) < 1e-6
