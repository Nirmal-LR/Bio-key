import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from signal_processing.preprocess import load_ecg
from signal_processing.r_peak import detect_r_peaks
from hrv.hrv_calc import extract_hrv
from key_generation.session_key_generation import (
    generate_deterministic_key,
    generate_session_key,
)

def test_multiple_records():

    records = ["100", "101", "102", "103"]

    deterministic_keys = {}

    for record in records:
        print("\n==============================")
        print("Testing Record:", record)
        print("==============================")

        # Load ECG
        ecg, fs = load_ecg(f"data/{record}")

        # Limit to 60 seconds
        ecg = ecg[:fs * 60]

        # Extract HRV
        r_peaks = detect_r_peaks(ecg, fs)
        rr_intervals = extract_hrv(r_peaks, fs)

        # Generate keys
        deterministic_key = generate_deterministic_key(rr_intervals)
        session_key, nonce = generate_session_key(rr_intervals)

        print("Deterministic Key:", deterministic_key[:32])
        print("Session Key      :", session_key[:32])

        deterministic_keys[record] = deterministic_key

    # -------------------------------
    # Uniqueness Check
    # -------------------------------
    print("\n======= Uniqueness Analysis =======")

    unique_keys = set(deterministic_keys.values())

    if len(unique_keys) == len(records):
        print("All deterministic keys are unique across records.")
    else:
        print("Collision detected! Keys are not unique.")

    print("\nKey Summary:")
    for record, key in deterministic_keys.items():
        print(f"Record {record} → {key[:32]}")


if __name__ == "__main__":
    test_multiple_records()
