import numpy as np
import hashlib
import os


# -------------------------------
# Deterministic Key (No Nonce)
# -------------------------------
def generate_deterministic_key(rr_intervals):
    """
    Generate a reproducible biometric key.
    Same RR input → Same key.
    """
    rr_intervals = np.array(rr_intervals, dtype=float)

    if rr_intervals is None or len(rr_intervals) < 40:
        raise ValueError("Insufficient HRV data for deterministic key")

    num_features = min(40, len(rr_intervals))
    features = np.round(rr_intervals[:num_features], 3)

    deterministic_key = hashlib.sha256(features.tobytes()).hexdigest()

    return deterministic_key


# -------------------------------
# Session-Based Key (With Nonce)
# -------------------------------
def generate_session_key(deterministic_key):
    """
    Generate session-based dynamic key.
    Deterministic key + random nonce.
    """
    if deterministic_key is None:
        raise ValueError("Deterministic key required")

    nonce = os.urandom(16)

    session_key = hashlib.sha256(
        deterministic_key.encode() + nonce
    ).hexdigest()

    return session_key
