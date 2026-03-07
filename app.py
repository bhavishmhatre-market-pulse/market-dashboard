import streamlit as st
import yfinance as yf
import requests
import time
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- 1. SETUP TERMINAL THEME ---
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #12141A; } 
    h1, h2, h3, h4, h5, p, span { font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; }
    .block-container { padding-top: 1.5rem; }
    .stPlotlyChart { margin-top: -20px; margin-bottom: -10px; }
    .header-glow { color: white; font-weight: 800; font-size: 24px; letter-spacing: 1px; }
    .live-feed-btn {
        background-color: rgba(0, 255, 127, 0.1); border: 1px solid #00FF7F;
        color: #00FF7F; padding: 4px 12px; border-radius: 15px; font-size: 12px;
        font-weight: bold; float: right; margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #30363D; padding-bottom: 10px; margin-bottom: 20px;">
        <span class="header-glow">GLOBAL MARKET IMPACT PULSE 2026</span>
        <span class="live-feed-btn">● LIVE DATA FEED</span>
    </div>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color, opacity=0.1):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {opacity})"


# ==========================================
# --- TOP ROW: HORIZONTAL TRACKER BAR ---
# ==========================================
st.markdown("<h4 style='color: #8B949E; font-size: 14px; margin-bottom: 15px;'>📡 LIVE COMMODITY TRACKER</h4>", unsafe_allow_html=True)

# Splits the top of the screen into 4 equal horizontal columns
col1, col2, col3, col4 = st.columns(4)

assets = [
    {"name": "SILVER (XAG)", "ticker": "SI=F", "icon": "🥈", "color": "#00FF7F", "col": col1}, 
    {"name": "GOLD (XAU)", "ticker": "GC=F", "icon": "🟡", "color": "#FFD700", "col": col2},   
    {"name": "WTI CRUDE", "ticker": "CL=F", "icon": "🛢️", "color": "#00FF7F", "col": col3},       
    {"name": "NIFTY 50", "ticker": "^NSEI", "icon": "🇮🇳", "color": "#00BFFF", "col": col4}        
]

for info in assets:
    with info["col"]:
        try:
            ticker_data = yf.Ticker(info["ticker"])
            hist = ticker_data.history(period="1d", interval="15m")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                if pct_change > 0:
                    status, label_color = "Bullish", "#00FF7F"
                elif pct_change < 0:
                    status, label_color = "Bearish", "#FF4B4B"
                else:
                    status, label_color = "Neutral", "#AAAAAA"
                    
                bg_color = hex_to_rgba(label_color, 0.15)
                price_str = f"₹{current_price:,.2f}" if "NIFTY" in info["name"] else f"${current_price:,.2f}"

                # Compact Horizontal Card Design
                st.markdown(f"""
                <div style="background-color: #1A1D24; border: 1px solid #2A2E39; border-bottom: none; border-radius: 8px 8px 0 0; padding: 15px 15px 0 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #FFFFFF; font-size: 12px; font-weight: 700;">{info['icon']} {info['name']}</span>
                        <span style="background-color: {bg_color}; color: {label_color}; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">{status}</span>
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="color: white; font-size: 20px; font-weight: bold;">{price_str}</span>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <span style="color: {label_color}; font-size: 12px; font-weight: bold;">{'▲' if pct_change > 0 else '▼'} {pct_change:+.2f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Mini Plotly Chart
                fig = go.Figure(go.Scatter(
                    x=hist.index, y=hist['Close'], mode='lines',
                    line=dict(color=info["color"], width=2),
                    fill='tozeroy', fillcolor=hex_to_rgba(info["color"], 0.1) 
                ))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0), height=50,
                    paper_bgcolor='#1A1D24', plot_bgcolor='#1A1D24',
                    xaxis=dict(showgrid=False, zeroline=False, visible=False), 
                    yaxis=dict(showgrid=False, zeroline=False, visible=False), showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown("""<div style="border-top: 1px solid #2A2E39; margin-bottom: 20px; margin-top: -10px;"></div>""", unsafe_allow_html=True)
        except:
            st.write("Loading Data...")


# ==========================================
# --- ASSET IDENTIFIER AI FUNCTION ---
# ==========================================
def get_impacted_asset(text):
    text = text.lower()
    if "gold" in text or "bullion" in text: return "GOLD"
    if "silver" in text: return "SILVER"
    if "oil" in text or "crude" in text or "opec" in text: return "CRUDE OIL"
    if "nifty" in text or "sensex" in text or "india" in text: return "INDIAN STOCKS"
    return "GLOBAL MARKETS"


# ==========================================
# --- BOTTOM ROW: NEWS PREDICTIONS ---
# ==========================================
st.markdown("<h4 style='color: #8B949E; font-size: 14px; margin-bottom: 15px;'>🔥 AI NEWS IMPACT PREDICTIONS</h4>", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["NEWS_API_KEY"]
    search_query = '("gold price" OR "silver price" OR "crude oil" OR "nifty 50" OR sensex)'
    url = f"https://newsapi.org/v2/everything?q={search_query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    
    news = requests.get(url).json().get("articles", [])[:6] 
    
    analyzer = SentimentIntensityAnalyzer()
    for art in news:
        title = art.get('title', '')
        desc = art.get('description', '')
        full_text = f"{title} {desc}"
        
        # 1. Score the sentiment
        score = analyzer.polarity_scores(title)['compound']
        
        # 2. Identify the asset
        asset = get_impacted_asset(full_text)
        
        # 3. Calculate the estimated percentage impact (Scaling score to a max ~2.5% daily move)
        impact_pct = round(score * 2.5, 2)
        
        if score > 0.1:
            color, tag, text_color = "#00FF7F", "[BULLISH]", "#00FF7F"
            impact_text = f"Expected Impact: +{abs(impact_pct)}% surge on {asset} chart"
        elif score < -0.1:
            color, tag, text_color = "#FF4B4B", "[BEARISH]", "#FF4B4B"
            impact_text = f"Expected Impact: -{abs(impact_pct)}% drop on {asset} chart"
        else:
            color, tag, text_color = "#AAAAAA", "[NEUTRAL]", "#AAAAAA"
            impact_text = f"Expected Impact: Minimal volatility on {asset} chart"
            
        box_shadow = f"0px 0px 15px {hex_to_rgba(color, 0.4)}" 
        
        st.markdown(f"""
        <div style="background-color: #1A1D24; border: 1px solid {color}; box-shadow: {box_shadow}; border-radius: 6px; padding: 15px; margin-bottom: 15px;">
            <h5 style="margin: 0 0 10px 0; color: white; font-size: 14px; display: flex; align-items: center;">
                <span style="color: {text_color}; font-weight: bold; margin-right: 8px;">{tag}</span> 
                {title.upper()}
            </h5>
            <p style="font-size: 13px; color: {text_color}; margin: 0 0 5px 0;"><strong>{impact_text}</strong></p>
            <p style="font-size: 12px; color: #8B949E; margin: 0 0 5px 0;">• Impact Confidence Score: {round(abs(score) * 10, 1)}/10</p>
            <p style="font-size: 12px; color: #8B949E; margin: 0;">• Source: {art['source']['name']}</p>
        </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.info("Awaiting News Feed...")

# AUTO REFRESH
time.sleep(60)
st.rerun()
