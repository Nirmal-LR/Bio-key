import wfdb
import neurokit2 as nk
import numpy as np


def load_ecg(record_path):
    record = wfdb.rdrecord(record_path)
    ecg_signal = record.p_signal[:, 0]
    fs = record.fs
    return ecg_signal, fs


def extract_hrv(ecg_signal, fs):
    signals, info = nk.ecg_process(ecg_signal, sampling_rate=fs)
    r_peaks = info["ECG_R_Peaks"]
    rr_intervals = np.diff(r_peaks) / fs
    return rr_intervals


def quantize_hrv(rr_intervals):
    threshold = np.mean(rr_intervals)
    binary_key = (rr_intervals > threshold).astype(int)
    return binary_key


if __name__ == "__main__":
    ecg, fs = load_ecg("data/100")
    rr_intervals = extract_hrv(ecg, fs)
    binary_key = quantize_hrv(rr_intervals)

    print("Binary key (first 64 bits):")
    print(binary_key[:64])
