import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# Wide-screen layout for clean viewing on iPhone
st.set_page_config(layout="wide")

st.title("🌙 Macro Decision Terminal")
st.caption("15TF Positional Execution Filter | Python Live Feed")

# --- CORE TICKER DICTIONARY ---
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

live_prices, live_changes = fetch_live_market_data()

# --- DECISION CALCULATOR ENGINE ---
nifty_move = live_changes["Nifty 50"]
bn_move    = live_changes["Bank Nifty"]
vix_move   = live_changes["India VIX"]
reliance   = live_changes["Reliance"]

banks_green_count = 0
for b in ["HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Bank"]:
    if live_changes[b] > 0:
        banks_green_count += 1

final_decision = "CHOP ZONE"
decision_color = "gray"

if abs(nifty_move) < 0.15 and abs(bn_move) < 0.15:
    final_decision = "SQUEEZE"
    decision_color = "blue"
elif bn_move < -0.6 or (nifty_move < -0.4 and vix_move > 3.0) or banks_green_count == 0:
    final_decision = "HEAVY BEARISH"
    decision_color = "red"
elif nifty_move > 0 and bn_move > 0 and reliance > 0 and banks_green_count >= 3:
    final_decision = "BULLISH"
    decision_color = "green"
else:
    final_decision = "CHOP ZONE"
    decision_color = "orange"

# --- VISIBLE DASHBOARD LAYOUT ---
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

# Create standard dataset
summary_matrix = {
    "Trading Asset": list(tickers.keys()),
    "Live Price (Rs.)": [f"{live_prices[name]:,.2f}" for name in tickers.keys()],
    "Daily Change (%)": [f"{live_changes[name]:+.2f}%" for name in tickers.keys()],
    "Status": ["BULLISH" if live_changes[name] > 0 else "BEARISH" for name in tickers.keys()]
}

df = pd.DataFrame(summary_matrix)

# --- CONDITIONAL FORMATTING ENGINE ---
def apply_status_color(row):
    color_map = []
    for val in row:
        if val == "BULLISH":
            # Bright Emerald Green background with bold black text
            color_map.append("background-color: #2ecc71; color: black; font-weight: bold;")
        elif val == "BEARISH":
            # Bright Crimson Red background with bold black text
            color_map.append("background-color: #e74c3c; color: black; font-weight: bold;")
        else:
            color_map.append("")
    return color_map

# Apply styling selectively to the 'Status' column
styled_df = df.style.apply(apply_status_color, subset=["Status"])

# Render the stylized data matrix with the index column hidden for a clean mobile look
st.dataframe(styled_df, use_container_width=True, hide_index=True)


# ==============================================================================
# NEW INTEGRATION: DIRECT NSE INSTITUTIONAL OPEN INTEREST MODULE (ALL ASSETS)
# ==============================================================================
st.markdown("---")
st.header("🛡️ Institutional Wall & Sentiment Matrix")

# Simple selector covering all assets (excluding VIX which has no options chain here)
target_options = [
    "Nifty 50", "Bank Nifty", "Reliance", "HDFC Bank", 
    "ICICI Bank", "Axis Bank", "Kotak Bank", "Divis Lab"
]
asset_choice = st.selectbox("Select Target Chain Analysis", target_options)

def display_institutional_matrix(asset_choice):
    # Map selection directly to NSE official server symbols and exact server folders
    ticker_map = {
        "Nifty 50": {"symbol": "NIFTY", "type": "indices"},
        "Bank Nifty": {"symbol": "BANKNIFTY", "type": "indices"},
        "Reliance": {"symbol": "RELIANCE", "type": "equities"},
        "HDFC Bank": {"symbol": "HDFCBANK", "type": "equities"},
        "ICICI Bank": {"symbol": "ICICIBANK", "type": "equities"},
        "Axis Bank": {"symbol": "AXISBANK", "type": "equities"},
        "Kotak Bank": {"symbol": "KOTAKBANK", "type": "equities"},
        "Divis Lab": {"symbol": "DIVISLAB", "type": "equities"}
    }
    
    asset_info = ticker_map.get(asset_choice)
    nse_symbol = asset_info["symbol"]
    nse_type = asset_info["type"]
    
    try:
        # 1. Establish a direct stealth connection to NSE Servers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }
        
        session = requests.Session()
        # Ping main page first to grab valid security session cookies
        session.get("https://www.nseindia.com", headers=headers, timeout=5)
        
        # Request live option chain data payload based on the correct asset folder
        url = f"https://www.nseindia.com/api/option-chain-{nse_type}?symbol={nse_symbol}"
        response = session.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            st.warning("NSE Live Data Server is currently congested. Tap 'Sync Market Data' to try again.")
            return
            
        raw_data = response.json()
        
        # 2. Extract active front-month expiry and parse the order book
        active_expiry = raw_data['records']['expiryDates'][0]
        options_list = [row for row in raw_data['records']['data'] if row['expiryDate'] == active_expiry]
        
        # Build clean structural matrix from the raw JSON
        parsed_data = []
        for row in options_list:
            strike = row.get('strikePrice', 0)
            ce_oi = row.get('CE', {}).get('openInterest', 0)
            pe_oi = row.get('PE', {}).get('openInterest', 0)
            parsed_data.append({'strike': strike, 'CE_OI': ce_oi, 'PE_OI': pe_oi})
            
        df = pd.DataFrame(parsed_data)
        
        # 3. Calculate Master Option Put-Call Ratio (PCR)
        total_call_oi = df['CE_OI'].sum()
        total_put_oi = df['PE_OI'].sum()
        pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0.0
        
        # Pull massive institutional absolute limit strikes
        ceiling_strike = df.loc[df['CE_OI'].idxmax()]['strike']
        floor_strike = df.loc[df['PE_OI'].idxmax()]['strike']
        
        # Translate macro ratio into your exact clean terminology rules
        if pcr >= 1.3:
            sentiment_text = "HEAVY BULL / GOING UP"
            bg_color = "#2ecc71" # Bright Neon Green
        elif pcr <= 0.7:
            sentiment_text = "HEAVY BEAR / CEILING LOCKED"
            bg_color = "#e74c3c" # Bright Neon Red
        else:
            sentiment_text = "CHOP ZONE / GOING SIDEWAYS"
            bg_color = "#f1c40f" # Bright Yellow

        # Render explicit high-visibility status box banner
        st.markdown(
            f'<div style="background-color:{bg_color}; padding:15px; border-radius:8px; text-align:center;">'
            f'<h3 style="color:black; margin:0;">SYSTEM SENTIMENT: {sentiment_text}</h3>'
            f'<p style="color:black; margin:5px 0 0 0; font-weight:bold;">Macro Put-Call Ratio (PCR): {pcr:.2f}</p>'
            f'</div>', 
            unsafe_html=True
        )
        
        # 4. Locate active Live Spot Price from the NSE data to center the grid
        underlying_price = raw_data['records']['underlyingValue']
        df['distance'] = (df['strike'] - underlying_price).abs()
        
        # Filter strictly down to the 3 absolute closest strike zones
        closest_strikes = df.nsmallest(3, 'distance').sort_values('strike')
        
        grid_data = []
        for _, row in closest_strikes.iterrows():
            strike = int(row['strike'])
            call_oi = int(row['CE_OI'])
            put_oi = int(row['PE_OI'])
            
            # Map order-book depth weightings to simplified visual states
            if call_oi > put_oi * 1.2:
                state = "HEAVY BEAR"
                action = "GOING DOWN"
                row_color = "background-color: #e74c3c; color: black; font-weight: bold;"
            elif put_oi > call_oi * 1.2:
                state = "HEAVY BULL"
                action = "GOING UP"
                row_color = "background-color: #2ecc71; color: black; font-weight: bold;"
            else:
                state = "EQUAL FIGHT"
                action = "GOING SIDEWAYS"
                row_color = ""
                
            grid_data.append({
                "Market Level (Strike)": strike,
                "Who is Defending This Wall?": state,
                "What Are They Doing Right Now?": action,
                "Raw Call Volume (OI)": f"{call_oi:,}",
                "Raw Put Volume (OI)": f"{put_oi:,}",
                "style": row_color
            })
            
        df_grid = pd.DataFrame(grid_data)
        
        # Local structural cell-color layout formatting loop
        def style_rows(row):
            return [row['style']] * len(row) if row['style'] else [''] * len(row)
            
        display_df = df_grid.drop(columns=['style'])
        
        # Display the live NSE tracked price just above the grid
        st.write(f"### 📊 Near-the-Money Strike Target Grid")
        st.caption(f"🎯 **Active Tracked Spot Price:** ₹{underlying_price:,.2f}")
        
        st.dataframe(display_df.style.apply(style_rows, axis=1), use_container_width=True, hide_index=True)
        
        # Output absolute boundary tags clearly below matrix
        st.info(f"📍 Major Absolute Roof Boundary: {int(ceiling_strike)} | 📍 Major Absolute Floor Boundary: {int(floor_strike)}")

    except Exception as e:
        st.warning("NSE Live Data Server is resetting the connection. Tap 'Sync Market Data' at the bottom to reconnect.")

# Trigger Option calculation grid render pass
display_institutional_matrix(asset_choice)

# --- MANUAL REFRESH OVERDRIVE BAR ---
st.markdown("---")
if st.button("🔄 Sync Market Data"):
    st.cache_data.clear()
    st.rerun()
