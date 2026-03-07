import streamlit as st
import requests

st.set_page_config(page_title="Global Market Impact Pulse 2026", layout="wide")

st.title("🌍 GLOBAL MARKET IMPACT PULSE 2026")

st.subheader("📊 Live Commodity Tracker")

# ---- Gold Price ----
def get_gold_price():
    try:
        url = "https://api.metals.live/v1/spot/gold"
        data = requests.get(url).json()
        return data[0]["price"]
    except:
        return "Unavailable"

# ---- Silver Price ----
def get_silver_price():
    try:
        url = "https://api.metals.live/v1/spot/silver"
        data = requests.get(url).json()
        return data[0]["price"]
    except:
        return "Unavailable"

# ---- Oil Price ----
def get_oil_price():
    try:
        url = "https://api.metals.live/v1/spot/oil"
        data = requests.get(url).json()
        return data[0]["price"]
    except:
        return "Unavailable"


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Gold (USD)", get_gold_price())

with col2:
    st.metric("Silver (USD)", get_silver_price())

with col3:
    st.metric("WTI Crude Oil", get_oil_price())


st.divider()

st.subheader("📰 Global Market News")

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey=YOUR_NEWSAPI_KEY"
        response = requests.get(url)
        data = response.json()
        return data["articles"]
    except:
        return []

articles = get_news()

for article in articles:
    st.markdown(f"### {article['title']}")
    st.write(article["source"]["name"])
    st.write(article["description"])
    st.markdown(f"[Read more]({article['url']})")
    st.divider()
