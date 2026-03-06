import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. SETUP FULL-SCREEN TERMINAL LOOK
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to make it look like a trading terminal
st.markdown("""
    <style>
    /* Darken the background and make text pop */
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #FFFFFF !important; }
    
    /* Remove padding to make it wide like a monitor */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 GLOBAL MARKET IMPACT PULSE 2026")
st.markdown("---")

# 2. CREATE SPLIT SCREEN (Left: Prices, Right: News)
col_left, col_right = st.columns([1.2, 2.8]) # Left column is narrower

# --- LEFT COLUMN: LIVE COMMODITY TRACKER ---
with col_left:
    st.subheader("📈 LIVE COMMODITY TRACKER")
    
    tickers = {
        "Silver (XAG/USD)": "SI=F", 
        "Gold (XAU/USD)": "GC=F", 
        "WTI Crude Oil": "CL=F",
        "Bitcoin (BTC)": "BTC-USD",
        "Nifty 50 (India)": "^NSEI"
    }

    for name, symbol in tickers.items():
        try:
            data = yf.Ticker(symbol)
            hist = data.history(period="7d") # Get 7 days for the mini-chart
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                # Format price and change
                price_str = f"${current_price:,.2f}" if "Nifty" not in name else f"₹{current_price:,.2f}"
                delta_color = "normal" if pct_change >= 0 else "inverse"
                
                # Display the Metric
                st.metric(label=name, value=price_str, delta=f"{pct_change:.2f}%", delta_color=delta_color)
                
                # Display the "Sparkline" trend chart
                st.line_chart(hist['Close'], height=120)
                st.markdown("<br>", unsafe_allow_html=True) # Add some spacing
            else:
                st.metric(label=name, value="Market Closed")
        except Exception as e:
            st.metric(label=name, value="Fetching...")


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
                
                # UI DESIGN: Custom Colored Alert Boxes
                if score > 0.1:
                    border_color = "#00FF00" # Neon Green
                    impact_text = f"🟢 GOOD IMPACT: {asset_tag}"
                elif score < -0.1:
                    border_color = "#FF0000" # Neon Red
                    impact_text = f"🚨 CRITICAL ALERT: {asset_tag}"
                else:
                    border_color = "#888888" # Gray
                    impact_text = f"⚪ NEUTRAL: {asset_tag}"
                    
                # The Custom HTML/CSS Card for each news item
                card_html = f"""
                <div style="border: 1px solid {border_color}; border-left: 8px solid {border_color}; background-color: #1E1E1E; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
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
