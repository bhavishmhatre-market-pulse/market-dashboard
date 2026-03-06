import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Force Dark Mode and Wide Layout
st.set_page_config(page_title="Global Market Pulse", layout="wide", initial_sidebar_state="expanded")

st.title("📊 Custom Market Impact Pulse")

# --- 1. LIVE PRICES & MINI CHARTS (Sidebar) ---
st.sidebar.header("Live Watchlist")

tickers = {
    "Gold (XAU)": "GC=F", 
    "Silver (XAG)": "SI=F", 
    "Crude Oil": "CL=F",
    "Bitcoin (BTC)": "BTC-USD",
    "Nifty 50 (India)": "^NSEI"
}

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol)
        # Pulling 7 days of data so we have a nice line chart to look at
        hist = data.history(period="7d")
        
        if not hist.empty:
            price = round(hist['Close'].iloc[-1], 2)
            # Calculate difference to show red/green
            prev_price = round(hist['Close'].iloc[-2], 2)
            delta = round(price - prev_price, 2)
            
            # Show the price and the green/red change indicator
            st.sidebar.metric(label=name, value=f"{price:,.2f}", delta=f"{delta}")
            
            # Show the mini line chart!
            st.sidebar.line_chart(hist['Close'], height=120)
        else:
            st.sidebar.metric(label=name, value="Market Closed")
    except Exception as e:
        st.sidebar.metric(label=name, value="Fetching...")

# --- 2. ASSET KEYWORDS (The Strict Filter) ---
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

# --- 3. LIVE NEWS & AI SENTIMENT ---
st.subheader("🔥 Live News Impact Stream")

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
            
            if score > 0.1: impact = f"🟢 GOOD for {asset_tag}"
            elif score < -0.1: impact = f"🔴 BAD for {asset_tag}"
            else: impact = f"⚪ NEUTRAL for {asset_tag}"
                
            with st.expander(f"{impact} | {title}"):
                st.write(desc)
                st.markdown(f"**Source:** {article['source']['name']} | [Read Full Article]({article.get('url')})")
                
        if valid_articles_displayed == 0:
            st.write("No highly relevant market news found in the last few minutes. Waiting for the next cycle...")
    else:
        st.error("Waiting for valid API Key or API limit reached...")

except Exception as e:
    st.info("System is ready! Just add your API key to Streamlit Settings to activate.")

# --- 4. AUTO REFRESH ---
st.write("⏱️ *Auto-refreshing every 60 seconds...*")
time.sleep(60) 
st.rerun()
