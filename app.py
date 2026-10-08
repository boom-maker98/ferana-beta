

   
import streamlit as st
import numpy as np

st.set_page_config(page_title="Ferana Sandbox", page_icon="⚡", layout="centered")

# Paste your Google Form link here when you have one
FEEDBACK_FORM_URL = "https://forms.gle/REPLACE-WITH-YOUR-FORM-LINK"

# --- UI BRANDING LAYER ---
st.markdown("<h1 style='text-align: center; font-family: monospace;'>Ferana // Biometric Sandbox v1.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>A private beta playground to test the 3-Matrix Logic Engine.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- STEP 1: INPUTS ---
st.subheader("📥 Step 1: Input Waking Biometrics")
col1, col2 = st.columns(2)
hrv = col1.number_input("Heart Rate Variability (HRV Score)", min_value=10, max_value=200, value=65, step=1, help="Your morning waking HRV score.")
rhr_drift = col1.slider("Resting Heart Rate (RHR) Drift", min_value=-10, max_value=15, value=0, step=1, help="How many BPM higher (+) or lower (-) your waking RHR is compared to your 30-day baseline.")
sleep_debt = col2.slider("Sleep Debt (Hours Short)", min_value=0.0, max_value=6.0, value=0.0, step=0.5, help="How many hours of sleep you are short from your ideal night.")
cycle_phase = col2.selectbox("Cycle phase (optional)", ["Not tracking", "Menstrual", "Follicular", "Ovulatory", "Luteal"], help="Optional. Not saved anywhere.")
st.markdown("<br>", unsafe_allow_html=True)
run_engine = st.button("Execute 3-Matrix Engine", type="primary")
st.caption("Prototype for testing only. Not medical advice. Nothing you enter is saved.")

# Keep results on screen after the first click
if run_engine: st.session_state["ran"] = True
if not st.session_state.get("ran", False): st.stop()

# --- MATRIX 1: CLINICAL CONSTRAINTS / SAFETY VERIFICATION ---
checks = [
(rhr_drift >= 7, "Resting heart rate is 7+ BPM above your baseline, which can signal illness, stress, or under-recovery."),
(sleep_debt >= 4, "Sleep debt is 4+ hours, so injury risk goes up on hard sessions."),
(hrv < 30, "HRV is very low today, so recovery should come first."),
]
safety_warnings = [msg for flag, msg in checks if flag]
matrix_1_status = "CRITICAL WARNING" if rhr_drift >= 7 else ("CAUTION" if safety_warnings else "PASS")
hr_cap_modifier = -10 if matrix_1_status == "CRITICAL WARNING" else (-5 if matrix_1_status == "CAUTION" else 0)

# --- MATRIX 2: READINESS SCORE ---
hrv_pts = float(np.clip((hrv - 20) / 80, 0, 1)) * 45
rhr_pts = float(np.clip((15 - rhr_drift) / 25, 0, 1)) * 30
sleep_pts = float(np.clip(1 - sleep_debt / 6, 0, 1)) * 25
readiness = int(round(hrv_pts + rhr_pts + sleep_pts))
readiness = min(readiness, 39) if matrix_1_status == "CRITICAL WARNING" else readiness

# --- MATRIX 3: DAILY PRESCRIPTION ---
tiers = [
(80, "PUSH", "45-60 min", "Zone 4 (80-90% of max HR)", ["Heavy strength work", "Hard intervals", "Sprint or tempo session"]),
(60, "BUILD", "40-50 min", "Zone 3 (70-80% of max HR)", ["Moderate strength circuit", "Steady tempo cardio", "Hill walk or bike"]),
(40, "MAINTAIN", "30-40 min", "Zone 2 (60-70% of max HR)", ["Light strength or Pilates", "Easy jog or swim", "Brisk walk"]),
(0, "RECOVER", "15-30 min", "Zone 1 (under 60% of max HR)", ["Gentle yoga or mobility", "Easy walk", "Stretching and breathwork"]),
]
tier_name, tier_duration, tier_zone, tier_ideas = next((t[1], t[2], t[3], t[4]) for t in tiers if readiness >= t[0])
phase_notes = {
"Not tracking": "",
"Menstrual": "Energy can run lower for some people, so lean toward the lighter end of today's plan if you feel off.",
"Follicular": "Many people feel strong and recover well in this phase, so it can be a good time to push if readiness agrees.",
"Ovulatory": "Some people feel their strongest here. Warm up thoroughly before hard efforts.",
"Luteal": "Some people see a slightly higher resting heart rate late in this phase. Still follow the safety check above.",
}

# --- STEP 2: RESULTS ---
st.markdown("---")
st.subheader("📊 Step 2: Your Engine Results")
c1, c2, c3 = st.columns(3)
c1.metric("Matrix 1: Safety", matrix_1_status)
c2.metric("Matrix 2: Readiness", str(readiness) + "/100")
c3.metric("Matrix 3: Plan", tier_name)
st.progress(readiness / 100)
if safety_warnings: st.warning("\n\n".join("⚠️ " + w for w in safety_warnings))
if not safety_warnings: st.success("✅ All safety checks passed.")
st.markdown("**Today's prescription:** " + tier_duration + " at " + tier_zone)
st.markdown("\n".join("- " + idea for idea in tier_ideas))
if hr_cap_modifier != 0: st.info("Safety adjustment: keep effort about " + str(abs(hr_cap_modifier)) + "% below the zone above.")
if cycle_phase != "Not tracking": st.caption("Cycle note (" + cycle_phase + "): " + phase_notes[cycle_phase])

# --- STEP 3: FEEDBACK ---
st.markdown("---")
st.subheader("💬 Step 3: Help us improve")
st.write("Was this plan useful? What was confusing or missing? It takes under a minute.")
if "REPLACE" not in FEEDBACK_FORM_URL: st.link_button("Give feedback", FEEDBACK_FORM_URL)
if "REPLACE" in FEEDBACK_FORM_URL: st.info("Feedback link coming soon.")
