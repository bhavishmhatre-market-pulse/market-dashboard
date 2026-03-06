import streamlit as st
import yfinance as yf
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setup Dashboard Look
st.set_page_config(page_title="Global Market Pulse", layout="wide")
st.title("📊 Global Market Impact Pulse")

# --- 1. LIVE PRICES (Sidebar) ---
st.sidebar.header("Live Watchlist")

# We will use SI=F (Silver Futures) as it is generally the most stable free ticker
tickers = {"Silver (XAG)": "SI=F", "Gold (XAU)": "GC=F", "Crude Oil": "CL=F", "S&P 500": "^GSPC"}

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol)
        # CHANGED: Pull 5 days of data to guarantee we don't get a blank page
        hist = data.history(period="5d")
        
        if not hist.empty:
            price = round(hist['Close'].iloc[-1], 2)
            st.sidebar.metric(label=name, value=f"${price}")
        else:
            st.sidebar.metric(label=name, value="Market Closed")
    except Exception as e:
        st.sidebar.metric(label=name, value="Fetching...")

# --- 2. LIVE NEWS & AI SENTIMENT ---
st.subheader("🔥 Live News Impact Stream")

try:
    API_KEY = st.secrets["NEWS_API_KEY"]
    
    url = f"https://newsapi.org/v2/everything?q=silver OR gold OR crude oil OR global market&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url).json()
    
    if response.get("status") == "ok":
        articles = response.get("articles", [])[:10] 
        analyzer = SentimentIntensityAnalyzer()
        
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
