import streamlit as st
import yfinance as yf
import requests

st.set_page_config(page_title="India Market Impact Pulse", layout="wide")

st.title("📊 IN INDIA MARKET IMPACT PULSE")

# -------- MARKET DATA --------

def get_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d")
        price = data["Close"].iloc[-1]
        return round(price,2), data["Close"]
    except:
        return "Unavailable", []

col1, col2 = st.columns(2)

with col1:
    price, chart = get_price("^NSEI")
    st.metric("NIFTY 50", price)
    if len(chart) > 0:
        st.line_chart(chart)

with col2:
    price, chart = get_price("^NSEBANK")
    st.metric("BANKNIFTY", price)
    if len(chart) > 0:
        st.line_chart(chart)

st.divider()

# -------- NEWS --------

st.header("📰 Market News")

API_KEY = "037f99a875704e9e8ca788e6859a7de4"

def get_news():
    url = f"https://newsapi.org/v2/everything?q=stock%20market&language=en&sortBy=publishedAt&pageSize=5&apiKey={API_KEY}"
    r = requests.get(url)
    data = r.json()

    if "articles" in data:
        return data["articles"]
    else:
        return []

articles = get_news()

if articles:
    for a in articles:
        st.subheader(a["title"])
        st.write(a["source"]["name"])
        st.write(a["description"])
        st.markdown(f"[Read full article]({a['url']})")
        st.divider()
else:
    st.warning("News could not be loaded.")
