import streamlit as st
import pandas as pd
import random

# Set mobile-friendly wide layout
st.set_page_config(layout="wide")

st.title("🌙 Institutional Structure Dashboard")
st.caption("Testing Environment | 15-Minute Macro Timeframe")

# --- SECTION 1: MASTER HEALTH TOGGLE & ALERTS ---
st.sidebar.header("🎛️ Control Room")
market_status = st.sidebar.radio("Market Phase", ["Active Tracking", "No-Trade Squeeze Zone"])

if market_status == "No-Trade Squeeze Zone":
    st.error("⚠️ SYSTEM WARNING: Nifty stuck between 9 EMA & VWAP (Chop Cloud Active)")
else:
    st.success("🟢 SYSTEM READY: Volatility Expansion Active")

# --- SECTION 2: THE HEAVYWEIGHT ENGINE STATUS ---
st.header("🏢 Bank Nifty Heavyweight Drivers")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="ICICI Bank (40.3% Weight)", value="Rs. 1,120", delta="Above Daily VWAP (Bullish)")
with col2:
    st.metric(label="HDFC Bank (14.7% Weight)", value="Rs. 1,645", delta="-1.2% Below VWAP (Bearish)", delta_color="inverse")
with col3:
    st.metric(label="System Coherence (Direction)", value="COHESIVE DOWN", delta="Hedges Triggered", delta_color="off")

# --- SECTION 3: THE C, P, G, R DATA SHEET ---
st.header("📊 J 51 Whale Sentiment Logs")

# Mock data table simulating your TV indicator metrics
data = {
    "Index / Asset": ["Nifty 50", "Bank Nifty", "Reliance", "SBIN"],
    "Call Whales (C)": [14, 5, 18, 2],
    "Put Whales (P)": [3, 12, 1, 9],
    "Green Spikes (G)": [8, 2, 11, 1],
    "Red Spikes (R)": [2, 9, 0, 7],
    "Calculated Bias": ["BULLISH", "HEAVY BEARISH", "STRONG BULL", "BEARISH"]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# --- SECTION 4: LIVE INTERMARKET CORRELATION ---
st.header("🔗 Intermarket Correlation Matrix")
st.info("💡 Rule: If India VIX spikes while Bank Nifty tests a Call Floor, options premiums will expand aggressively.")

vix_slider = st.slider("Simulate India VIX Levels", min_value=10.0, max_value=25.0, value=14.5)
st.write(f"Current Simulated Risk Premium Multiplier: **{round(vix_slider / 14.5, 2)}x**")
