import pandas as pd
import numpy as np

def read_csv_timeseries(path, time_col='time', amp_col='amp'):
    """
    Membaca CSV dengan kolom waktu dan amplitudo.
    time_col: bisa unix time atau detik relatif, atau string waktu yang bisa di-parse pandas.
    Returns times (numpy array), amps (numpy array)
    """
    df = pd.read_csv(path)
    if time_col not in df.columns or amp_col not in df.columns:
        raise ValueError(f"CSV harus memiliki kolom '{time_col}' dan '{amp_col}'")
    # try convert time to float seconds if possible
    times = df[time_col].values
    amps = df[amp_col].values.astype(float)
    # jika times bukan numeric, coba parse ke datetime -> convert ke seconds from start
    if not np.issubdtype(times.dtype, np.number):
        times = pd.to_datetime(times)
        times = (times - times.iloc[0]).total_seconds().astype(float)
    return np.array(times, dtype=float), np.array(amps, dtype=float)
