import streamlit as st
import yfinance as yf

# Setup the Dashboard Look
st.set_page_config(page_title="Global Market Pulse", layout="wide")
st.title("📊 Global Market Impact Pulse")

# Sidebar for Live Prices (Using Yahoo Finance - 100% Free, No Key Needed)
st.sidebar.header("Live Watchlist")
tickers = {"Silver (XAG)": "SI=F", "Gold (XAU)": "GC=F", "Crude Oil": "CL=F", "S&P 500": "^GSPC"}

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol)
        price = round(data.history(period="1d")['Close'].iloc[-1], 2)
        st.sidebar.metric(label=name, value=f"${price}")
    except:
        st.sidebar.metric(label=name, value="Fetching...")

# Main Dashboard Area
st.subheader("🔥 Live News Impact Stream")
st.info("System is ready. Awaiting News API Key to activate the AI Sentiment Engine...")

# Placeholder for the layout
with st.expander("[CRITICAL] Example News: Major Silver Mine Suspended"):
    st.markdown("**Impact Score:** -0.8 (RED)")
    st.write("This is how your live news will look once we connect the final piece.")
