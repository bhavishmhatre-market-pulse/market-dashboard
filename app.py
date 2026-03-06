import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. SETUP FULL-SCREEN TERMINAL LOOK
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to darken the background and remove white space
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #FFFFFF !important; }
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    /* Hide the default chart fullscreen button for a cleaner look */
    button[title="View fullscreen"] { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 GLOBAL MARKET IMPACT PULSE")
st.markdown("---")

col_left, col_right = st.columns([1.2, 2.8]) 

# --- LEFT COLUMN: PRO COMMODITY TRACKER CARDS ---
with col_left:
    st.subheader("LIVE COMMODITY TRACKER")
    
    # Custom dictionary: Ticker symbol, Icon, and Chart Color matching your image
    tickers = {
        "SILVER (XAG/USD)": {"symbol": "SI=F", "icon": "🪙", "color": "#28a745"},  # Green
        "GOLD (XAU/USD)": {"symbol": "GC=F", "icon": "🥇", "color": "#ffc107"},   # Yellow/Gold
        "WTI CRUDE": {"symbol": "CL=F", "icon": "🛢️", "color": "#28a745"},       # Green
        "BITCOIN (BTC)": {"symbol": "BTC-USD", "icon": "₿", "color": "#fd7e14"}, # Orange
        "NIFTY 50": {"symbol": "^NSEI", "icon": "📈", "color": "#0dcaf0"}        # Blue
    }

    for name, info in tickers.items():
        try:
            data = yf.Ticker(info["symbol"])
            hist = data.history(period="14d") # 14 days makes a better looking mini-chart
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                # Format price (Add Rupees for Nifty)
                price_str = f"${current_price:,.2f}" if "NIFTY" not in name else f"₹{current_price:,.2f}"
                
                # Calculate Bullish/Bearish Badge styling
                if pct_change > 0.1:
                    sentiment = "Bullish"
                    badge_bg = "rgba(40, 167, 69, 0.2)"
                    text_color = "#28a745" # Green
                    arrow = "▲"
                elif pct_change < -0.1:
                    sentiment = "Bearish"
                    badge_bg = "rgba(220, 53, 69, 0.2)"
                    text_color = "#dc3545" # Red
                    arrow = "▼"
                else:
                    sentiment = "Neutral"
                    badge_bg = "rgba(108, 117, 125, 0.2)"
                    text_color = "#adb5bd" # Gray
                    arrow = "▬"

                # CUSTOM HTML CARD DESIGN (Mimicking the uploaded picture)
                card_html = f"""
                <div style="background-color: #1A1C24; padding: 15px 15px 5px 15px; border-radius: 10px 10px 0 0; border: 1px solid #2E3038; border-bottom: none; margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #FFFFFF; font-weight: bold; font-size: 16px;">{info['icon']} {name}</span>
                        <span style="background-color: {badge_bg}; color: {text_color}; padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: bold;">{sentiment}</span>
                    </div>
                    <div style="margin-top: 10px;">
                        <span style="color: #FFFFFF; font-size: 28px; font-weight: bold;">{price_str}</span>
                    </div>
                    <div style="margin-top: 2px;">
                        <span style="color: {text_color}; font-size: 14px; font-weight: bold;">{arrow} {pct_change:+.2f}%</span>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Filled Area Chart underneath the card text
                st.area_chart(hist['Close'], color=info["color"], height=120, use_container_width=True)
                
            else:
                st.write(f"**{name}**: Market Closed / Fetching...")
        except Exception as e:
            st.write(f"**{name}**: Error Loading Data")


# --- RIGHT COLUMN: NEWS IMPACT STREAM ---
with col_right:
    st.subheader("🔥 NEWS IMPACT STREAM (Fastest Updates)")
    
    asset_keywords = {
        "Gold": ["gold", "xau", "bullion", "precious metal"],
        "Silver": ["silver", "xag"],
        "Crude Oil": ["oil", "crude", "wti", "brent", "opec", "energy"],
        "Crypto": ["crypto", "bitcoin", "btc", "ethereum", "eth"],
        "Indian Stocks": ["nifty", "sensex", "indian stock", "nse", "bse", "rbi"]
    }

    def identify_asset(text):
        text_lower = text.lower()
        impacted_assets = []
        for asset, keywords in asset_keywords.items():
            if any(word in text_lower for word in keywords):
                impacted_assets.append(asset)
        return impacted_assets

    try:
        API_KEY = st.secrets["NEWS_API_KEY"]
        search_query = '("gold price" OR "silver price" OR bitcoin OR cryptocurrency OR "crude oil" OR "nifty 50" OR sensex)'
        url = f"https://newsapi.org/v2/everything?q={search_query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
        
        response = requests.get(url).json()
        
        if response.get("status") == "ok":
            raw_articles = response.get("articles", [])
            analyzer = SentimentIntensityAnalyzer()
            valid_articles_displayed = 0
            
            for article in raw_articles:
                if valid_articles_displayed >= 10: break
                    
                title = article.get("title", "")
                desc = article.get("description", "")
                full_text = f"{title} {desc}"
                
                impacted_assets = identify_asset(full_text)
                if not impacted_assets: continue
                valid_articles_displayed += 1
                
                asset_tag = f"[{', '.join(impacted_assets)}]"
                score = analyzer.polarity_scores(title)['compound']
                
                # UI DESIGN: Custom Colored Alert Boxes for News
                if score > 0.1:
                    border_color = "#00FF00" # Neon Green
                    impact_text = f"🟢 GOOD IMPACT: {asset_tag}"
                elif score < -0.1:
                    border_color = "#FF0000" # Neon Red
                    impact_text = f"🚨 CRITICAL ALERT: {asset_tag}"
                else:
                    border_color = "#888888" # Gray
                    impact_text = f"⚪ NEUTRAL: {asset_tag}"
                    
                card_html = f"""
                <div style="border: 1px solid {border_color}; border-left: 8px solid {border_color}; background-color: #1A1C24; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                    <h4 style="color: white; margin-top: 0; font-family: sans-serif;">{impact_text}</h4>
                    <h5 style="color: #E0E0E0; margin-bottom: 10px;">{title}</h5>
                    <p style="color: #A0A0A0; font-size: 14px;">{desc}</p>
                    <span style="color: #666666; font-size: 12px;">Source: {article['source']['name']} | Score: {score}</span>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
            if valid_articles_displayed == 0:
                st.write("Monitoring wires for highly relevant market news...")
                
        else:
            st.error("News API Error: Please check your API Key limits.")

    except Exception as e:
        st.info("System is ready! Awaiting API Key connection.")

# --- AUTO REFRESH ---
st.write("⏱️ *Auto-refreshing every 60 seconds...*")
time.sleep(60) 
st.rerun()
