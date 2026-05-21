import streamlit as st
import pandas as pd
import yfinance as yf

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

# Mobile Manual Overdrive
if st.button("🔄 Sync Market Data"):
    st.cache_data.clear()
    st.rerun()
    import pandas as pd
import yfinance as yf
import streamlit as st

# ==============================================================================
# 1. CORE MARKET SNAPSHOT CONFIGURATION
# ==============================================================================
st.set_page_config(page_title="Institutional Radar Dashboard", layout="wide")
st.title("📊 Alpha Matrix Control Panel")

# Core asset tracking directory
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

# Mobile Sidebar Router Selection Panel
asset_choice = st.sidebar.selectbox("Select Core Sentiment Target", ["Nifty 50", "Bank Nifty"])

# ==============================================================================
# 2. DATA ACQUISITION & MATRIX CALCULATION ENGINE
# ==============================================================================
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

# Extract math vector filters
nifty_move = changes["Nifty 50"]
bn_move    = changes["Bank Nifty"]
vix_move   = changes["India VIX"]
reliance   = changes["Reliance"]

banks_green = 0
for b in ["HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Bank"]:
    if changes[b] > 0:
        banks_green += 1

# System Logic Decision Map
if abs(nifty_move) < 0.15 and abs(bn_move) < 0.15:
    decision = "SQUEEZE"
elif bn_move < -0.6 or (nifty_move < -0.4 and vix_move > 3.0) or banks_green == 0:
    decision = "HEAVY BEARISH"
elif nifty_move > 0 and bn_move > 0 and reliance > 0 and banks_green >= 3:
    decision = "BULLISH"
else:
    decision = "CHOP ZONE"

# ==============================================================================
# 3. USER INTERFACE DISPLAY (SUMMARY CARDS & CORE TRACKING SHEET)
# ==============================================================================
st.markdown(f"### 🔥 SYSTEM FINAL DECISION: **{decision}**")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Active Green Banking Engines", value=f"{banks_green} / 4")
with col2:
    st.metric(label="India VIX Velocity Vector", value=f"{vix_move:+.2f}%")

# Main Dashboard Table Preparation
summary_matrix = {
    "Asset Name": list(tickers.keys()),
    "Live Price (Rs)": [f"{prices[name]:,.2f}" for name in tickers.keys()],
    "15M Momentum (%)": [f"{changes[name]:+.2f}%" for name in tickers.keys()],
    "State Indicator": ["BULLISH" if changes[name] > 0 else "BEARISH" for name in tickers.keys()]
}
df = pd.DataFrame(summary_matrix)

# High-Contrast Bright Neon Color Theme Engine
def apply_status_color(row):
    color_map = []
    for val in row:
        if val == "BULLISH":
            color_map.append("background-color: #2ecc71; color: black; font-weight: bold;")
        elif val == "BEARISH":
            color_map.append("background-color: #e74c3c; color: black; font-weight: bold;")
        else:
            color_map.append("")
    return color_map

st.write("### 📈 Asset Correlation Sheet")
st.dataframe(df.style.apply(apply_status_color, subset=["State Indicator"]), use_container_width=True, hide_index=True)

# ==============================================================================
# 4. UPGRADED OPEN INTEREST OVERLAY ENGINE (THE NEW SIMPLIFIED LOGIC)
# ==============================================================================
def display_institutional_matrix(asset_choice):
    st.markdown("---")
    st.write(f"### 🛡️ Institutional Wall & Sentiment Matrix ({asset_choice})")
    
    ticker_map = {
        "Nifty 50": "^NSEI",
        "Bank Nifty": "^NSEBANK"
    }
    
    target_ticker = ticker_map.get(asset_choice, "^NSEI")
    
    try:
        engine = yf.Ticker(target_ticker)
        expiries = engine.options
        
        if not expiries:
            st.info("Waiting for live option chain updates from exchange...")
            return
            
        # Harvest the front active option chain series data packet
        active_expiry = expiries[0]
        chain = engine.option_chain(active_expiry)
        calls_df = chain.calls
        puts_df = chain.puts
        
        # Calculate Option Master Put-Call Ratio (PCR)
        total_call_oi = calls_df['openInterest'].sum()
        total_put_oi = puts_df['openInterest'].sum()
        pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0.0
        
        # Identify the massive outer boundaries (Highest absolute contract strikes)
        ceiling_strike = calls_df.loc[calls_df['openInterest'].idxmax()]['strike']
        floor_strike = puts_df.loc[puts_df['openInterest'].idxmax()]['strike']
        
        # Map macro ratio to our exact simplified terminology
        if pcr >= 1.3:
            sentiment_text = "HEAVY BULL / GOING UP"
            bg_color = "#2ecc71" # Bright Emerald
        elif pcr <= 0.7:
            sentiment_text = "HEAVY BEAR / CEILING LOCKED"
            bg_color = "#e74c3c" # Bright Crimson
        else:
            sentiment_text = "CHOP ZONE / GOING SIDEWAYS"
            bg_color = "#f1c40f" # Yellow

        # Render explicit large banner container
        st.markdown(
            f'<div style="background-color:{bg_color}; padding:15px; border-radius:8px; text-align:center;">'
            f'<h3 style="color:black; margin:0;">SYSTEM SENTIMENT: {sentiment_text}</h3>'
            f'<p style="color:black; margin:5px 0 0 0; font-weight:bold;">Macro Put-Call Ratio (PCR): {pcr:.2f}</p>'
            f'</div>', 
            unsafe_html=True
        )
        
        # Filter down view to focus on the 3 strikes surrounding the active spot market
        spot_price = prices.get(asset_choice, ceiling_strike)
        calls_df['distance'] = (calls_df['strike'] - spot_price).abs()
        closest_strikes = calls_df.nsmallest(3, 'distance')['strike'].tolist()
        
        grid_data = []
        for strike in sorted(closest_strikes):
            strike_call = calls_df[calls_df['strike'] == strike]
            strike_put = puts_df[puts_df['strike'] == strike]
            
            call_oi = int(strike_call['openInterest'].iloc[0]) if not strike_call.empty else 0
            put_oi = int(strike_put['openInterest'].iloc[0]) if not strike_put.empty else 0
            
            # Map strike strength to simplified wording definitions
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
                "Market Level (Strike)": int(strike),
                "Who is Defending This Wall?": state,
                "What Are They Doing Right Now?": action,
                "Raw Call Volume (OI)": f"{call_oi:,}",
                "Raw Put Volume (OI)": f"{put_oi:,}",
                "style": row_color
            })
            
        df_grid = pd.DataFrame(grid_data)
        
        # Apply localized grid highlights
        def style_rows(row):
            return [row['style']] * len(row) if row['style'] else [''] * len(row)
            
        display_df = df_grid.drop(columns=['style'])
        st.write("### 📊 Near-the-Money Strike Target Grid")
        st.dataframe(display_df.style.apply(style_rows, axis=1), use_container_width=True, hide_index=True)
        
        # Display large absolute parameters
        st.info(f"📍 Major Absolute Roof Boundary: {int(ceiling_strike)} | 📍 Major Absolute Floor Boundary: {int(floor_strike)}")

    except:
        st.warning("Data network resting. Will synchronize automatically on next systemic refresh.")

# Execute final dashboard extension view
display_institutional_matrix(asset_choice)
