import streamlit as st
import yfinance as yf
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setup Dashboard Look
st.set_page_config(page_title="Global Market Pulse", layout="wide")
st.title("📊 Custom Market Impact Pulse")

# --- 1. LIVE PRICES (Sidebar) ---
st.sidebar.header("Live Watchlist")

# Custom list: Gold, Silver, Oil, Crypto (Bitcoin), and Indian Stocks (Nifty 50)
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
        hist = data.history(period="5d")
        
        if not hist.empty:
            price = round(hist['Close'].iloc[-1], 2)
            # Formatting to handle crypto and index sizes cleanly
            st.sidebar.metric(label=name, value=f"{price:,.2f}")
        else:
            st.sidebar.metric(label=name, value="Market Closed")
    except Exception as e:
        st.sidebar.metric(label=name, value="Fetching...")

# --- 2. LIVE NEWS & AI SENTIMENT ---
st.subheader("🔥 Live News Impact Stream")

try:
    API_KEY = st.secrets["NEWS_API_KEY"]
    
    # NEW: Hyper-focused search query for your specific assets
    search_query = 'gold OR silver OR crypto OR "indian stock" OR "crude oil"'
    url = f"https://newsapi.org/v2/everything?q={search_query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    
    response = requests.get(url).json()
    
    if response.get("status") == "ok":
        articles = response.get("articles", [])[:10] 
        analyzer = SentimentIntensityAnalyzer()
        
        if not articles:
            st.write("No major news on these exact assets in the last few minutes. Waiting for updates...")
            
        for article in articles:
            title = article.get("title", "")
            score = analyzer.polarity_scores(title)['compound']
            
            if score > 0.1:
                impact = "🟢 GOOD IMPACT"
            elif score < -0.1:
                impact = "🔴 BAD IMPACT"
            else:
                impact = "⚪ NEUTRAL"
                
            with st.expander(f"{impact} | {title}"):
                st.write(article.get("description", "No description available."))
                st.markdown(f"**Source:** {article['source']['name']} | [Read Full Article]({article.get('url')})")
    else:
        st.error("Waiting for valid API Key...")

except Exception as e:
    st.info("System is ready! Just add your API key to Streamlit Settings to activate.")

# --- 3. AUTO REFRESH ---
st.write("⏱️ *Auto-refreshing every 60 seconds for fastest updates...*")
time.sleep(60) 
st.rerun()
