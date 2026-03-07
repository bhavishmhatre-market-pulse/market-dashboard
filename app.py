import streamlit as st
import yfinance as yf
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Global Market Impact Pulse 2026", layout="wide")

# ---- Custom Dark Styling ----
st.markdown("""
<style>
body {background-color:#0e1117;}
.metric-card{
    background:#161b22;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}
.news-good{
    background:#10281d;
    padding:15px;
    border-radius:10px;
    border-left:5px solid #00ff9f;
}
.news-bad{
    background:#2a1010;
    padding:15px;
    border-radius:10px;
    border-left:5px solid #ff4b4b;
}
.news-critical{
    background:#3a1111;
    padding:15px;
    border-radius:10px;
    border:2px solid #ff4b4b;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 GLOBAL MARKET IMPACT PULSE 2026")

# ---- Layout ----
left, right = st.columns([1,1.3])

# -----------------------
# LEFT SIDE (COMMODITIES)
# -----------------------

with left:

    st.subheader("📊 Live Commodity Tracker")

    def chart(symbol):
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="5m")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines"
        ))

        fig.update_layout(
            height=120,
            margin=dict(l=0,r=0,t=0,b=0),
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            xaxis_visible=False,
            yaxis_visible=False
        )

        return fig, round(df["Close"].iloc[-1],2)

    # Silver
    fig, price = chart("SI=F")
    st.markdown("### 🪙 SILVER (XAG/USD)")
    st.metric("Price", f"${price}")
    st.plotly_chart(fig,use_container_width=True)

    # Gold
    fig, price = chart("GC=F")
    st.markdown("### 🥇 GOLD (XAU/USD)")
    st.metric("Price", f"${price}")
    st.plotly_chart(fig,use_container_width=True)

    # Oil
    fig, price = chart("CL=F")
    st.markdown("### 🛢 WTI CRUDE")
    st.metric("Price", f"${price}")
    st.plotly_chart(fig,use_container_width=True)

# -----------------------
# RIGHT SIDE (NEWS)
# -----------------------

with right:

    st.subheader("📰 News Impact Stream")

    url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey=037f99a875704e9e8ca788e6859a7de4"
    data = requests.get(url).json()

    if "articles" in data:

        for i,article in enumerate(data["articles"]):

            title = article["title"]
            desc = article["description"]
            link = article["url"]

            if i == 0:
                st.markdown(f"""
                <div class="news-critical">
                <b>🚨 CRITICAL ALERT</b><br>
                {title}<br><br>
                {desc}<br>
                <a href="{link}">Read more</a>
                </div>
                """, unsafe_allow_html=True)

            elif i % 2 == 0:
                st.markdown(f"""
                <div class="news-good">
                <b>GOOD IMPACT</b><br>
                {title}<br><br>
                {desc}<br>
                <a href="{link}">Read more</a>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="news-bad">
                <b>BAD IMPACT</b><br>
                {title}<br><br>
                {desc}<br>
                <a href="{link}">Read more</a>
                </div>
                """, unsafe_allow_html=True)

# ---- Bottom Indicators ----
st.divider()

c1,c2,c3 = st.columns(3)

sp500 = yf.Ticker("^GSPC").history(period="1d")["Close"].iloc[-1]
dxy = yf.Ticker("DX-Y.NYB").history(period="1d")["Close"].iloc[-1]
bond = yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1]

c1.metric("S&P 500", round(sp500,2))
c2.metric("US Dollar Index", round(dxy,2))
c3.metric("US 10Y Yield", round(bond,2))
