import streamlit as st
import yfinance as yf
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setup Dashboard Look
st.set_page_config(page_title="Global Market Pulse", layout="wide")
st.title("📊 Global Market Impact Pulse")

# --- 1. LIVE PRICES (Sidebar) ---
st.sidebar.header("Live Watchlist")
# Fixed Silver to XAG=X (Spot Silver) for reliable live data
tickers = {"Silver (XAG)": "XAG=X", "Gold (XAU)": "GC=F", "Crude Oil": "CL=F", "S&P 500": "^GSPC"}

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol)
        price = round(data.history(period="1d")['Close'].iloc[-1], 2)
        st.sidebar.metric(label=name, value=f"${price}")
    except:
        st.sidebar.metric(label=name, value="Fetching...")

# --- 2. LIVE NEWS & AI SENTIMENT ---
st.subheader("🔥 Live News Impact Stream")

try:
    # This securely pulls the key from Streamlit's hidden vault
    API_KEY = st.secrets["NEWS_API_KEY"]
    
    # Fetch latest news specifically about Silver, Gold, Oil, or Markets
    url = f"https://newsapi.org/v2/everything?q=silver OR gold OR crude oil OR global market&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url).json()
    
    if response.get("status") == "ok":
        articles = response.get("articles", [])[:10] # Gets the 10 newest articles
        analyzer = SentimentIntensityAnalyzer()
        
        for article in articles:
            title = article.get("title", "")
            # The AI Brain scores the headline
            score = analyzer.polarity_scores(title)['compound']
            
            # Decide the color and impact based on the score
            if score > 0.1:
                impact = "🟢 GOOD IMPACT"
            elif score < -0.1:
                impact = "🔴 BAD IMPACT"
            else:
                impact = "⚪ NEUTRAL"
                
            # Display the news on the screen
            with st.expander(f"{impact} | {title}"):
                st.write(article.get("description", "No description available."))
                st.markdown(f"**Source:** {article['source']['name']} | [Read Full Article]({article.get('url')})")
    else:
        st.error("Waiting for valid API Key...")

except Exception as e:
    st.info("System is ready! Just add your API key to Streamlit Settings to activate.")
