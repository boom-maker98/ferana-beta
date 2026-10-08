

   
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ferana Sandbox", page_icon="⚡", layout="centered")

# --- UI BRANDING LAYER ---
st.markdown("<h1 style='text-align: center; color: #1e1e1e; font-family: monospace;'>Ferana // Biometric Sandbox v1.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #666;'>An exclusive real-time interactive playground for our private beta members to test the 3-Matrix Logic Engine.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- INPUT SECTION (DATA INGESTION) ---
st.subheader("📥 Step 1: Input Waking Biometrics")
col1, col2 = st.columns(2)
hrv = col1.number_input("Heart Rate Variability (HRV Score)", min_value=10, max_value=200, value=65, step=1, help="Your morning waking HRV score.")
rhr_drift = col1.slider("Resting Heart Rate (RHR) Drift", min_value=-10, max_value=15, value=0, step=1, help="How many BPM higher (+) or lower (-) your waking RHR is compared to your 30-day baseline.")
sleep_debt = col2.slider("Sleep Debt (Hours Short)", min_value=0.0, max_value=6.0, value=0.0, step=0.5, help="How many hours of sleep you are short from your ideal night.")
st.markdown("<br>", unsafe_allow_html=True)

# --- EXECUTION BUTTON ---
run_engine = st.button("Execute 3-Matrix Engine", use_container_width=True)

# --- INTERNAL DETERMINISTIC LOGIC ENGINE ---
# Matrix 1: Clinical Constraints / Safety Verification
matrix_1_status = "PASS"
safety_warnings = []
hr_cap_modifier = 0
if rhr_drift >= 7: matrix_1_status = "CRITICAL WARNING"
