import wfdb
import matplotlib.pyplot as plt


def load_ecg(record):
    """
    Load ECG signal from data folder.
    record: string like "100", "101", etc.
    """
    signal, fields = wfdb.rdsamp(f"data/{record}")
    fs = fields["fs"]
    ecg_signal = signal[:, 0]  # first channel
    return ecg_signal, fs


def plot_ecg(ecg_signal, fs, seconds=10):
    samples = int(seconds * fs)
    plt.figure(figsize=(12, 4))
    plt.plot(ecg_signal[:samples])
    plt.title("ECG Signal")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    ecg, fs = load_ecg("100")
    plot_ecg(ecg, fs)
