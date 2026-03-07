import streamlit as st
import yfinance as yf
import requests

st.set_page_config(page_title="Global Market Impact Pulse 2026", layout="wide")

st.title("🌍 GLOBAL MARKET IMPACT PULSE 2026")

st.subheader("📊 Live Commodity Tracker")

# Get commodity prices using yfinance
def get_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
    except:
        return "Unavailable"

col1, col2, col3 = st.columns(3)

with col1:
    gold = get_price("GC=F")
    st.metric("Gold (USD)", gold)

with col2:
    silver = get_price("SI=F")
    st.metric("Silver (USD)", silver)

with col3:
    oil = get_price("CL=F")
    st.metric("WTI Crude Oil", oil)

st.divider()

st.subheader("📰 Global Market News")

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey=037f99a875704e9e8ca788e6859a7de4"
        response = requests.get(url)
        data = response.json()
        return data["articles"]
    except:
        return []

articles = get_news()

if articles:
    for article in articles:
        st.markdown(f"### {article['title']}")
        st.write(f"Source: {article['source']['name']}")
        st.write(article["description"])
        st.markdown(f"[Read more]({article['url']})")
        st.divider()
else:
    st.warning("News data not available")
