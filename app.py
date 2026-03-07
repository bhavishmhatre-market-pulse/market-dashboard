import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. TERMINAL UI SETUP
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0B0C10; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem; }
    /* This hides the plain gray background behind the sharp lines */
    [data-testid="stMetricDelta"] svg { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("GLOBAL MARKET IMPACT PULSE 2026")

# Setting up the columns correctly to fix the error
col_left, col_right = st.columns([1, 2.5])

# --- LEFT COLUMN: SHARP PRO TRACKER ---
with col_left:
    st.markdown("### LIVE COMMODITY TRACKER")
    
    assets = {
        "SILVER (XAG/USD)": {"ticker": "SI=F", "icon": "🥈", "color": "#00FF7F"}, 
        "GOLD (XAU/USD)": {"ticker": "GC=F", "icon": "🟡", "color": "#FFD700"},   
        "WTI CRUDE": {"ticker": "CL=F", "icon": "🛢️", "color": "#00FF7F"},       
        "BITCOIN (BTC)": {"ticker": "BTC-USD", "icon": "₿", "color": "#FF8C00"}, 
        "NIFTY 50": {"ticker": "^NSEI", "icon": "🇮🇳", "color": "#00BFFF"}        
    }

    for name, info in assets.items():
        try:
            ticker_data = yf.Ticker(info["ticker"])
            # 15m intervals create that "Sharp Pulse" look
            hist = ticker_data.history(period="1d", interval="15m")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                status, label_color = ("Bullish", "#00FF7F") if pct_change > 0 else ("Bearish", "#FF4B4B")
                bg_color = f"rgba({0 if pct_change > 0 else 255}, {255 if pct_change > 0 else 75}, {127 if pct_change > 0 else 75}, 0.1)"

                # The Card Layout
                st.markdown(f"""
                <div style="background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 12px; margin-bottom: -5px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #8B949E; font-size: 11px; font-weight: bold;">{info['icon']} {name}</span>
                        <span style="background-color: {bg_color}; color: {label_color}; padding: 1px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">{status}</span>
                    </div>
                    <div style="margin: 2px 0;">
                        <span style="color: white; font-size: 24px; font-weight: bold;">${current_price:,.2f}</span>
                    </div>
                    <div style="color: {label_color}; font-size: 13px; font-weight: bold;">
                        {'▲' if pct_change > 0 else '▼'} {pct_change:+.2f}% <span style="color: #555; font-size: 10px; margin-left: 5px;">24H Pulse</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # SHARP LINE CHART (No plain fill)
                st.line_chart(hist['Close'], color=info["color"], height=100, use_container_width=True)
        except:
            st.error(f"Syncing {name}...")

# --- RIGHT COLUMN: NEWS FEED ---
with col_right:
    st.markdown("### NEWS IMPACT STREAM")
    try:
        API_KEY = st.secrets["NEWS_API_KEY"]
        url = f"https://newsapi.org/v2/everything?q=(gold OR silver OR bitcoin OR nifty OR oil)&language=en&sortBy=publishedAt&apiKey={API_KEY}"
        news = requests.get(url).json().get("articles", [])[:8]
        
        analyzer = SentimentIntensityAnalyzer()
        for art in news:
            score = analyzer.polarity_scores(art['title'])['compound']
            color = "#00FF7F" if score > 0.1 else "#FF4B4B" if score < -0.1 else "#8B949E"
            
            st.markdown(f"""
            <div style="border-left: 5px solid {color}; background-color: #161B22; padding: 15px; border-radius: 0 8px 8px 0; margin-bottom: 10px; border: 1px solid #30363D;">
                <h5 style="margin: 0; color: white;">{art['title']}</h5>
                <p style="font-size: 12px; color: #8B949E; margin: 5px 0;">Source: {art['source']['name']}</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.info("Awaiting News Feed...")

# AUTO-REFRESH
time.sleep(60)
st.rerun()
