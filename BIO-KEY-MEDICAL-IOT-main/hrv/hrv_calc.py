import numpy as np
import matplotlib.pyplot as plt


def extract_hrv(r_peaks, fs):
    """
    Compute RR intervals (HRV) from R-peak indices.
    """
    if r_peaks is None or len(r_peaks) < 2:
        raise ValueError("Not enough R-peaks to compute HRV")

    # Ensure numeric type
    r_peaks = np.array(r_peaks, dtype=float)

    rr_intervals = np.diff(r_peaks) / float(fs)
    return rr_intervals


def plot_hrv(rr_intervals):
    plt.figure(figsize=(10, 4))
    plt.plot(rr_intervals, marker="o")
    plt.title("Heart Rate Variability (RR Intervals)")
    plt.xlabel("Beat Number")
    plt.ylabel("RR Interval (seconds)")
    plt.grid(True)
    plt.show()
