import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. SETUP TERMINAL UI
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for the "Deep Dark" theme
st.markdown("""
    <style>
    .stApp { background-color: #0B0C10; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem; }
    [data-testid="stMetricDelta"] svg { display: none; } /* Hide default arrows */
    </style>
""", unsafe_allow_html=True)

st.title("GLOBAL MARKET IMPACT PULSE 2026")

col_left, col_right = st.columns([1, 2.5])

# --- LEFT COLUMN: LIVE COMMODITY TRACKER (EXACT MATCH) ---
with col_left:
    st.markdown("### LIVE COMMODITY TRACKER")
    
    # Asset configuration matching your image
    assets = {
        "SILVER (XAG/USD)": {"ticker": "SI=F", "icon": "🥈", "color": "#00FF7F"}, # Neon Green
        "GOLD (XAU/USD)": {"ticker": "GC=F", "icon": "🟡", "color": "#FFD700"},   # Gold
        "WTI CRUDE": {"ticker": "CL=F", "icon": "🛢️", "color": "#00FF7F"},       # Neon Green
        "BITCOIN (BTC)": {"ticker": "BTC-USD", "icon": "₿", "color": "#FF8C00"}, # Orange
        "NIFTY 50": {"ticker": "^NSEI", "icon": "🇮🇳", "color": "#00BFFF"}        # Blue
    }

    for name, info in assets.items():
        try:
            # Fetching 24-hour data at 1-hour intervals for the graph
            ticker_data = yf.Ticker(info["ticker"])
            hist = ticker_data.history(period="1d", interval="1h")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                # Determine Sentiment Label
                if pct_change > 0:
                    status, label_color, bg_color = "Bullish", "#00FF7F", "rgba(0, 255, 127, 0.1)"
                else:
                    status, label_color, bg_color = "Bearish", "#FF4B4B", "rgba(255, 75, 75, 0.1)"

                # THE EXACT WORDING & CARD LAYOUT
                st.markdown(f"""
                <div style="background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 12px; margin-bottom: -10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #8B949E; font-size: 12px; font-weight: bold;">{info['icon']} {name}:</span>
                        <span style="background-color: {bg_color}; color: {label_color}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">{status}</span>
                    </div>
                    <div style="margin: 5px 0;">
                        <span style="color: white; font-size: 24px; font-weight: bold;">${current_price:,.2f}</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="color: {label_color}; font-size: 14px; font-weight: bold;">▲ {pct_change:+.1f}%</span>
                        <span style="color: #8B949E; font-size: 10px; margin-left: 10px; background-color: #21262D; padding: 2px 5px; border-radius: 3px;">{status}</span>
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
    # (Keeping your existing news logic here to ensure the "fastest updates" you requested)
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

# AUTO-REFRESH SCRIPT
time.sleep(60)
st.rerun()
