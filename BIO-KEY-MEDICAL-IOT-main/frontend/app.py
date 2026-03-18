import sys
import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import time
import hashlib

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Backend imports
from signal_processing.preprocess import load_ecg
from signal_processing.r_peak import detect_r_peaks
from hrv.hrv_calc import extract_hrv
from key_generation.session_key_generation import (
    generate_deterministic_key,
    generate_session_key
)
from crypto.encryption import encrypt_data, decrypt_data

st.set_page_config(page_title="Bio-Key Medical IoT", layout="centered")

st.title("Privacy-Preserving Bio-Key for Medical IoT")
st.write("Biometric session key generation using ECG-based HRV.")

# ---------------------------
# Step 1: Select ECG Record
# ---------------------------
st.header("1. Select ECG Record")

record = st.selectbox(
    "Choose ECG record",
    ["100", "101", "102", "103"]
)

# ---------------------------
# Step 2: Process ECG
# ---------------------------
st.header("2. ECG Processing")

if st.button("Process ECG"):
    try:
        start_ecg = time.time()

        ecg, fs = load_ecg(record)
        r_peaks = detect_r_peaks(ecg, fs)
        r_peaks = np.array(r_peaks, dtype=int)

        rr_intervals = extract_hrv(r_peaks, fs)
        rr_intervals = np.array(rr_intervals, dtype=float)

        end_ecg = time.time()

        st.session_state["ecg"] = ecg
        st.session_state["r_peaks"] = r_peaks
        st.session_state["rr"] = rr_intervals
        st.session_state["fs"] = fs
        st.session_state["ecg_time"] = end_ecg - start_ecg

        st.success("ECG processed successfully")

    except Exception as e:
        st.error(f"Processing error: {e}")

# ---------------------------
# ECG and HRV Display
# ---------------------------
if "ecg" in st.session_state:
    ecg = st.session_state["ecg"]
    r_peaks = st.session_state["r_peaks"]
    rr_intervals = st.session_state["rr"]

    st.subheader("ECG Signal with R-peaks")
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(ecg[:2000], label="ECG")
    valid_peaks = r_peaks[r_peaks < 2000]
    ax.scatter(valid_peaks, ecg[valid_peaks], color="red", label="R-peaks")
    ax.legend()
    st.pyplot(fig)

    st.subheader("HRV (RR Intervals)")
    fig2, ax2 = plt.subplots(figsize=(10, 3))
    ax2.plot(rr_intervals, marker="o")
    st.pyplot(fig2)

    st.write("ECG Processing Time:",
             round(st.session_state["ecg_time"], 6), "seconds")

# ---------------------------
# Step 3: Generate Keys
# ---------------------------
st.header("3. Generate Keys")

if st.button("Generate Bio-Key"):
    if "rr" not in st.session_state:
        st.error("Process ECG first.")
    else:
        try:
            rr_intervals = st.session_state["rr"]

            # Deterministic key timing
            start_det = time.time()
            det_key = generate_deterministic_key(rr_intervals)
            end_det = time.time()

            # Session key timing
            start_sess = time.time()
            session_key = generate_session_key(det_key)
            end_sess = time.time()

            st.session_state["det_key"] = det_key
            st.session_state["session_key"] = session_key
            st.session_state["det_time"] = end_det - start_det
            st.session_state["sess_time"] = end_sess - start_sess
            st.session_state["total_key_time"] = end_sess - start_det

        except Exception as e:
            st.error(f"Key generation error: {e}")

# Display keys and metrics persistently
if "det_key" in st.session_state:
    st.subheader("Deterministic Key")
    st.code(st.session_state["det_key"])

    st.subheader("Session Key")
    st.code(st.session_state["session_key"])

    aes_key = hashlib.sha256(
        st.session_state["session_key"].encode()
    ).digest()

    st.subheader("Key Performance Metrics")
    st.write("Deterministic Key Time:",
             round(st.session_state["det_time"], 6), "seconds")
    st.write("Session Key Time:",
             round(st.session_state["sess_time"], 6), "seconds")
    st.write("Total Key Derivation Time:",
             round(st.session_state["total_key_time"], 6), "seconds")
    st.write("AES Key Size:", len(aes_key) * 8, "bits")

# ---------------------------
# Step 4: Encryption
# ---------------------------
st.header("4. Encryption Demo")

if "rr" in st.session_state:
    rr_intervals = st.session_state["rr"]
    avg_rr = np.mean(rr_intervals)
    heart_rate = 60 / avg_rr
    medical_data = f"Heart rate: {heart_rate:.1f} bpm"
    st.write("Medical Data:", medical_data)
else:
    medical_data = None
    st.info("Process ECG first to generate medical data.")

if st.button("Encrypt Data"):
    if "session_key" not in st.session_state or medical_data is None:
        st.error("Generate session key first.")
    else:
        try:
            key = hashlib.sha256(
                st.session_state["session_key"].encode()
            ).digest()

            start_enc = time.time()
            ciphertext = encrypt_data(medical_data.encode(), key)
            end_enc = time.time()

            st.session_state["ciphertext"] = ciphertext
            st.session_state["enc_time"] = end_enc - start_enc

        except Exception as e:
            st.error(f"Encryption error: {e}")

if "ciphertext" in st.session_state:
    st.subheader("Encrypted Data (hex)")
    st.code(st.session_state["ciphertext"].hex())
    st.write("Encryption Time:",
             round(st.session_state["enc_time"], 6), "seconds")

# ---------------------------
# Decryption
# ---------------------------
if st.button("Decrypt Data"):
    if "ciphertext" not in st.session_state:
        st.error("No encrypted data found.")
    else:
        try:
            key = hashlib.sha256(
                st.session_state["session_key"].encode()
            ).digest()

            start_dec = time.time()
            plaintext = decrypt_data(st.session_state["ciphertext"], key)
            end_dec = time.time()

            st.session_state["plaintext"] = plaintext
            st.session_state["dec_time"] = end_dec - start_dec

        except Exception as e:
            st.error(f"Decryption error: {e}")

if "plaintext" in st.session_state:
    st.subheader("Decrypted Data")
    st.code(st.session_state["plaintext"].decode())
    st.write("Decryption Time:",
             round(st.session_state["dec_time"], 6), "seconds")