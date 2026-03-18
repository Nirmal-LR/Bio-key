import numpy as np
import neurokit2 as nk

def detect_r_peaks(ecg_signal, fs):
    """
    Detect R-peak indices from ECG signal.
    Returns a numeric numpy array of peak indices.
    """
    _, info = nk.ecg_process(ecg_signal, sampling_rate=fs)
    r_peaks = info["ECG_R_Peaks"]

    # Force numeric array
    r_peaks = np.array(r_peaks, dtype=int)

    return r_peaks
