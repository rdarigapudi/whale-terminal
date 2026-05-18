import streamlit as st
import pandas as pd
import yfinance as yf

# Wide-screen layout for clean viewing on iPhone
st.set_page_config(layout="wide")

st.title("🌙 Macro Decision Terminal")
st.caption("15TF Positional Execution Filter | Python Live Feed")

# --- CORE TICKER DICTIONARY ---
# Mapping your precise watchlist to Yahoo Finance codes
tickers = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "Reliance": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Axis Bank": "AXISBANK.NS",
    "Kotak Bank": "KOTAKBANK.NS",
    "Divis Lab": "DIVISLAB.NS",
    "India VIX": "^INDIAVIX"
}

@st.cache_data(ttl=60)  # Refresh cache every 60 seconds
def fetch_live_market_data():
    prices = {}
    changes = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d", interval="15m")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = stock.info.get('previousClose', hist['Close'].iloc[0])
                pct_change = ((current_price - prev_close) / prev_close) * 100
                
                prices[name] = current_price
                changes[name] = pct_change
            else:
                prices[name], changes[name] = 0.0, 0.0
        except:
            prices[name], changes[name] = 0.0, 0.0
    return prices, changes

# Harvest active prices and metrics
live_prices, live_changes = fetch_live_market_data()

# --- DECISION CALCULATOR ENGINE ---
nifty_move = live_changes["Nifty 50"]
bn_move    = live_changes["Bank Nifty"]
vix_move   = live_changes["India VIX"]
reliance   = live_changes["Reliance"]

# Track how many of the 4 big banks are trading green today
banks_green_count = 0
for b in ["HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Bank"]:
    if live_changes[b] > 0:
        banks_green_count += 1

# Algorithmic Checklist mapping to your specific terms
final_decision = "CHOP ZONE"
decision_color = "gray"

# 1. Check for Squeeze (Volatility exceptionally tight)
if abs(nifty_move) < 0.15 and abs(bn_move) < 0.15:
    final_decision = "SQUEEZE"
    decision_color = "blue"
# 2. Check for Heavy Bearish (Index dropping + VIX inflating or heavy bank breakdown)
elif bn_move < -0.6 or (nifty_move < -0.4 and vix_move > 3.0) or banks_green_count == 0:
    final_decision = "HEAVY BEARISH"
    decision_color = "red"
# 3. Check for Bullish (Indices positive + main drivers supportive)
elif nifty_move > 0 and bn_move > 0 and reliance > 0 and banks_green_count >= 3:
    final_decision = "BULLISH"
    decision_color = "green"
# 4. Fallback to default if trends conflict
else:
    final_decision = "CHOP ZONE"
    decision_color = "orange"

# --- VISIBLE DASHBOARD LAYOUT ---
# High Visibility Top Box for rapid iPhone tracking
st.header("⚡ Core Execution Summary")
k1, k2, k3 = st.columns(3)

with k1:
    if decision_color == "green":
        st.success(f"🔥 FINAL DECISION: {final_decision}")
    elif decision_color == "red":
        st.error(f"🛑 FINAL DECISION: {final_decision}")
    elif decision_color == "blue":
        st.info(f"⚡ FINAL DECISION: {final_decision} (Prepare for Breakout)")
    else:
        st.warning(f"⚠️ FINAL DECISION: {final_decision} (Stay Cash)")

with k2:
    st.metric(label="Nifty Position Direction", value=f"{nifty_move:.2f}%", delta="Bullish Edge" if nifty_move > 0 else "Bearish Pressure")
with k3:
    st.metric(label="Bank Performance Index", value=f"{bn_move:.2f}%", delta=f"{banks_green_count}/4 Banks Green")

st.markdown("---")

# --- COMPLETE WATCHLIST SPREADSHEET ---
st.header("📊 Asset Correlation Sheet")

summary_matrix = {
    "Trading Asset": list(tickers.keys()),
    "Live Price (Rs.)": [f"{live_prices[name]:,.2f}" for name in tickers.keys()],
    "Daily Change (%)": [f"{live_changes[name]:+.2f}%" for name in tickers.keys()],
    "Status": [
        "BULLISH" if live_changes[name] > 0 else "BEARISH" for name in tickers.keys()
    ]
}

df = pd.DataFrame(summary_matrix)
st.dataframe(df, use_container_width=True)

# Mobile Manual Overdrive
if st.button("🔄 Sync Market Data"):
    st.cache_data.clear()
    st.rerun()
