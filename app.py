import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. SETUP FULL-SCREEN TERMINAL LOOK
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for the "Deep Dark" terminal theme
st.markdown("""
    <style>
    .stApp { background-color: #0B0C10; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem; }
    /* Hide default chart buttons for a cleaner look */
    button[title="View fullscreen"] { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 GLOBAL MARKET IMPACT PULSE 2026")

col_left, col_right = st.columns([1, 2.5])

# --- LEFT COLUMN: LIVE PRO TRACKER (24HR GRAPHS) ---
with col_left:
    st.markdown("### LIVE COMMODITY TRACKER")
    
    # Asset configuration matching your image colors
    assets = {
        "SILVER (XAG/USD)": {"ticker": "SI=F", "icon": "🥈", "color": "#00FF7F"}, 
        "GOLD (XAU/USD)": {"ticker": "GC=F", "icon": "🟡", "color": "#FFD700"},   
        "WTI CRUDE": {"ticker": "CL=F", "icon": "🛢️", "color": "#00FF7F"},       
        "BITCOIN (BTC)": {"ticker": "BTC-USD", "icon": "₿", "color": "#FF8C00"}, 
        "NIFTY 50": {"ticker": "^NSEI", "icon": "🇮🇳", "color": "#00BFFF"}        
    }

    for name, info in assets.items():
        try:
            # Fetching 24-hour data at 1-hour intervals for the sparkline
            ticker_data = yf.Ticker(info["ticker"])
            hist = ticker_data.history(period="1d", interval="1h")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                # Determine Sentiment Label colors
                status, label_color = ("Bullish", "#00FF7F") if pct_change > 0 else ("Bearish", "#FF4B4B")
                bg_color = f"rgba({0 if pct_change > 0 else 255}, {255 if pct_change > 0 else 75}, {127 if pct_change > 0 else 75}, 0.1)"

                # THE EXACT UI CARD LAYOUT
                st.markdown(f"""
                <div style="background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 12px; margin-bottom: -10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #8B949E; font-size: 12px; font-weight: bold;">{info['icon']} {name}:</span>
                        <span style="background-color: {bg_color}; color: {label_color}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">{status}</span>
                    </div>
                    <div style="margin: 5px 0;">
                        <span style="color: white; font-size: 26px; font-weight: bold;">${current_price:,.2f}</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="color: {label_color}; font-size: 14px; font-weight: bold;">{'▲' if pct_change > 0 else '▼'} {pct_change:+.2f}%</span>
                        <span style="color: #8B949E; font-size: 10px; margin-left: 10px; background-color: #21262D; padding: 2px 5px; border-radius: 3px;">24H Trend</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 24HR FILLED AREA GRAPH
                st.area_chart(hist['Close'], color=info["color"], height=100, use_container_width=True)
        except:
            st.error(f"Error loading {name}")

# --- RIGHT COLUMN: NEWS IMPACT STREAM ---
with col_right:
    st.markdown("### NEWS IMPACT STREAM")
    try:
        API_KEY = st.secrets["NEWS_API_KEY"]
        url = f"https://newsapi.org/v2/everything?q=(gold OR silver OR bitcoin OR nifty OR oil)&language=en&sortBy=publishedAt&apiKey={API_KEY}"
        news = requests.get(url).json().get("articles", [])[:10]
        
        analyzer = SentimentIntensityAnalyzer()
        for art in news:
            score = analyzer.polarity_scores(art['title'])['compound']
            color = "#00FF7F" if score > 0.1 else "#FF4B4B" if score < -0.1 else "#8B949E"
            impact_tag = "🟢 GOOD IMPACT" if score > 0.1 else "🔴 BAD IMPACT" if score < -0.1 else "⚪ NEUTRAL"
            
            st.markdown(f"""
            <div style="border-left: 5px solid {color}; background-color: #161B22; padding: 15px; border-radius: 0 8px 8px 0; margin-bottom: 12px; border: 1px solid #30363D;">
                <h6 style="color: {color}; margin: 0;">{impact_tag}</h6>
                <h5 style="margin: 5px 0; color: white;">{art['title']}</h5>
                <p style="font-size: 13px; color: #8B949E; margin: 0;">Source: {art['source']['name']} | 24H Pulse Active</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.info("Awaiting Live News Feed...")

# AUTO-REFRESH SCRIPT
time.sleep(60)
st.rerun()
