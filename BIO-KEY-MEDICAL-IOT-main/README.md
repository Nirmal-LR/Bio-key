**1. Project Title**

Privacy-Preserving Bio-Key for Medical IoT

**2. Problem Statement**

Passwords and stored keys are unsafe for medical IoT devices.

**3. Proposed Solution**

Use HRV-based biometric entropy to derive session encryption keys.

**4. Technologies Used**

Python, WFDB, NeuroKit2, AES, ECG datasets

**5. How to Run**
pip install -r requirements.txt
python signal_processing/preprocess.py
python signal_processing/r_peak.py
python hrv/hrv_calc.py
python key_generation/error_correction.py
python crypto/encryption.py

**6. Disclaimer**

Software proof-of-concept. No real medical devices.