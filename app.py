import streamlit as st
import yfinance as yf
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="India Market Impact Pulse", layout="wide")

st.title("🇮🇳 INDIA MARKET IMPACT PULSE")

# -------- Chart Function --------
def chart(symbol):

    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="5m")

    price = round(df["Close"].iloc[-1],2)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines"
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        xaxis_visible=False,
        yaxis_visible=False
    )

    return price, fig


left,right = st.columns([1,1.3])

# -------- LEFT SIDE --------
with left:

    st.subheader("📊 Market Tracker")

    # NIFTY 50
    price,fig = chart("^NSEI")
    st.metric("NIFTY 50", price)
    st.plotly_chart(fig,use_container_width=True)

    # BANK NIFTY
    price,fig = chart("^NSEBANK")
    st.metric("BANK NIFTY", price)
    st.plotly_chart(fig,use_container_width=True)

    # GOLD
    price,fig = chart("GC=F")
    st.metric("GOLD", price)
    st.plotly_chart(fig,use_container_width=True)

    # SILVER
    price,fig = chart("SI=F")
    st.metric("SILVER", price)
    st.plotly_chart(fig,use_container_width=True)

    # CRUDE
    price,fig = chart("CL=F")
    st.metric("CRUDE OIL", price)
    st.plotly_chart(fig,use_container_width=True)


# -------- RIGHT SIDE NEWS --------
with right:

    st.subheader("📰 Market News")

    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&pageSize=5&apiKey=037f99a875704e9e8ca788e6859a7de4"

    data = requests.get(url).json()

    if "articles" in data:

        for article in data["articles"]:

            st.markdown(f"### {article['title']}")
            st.write(article["source"]["name"])

            if article["description"]:
                st.write(article["description"])

            st.markdown(f"[Read full article]({article['url']})")

            st.divider()
