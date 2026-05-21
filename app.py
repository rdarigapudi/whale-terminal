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
    # ==============================================================================
#                 INSTITUTIONAL FLOOR & CEILING SENTIMENT ENGINE
# ==============================================================================
import datetime

def display_institutional_matrix(asset_choice):
    """
    Scans option chain matrices and displays market conditions 
    using explicit simplified structural tracking terminology.
    """
    st.markdown("---")
    st.subheader("🛡️ Institutional Wall & Sentiment Matrix")

    # Map tracking tokens cleanly
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
            
        # Extract the front active monthly expiry contract set
        active_expiry = expiries[0]
        chain = engine.option_chain(active_expiry)
        
        calls_df = chain.calls
        puts_df = chain.puts
        
        # Compute the Master Macro Sentiment Vector (PCR)
        total_call_oi = calls_df['openInterest'].sum()
        total_put_oi = puts_df['openInterest'].sum()
        pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0.0
        
        # Sort out the core macro defensive walls
        max_call_row = calls_df.loc[calls_df['openInterest'].idxmax()]
        max_put_row = puts_df.loc[puts_df['openInterest'].idxmax()]
        
        ceiling_strike = max_call_row['strike']
        floor_strike = max_put_row['strike']
        
        # Render the simplified Master Card
        if pcr >= 1.3:
            sentiment_text = "HEAVY BULL / GOING UP"
            bg_color = "#2ecc71" # Bright Emerald
            text_color = "black"
        elif pcr <= 0.7:
            sentiment_text = "HEAVY BEAR / CEILING LOCKED"
            bg_color = "#e74c3c" # Bright Crimson
            text_color = "black"
        else:
            sentiment_text = "CHOP ZONE / GOING SIDEWAYS"
            bg_color = "#f1c40f" # Yellow
            text_color = "black"
            
        st.markdown(
            f'<div style="background-color:{bg_color}; padding:15px; border-radius:8px; text-align:center;">'
            f'<h3 style="color:{text_color}; margin:0;">SYSTEM SENTIMENT: {sentiment_text}</h3>'
            f'<p style="color:{text_color}; margin:5px 0 0 0; font-weight:bold;">Macro Put-Call Ratio (PCR): {pcr:.2f}</p>'
            f'</div>', 
            unsafe_html=True
        )
        
        # Fetch underlying stock price to narrow structural strike window focus
        hist = engine.history(period="1d")
        spot_price = hist['Close'].iloc[-1] if not hist.empty else ceiling_strike
        
        # Filter down structural view to the 3 strikes closest to market center
        calls_df['distance'] = (calls_df['strike'] - spot_price).abs()
        closest_strikes = calls_df.nsmallest(3, 'distance')['strike'].tolist()
        
        grid_data = []
        for strike in sorted(closest_strikes):
            strike_call = calls_df[calls_df['strike'] == strike]
            strike_put = puts_df[puts_df['strike'] == strike]
            
            call_oi = int(strike_call['openInterest'].iloc[0]) if not strike_call.empty else 0
            put_oi = int(strike_put['openInterest'].iloc[0]) if not strike_put.empty else 0
            
            # Formulate tracking row allocations using clean terms
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
        
        # Direct CSS Row Injection formatting rule application
        def style_rows(row):
            return [row['style']] * len(row) if row['style'] else [''] * len(row)
            
        display_df = df_grid.drop(columns=['style'])
        st.write("### 📊 Near-the-Money Strike Target Grid")
        st.dataframe(
            display_df.style.apply(style_rows, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        # Print macro edge boundaries clear text alerts
        st.info(f"📍 Major Absolute Roof Boundary: {int(ceiling_strike)} | 📍 Major Absolute Floor Boundary: {int(floor_strike)}")

    except Exception as e:
        st.warning("Data network resting. Will synchronize automatically on next systemic bar frame interval update.")

# --- INJECT ROUTER TO MAIN EXECUTION CALL ---
# To finalize integration, add this line right at the very bottom of your main wrapper function:
# display_institutional_matrix(asset_choice)
