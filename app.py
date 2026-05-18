import streamlit as st
import pandas as pd
import yfinance as yf

# Wide-screen mobile optimization
st.set_page_config(layout="wide")

st.title("🌙 Institutional Live Market Feed")
st.caption("Live Feed System via yfinance Engine | 15TF Mode")

# --- DATA HARVESTING ENGINE (The Free Live Feed) ---
# Tickers used by Yahoo Finance for Indian Markets
tickers = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "ICICI Bank": "ICICIBANK.NS",
    "HDFC Bank": "HDFCBANK.NS"
}

@st.cache_data(ttl=60)  # Caches data for 60 seconds to stay fast and avoid getting blocked
def fetch_live_data():
    prices = {}
    changes = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            # Fetching today's intraday history
            hist = stock.history(period="2d", interval="15m")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = stock.info.get('previousClose', hist['Close'].iloc[0])
                pct_change = ((current_price - prev_close) / prev_close) * 100
                
                prices[name] = current_price
                changes[name] = pct_change
            else:
                prices[name] = 0.0
                changes[name] = 0.0
        except:
            prices[name] = 0.0
            changes[name] = 0.0
    return prices, changes

# Run the engine
live_prices, live_changes = fetch_live_data()

# --- REFRESH BUTTON FOR MOBILE ---
if st.button("🔄 Force Refresh Prices"):
    st.cache_data.clear()
    st.rerun()

# --- VISUAL DISPLAY 1: THE BANK NIFTY ENGINE ROOM ---
st.header("🏢 Heavyweight Sector Drivers")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="ICICI Bank (40.3% Engine Weight)", 
        value=f"Rs. {live_prices['ICICI Bank']:.2f}", 
        delta=f"{live_changes['ICICI Bank']:.2f}% Today"
    )
with col2:
    st.metric(
        label="HDFC Bank (14.7% Engine Weight)", 
        value=f"Rs. {live_prices['HDFC Bank']:.2f}", 
        delta=f"{live_changes['HDFC Bank']:.2f}% Today"
    )

# --- VISUAL DISPLAY 2: INDEX SPREADSHEET ---
st.header("📊 Macro Index Performance Status")

summary_data = {
    "Index Asset": ["Nifty 50 Index", "Bank Nifty Index"],
    "Live Trading Price": [f"Rs. {live_prices['Nifty 50']:.2f}", f"Rs. {live_prices['Bank Nifty']:.2f}"],
    "Daily Volatility Vector": [f"{live_changes['Nifty 50']:.2f}%", f"{live_changes['Bank Nifty']:.2f}%"],
    "Market Coherence Direction": [
        "BULLISH MOMENTUM" if live_changes['Nifty 50'] > 0 else "BEARISH DRIFT",
        "COHESIVE LONG" if live_changes['Bank Nifty'] > 0 else "LIQUIDITY DUMP"
    ]
}

df = pd.DataFrame(summary_data)
st.dataframe(df, use_container_width=True)

# --- STRUCTURAL TRADING LOGIC NOTE ---
st.sidebar.header("💡 Live Order Flow Analysis")
icici_change = live_changes['ICICI Bank']
hdfc_change = live_changes['HDFC Bank']

if icici_change > 0 and hdfc_change > 0:
    st.sidebar.success("🟢 BULLISH CONFIRMATION: Heavyweights are aligned. Support structures will likely hold.")
elif icici_change < 0 and hdfc_change < 0:
    st.sidebar.error("🔴 BEARISH DRIFT: Heavyweights dumping together. Do not catch falling knives at call floors.")
else:
    st.sidebar.warning("🟡 ENGINE CONFLICT: Banks fighting each other. High probability of chop inside the squeeze cloud.")
