

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Ferana Sandbox", page_icon="⚡", layout="centered")

# Paste your Google Form link here when you have one
FEEDBACK_FORM_URL = "https://forms.gle/REPLACE-WITH-YOUR-FORM-LINK"

# --- UI BRANDING LAYER ---
st.markdown("<h1 style='text-align: center; font-family: monospace;'>Ferana // Biometric Sandbox v1.1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>Stress resilience for women who wear wearables. A private beta playground for the 3-Matrix Logic Engine.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- STEP 1: INPUTS ---
st.subheader("📥 Step 1: Input Waking Biometrics")
name = st.text_input("First name (optional)")
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
(rhr_drift >= 7, "Resting heart rate is 7+ BPM above your baseline, which can signal illness, stress, or under-recovery. If you feel unwell (fever, chest pain, dizziness), skip the movement and rest."),
(sleep_debt >= 4, "Sleep debt is 4+ hours, so today's routine is softened to protect recovery."),
(hrv < 30, "HRV is very low today, so today's routine leans on nervous system support."),
]
safety_warnings = [msg for flag, msg in checks if flag]
matrix_1_status = "CRITICAL WARNING" if rhr_drift >= 7 else ("CAUTION" if safety_warnings else "PASS")

# --- MATRIX 2: RESILIENCE SCORE (higher = more resilient) ---
hrv_pts = float(np.clip((hrv - 20) / 80, 0, 1)) * 45
rhr_pts = float(np.clip((15 - rhr_drift) / 25, 0, 1)) * 30
sleep_pts = float(np.clip(1 - sleep_debt / 6, 0, 1)) * 25
resilience = int(round(hrv_pts + rhr_pts + sleep_pts))
resilience = min(resilience, 39) if matrix_1_status == "CRITICAL WARNING" else resilience
stress_index = 100 - resilience

# --- MATRIX 3: CHAPTER BUILDER ---
# (min resilience, tier, chapter II heart rate ceiling, Chapter I, Chapter II, Chapter III, coaching cue)
tiers = [
(80, "PRIMED", "up to 85% of max HR",
[("Diaphragmatic breathwork", 3), ("Spinal decompression", 5), ("Dynamic hip opener", 4)],
[("Dynamic warm-up flow", 5), ("Power flow: squat to lunge sequences", 12), ("Metabolic circuit, 30 sec on / 15 sec off", 10), ("Core stability series", 5), ("Active cool-down", 3)],
[("Hip and hamstring release", 5), ("Supine spinal twist", 4), ("4-7-8 breathwork", 3), ("Body scan", 3)],
"Your body is ready to work. Chapter II turns up the intensity today."),
(60, "BALANCED", "up to 75% of max HR",
[("Diaphragmatic breathwork", 3), ("Spinal decompression", 5), ("Dynamic hip opener", 4)],
[("Joint mobility warm-up", 5), ("Flow: lunge to hip-hinge sequences", 12), ("Steady metabolic circuit, 30 sec on / 30 sec off", 8), ("Core stability series", 6), ("Cool-down stretch", 4)],
[("Hip and hamstring release", 5), ("Supine spinal twist", 4), ("Box breathing", 3), ("Body scan", 3)],
"A balanced day. Chapter II holds a steady metabolic pace."),
(40, "STRAINED", "under 65% of max HR",
[("Extended-exhale breathwork", 4), ("Supported spinal decompression", 4), ("Gentle hip release", 4)],
[("Joint mobility warm-up", 5), ("Slow-tempo strength flow", 10), ("Low-impact metabolic circuit, 20 sec on / 40 sec off", 5), ("Gentle core series", 5), ("Cool-down stretch", 5)],
[("Hip and hamstring release", 5), ("Supported child's pose", 4), ("Extended-exhale breathwork", 3), ("Body scan", 3)],
"Your system is carrying some strain. Chapter II slows down and cuts the impact."),
(0, "OVERLOADED", "under 60% of max HR",
[("Extended-exhale breathwork", 5), ("Supported spinal decompression", 5), ("Gentle hip release", 5)],
[("Gentle joint mobility", 6), ("Supported mobility flow", 8), ("Breath-led core work", 3), ("Long cool-down stretch", 3)],
[("Supported hip and hamstring release", 5), ("Supported spinal twist", 4), ("Extended-exhale breathwork", 3), ("Body scan", 3)],
"Your body is asking for recovery. Today's flow is shorter and softer, but still fully guided."),
]
tier_name, hr_ceiling, ch1, ch2, ch3, cue = next((t[1], t[2], t[3], t[4], t[5], t[6]) for t in tiers if resilience >= t[0])
focus_lines = {
"PRIMED": "Resilience focus: stretch your capacity with a stress your body can absorb today.",
"BALANCED": "Resilience focus: build capacity steadily with a balanced load.",
"STRAINED": "Resilience focus: protect your baseline while you rebuild.",
"OVERLOADED": "Resilience focus: restore first. Capacity follows recovery.",
}

# Personal adjustments on top of the tier
ch1 = [("Extended-exhale breathwork", ch1[0][1])] + ch1[1:] if rhr_drift >= 5 else ch1
ch3 = ch3[:2] + [("Legs-up-the-wall sleep prep", ch3[2][1])] + ch3[3:] if sleep_debt >= 2 else ch3
adjust_notes = [msg for flag, msg in [
(rhr_drift >= 5, "Chapter I breathwork is extended because your resting heart rate is elevated."),
(sleep_debt >= 2, "Chapter III adds a legs-up-the-wall sleep prep because you are short on sleep."),
(hrv < 40, "Lower HRV shifts today's routine toward nervous system support."),
] if flag]

phase_notes = {
"Not tracking": "",
"Menstrual": "Some people find gentle hip and lower-back release especially welcome in this phase.",
"Follicular": "Many people feel energized in this phase, so Chapter II can feel extra good.",
"Ovulatory": "Take the full warm-up in Chapter II before the harder efforts.",
"Luteal": "Some people sleep lighter late in this phase, so Chapter III may help.",
}

# --- RESULTS ---
st.markdown("---")
st.markdown("### " + ("Morning, " + name.strip() + "." if name.strip() else "Good morning."))
st.caption("Body stress index: " + str(stress_index) + " (lower is calmer)")
c1, c2, c3 = st.columns(3)
c1.metric("Matrix 1: Safety", matrix_1_status)
c2.metric("Matrix 2: Resilience", str(resilience) + "/100")
c3.metric("Matrix 3: Routine", tier_name)
if safety_warnings: st.warning("\n\n".join("⚠️ " + w for w in safety_warnings))
if not safety_warnings: st.success("✅ All safety checks passed.")
st.markdown("*" + cue + "*")
st.markdown("**" + focus_lines[tier_name] + "**")

st.markdown("**TODAY'S MOVEMENT**")
numerals = ["i", "ii", "iii", "iv", "v"]
chapters = [("Chapter I: Morning Awakening", "Restorative", ch1), ("Chapter II: Peak Energy", "Metabolic flow", ch2), ("Chapter III: Evening Wind Down", "Nervous system release", ch3)]
_ = [st.expander(t + " · " + str(sum(x[1] for x in ch)) + " min · " + theme, expanded=True).markdown("\n\n".join(numerals[i] + ". " + mv + " (" + str(m) + " min)" for i, (mv, m) in enumerate(ch))) for t, theme, ch in chapters]
st.markdown("**Chapter II heart rate ceiling:** " + hr_ceiling)

if adjust_notes: st.markdown("**Personalized for you today**\n\n" + "\n".join("- " + n for n in adjust_notes))
if cycle_phase != "Not tracking": st.caption("Cycle note (" + cycle_phase + "): " + phase_notes[cycle_phase])
st.caption("Why this routine: HRV " + str(hrv) + ", RHR drift " + str(rhr_drift) + " BPM, sleep debt " + str(sleep_debt) + " h gives a resilience score of " + str(resilience) + " (" + tier_name + ").")

# --- STEP 3: RESILIENCE TREND (OPTIONAL) ---
st.markdown("---")
st.subheader("📈 Step 3: Track your resilience (optional)")
show_trend = st.checkbox("Add my last 7 days to see my resilience trend")
days = ["6 days ago", "5 days ago", "4 days ago", "3 days ago", "2 days ago", "Yesterday", "Today"]
base_df = pd.DataFrame({"Day": days, "HRV": [hrv] * 7, "RHR drift": [rhr_drift] * 7, "Sleep debt (h)": [sleep_debt] * 7})
if show_trend: st.caption("Edit each day to match your wearable. Your numbers stay in this session only.")
week = st.data_editor(base_df, hide_index=True, disabled=["Day"]) if show_trend else base_df
w_hrv = np.clip((week["HRV"].astype(float) - 20) / 80, 0, 1) * 45
w_rhr = np.clip((15 - week["RHR drift"].astype(float)) / 25, 0, 1) * 30
w_sleep = np.clip(1 - week["Sleep debt (h)"].astype(float) / 6, 0, 1) * 25
week_scores = (w_hrv + w_rhr + w_sleep).round(0)
trend = week_scores.iloc[-3:].mean() - week_scores.iloc[:3].mean()
trend_text = "n/a" if pd.isna(trend) else ("+" if trend >= 0 else "") + str(int(round(trend))) + " pts"
trend_msg = "Not enough data yet." if pd.isna(trend) else ("Trending up over this week." if trend >= 3 else ("Trending down over this week." if trend <= -3 else "Holding steady this week."))
if show_trend: st.line_chart(pd.DataFrame({"Resilience Score": week_scores.values}, index=list(range(-6, 1))))
if show_trend: st.metric("Trend: first 3 days vs last 3 days", trend_text)
if show_trend: st.caption(trend_msg + " Prototype score, not a clinical measure.")

# --- FEEDBACK ---
st.markdown("---")
st.subheader("💬 Help us improve")
st.write("Did today's routine feel right for your body? What was confusing or missing? It takes under a minute.")
if "REPLACE" not in FEEDBACK_FORM_URL: st.link_button("Give feedback", FEEDBACK_FORM_URL)
if "REPLACE" in FEEDBACK_FORM_URL: st.info("Feedback link coming soon.")
