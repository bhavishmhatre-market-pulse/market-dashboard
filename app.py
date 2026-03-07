import streamlit as st
import yfinance as yf
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Market Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #0B0C10; }
h1, h2, h3 { color: white !important; }
.block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("GLOBAL MARKET IMPACT PULSE 2026")

# -----------------------------
# AUTO REFRESH
# -----------------------------
st_autorefresh(interval=60000, key="marketpulse")

# -----------------------------
# SENTIMENT ANALYZER
# -----------------------------
analyzer = SentimentIntensityAnalyzer()

# -----------------------------
# ASSET IMPACT DETECTOR
# -----------------------------
def detect_asset_impact(text):

    text = text.lower()

    impact = {
        "gold": "Neutral",
        "silver": "Neutral",
        "oil": "Neutral",
        "crypto": "Neutral",
        "nifty": "Neutral"
    }

    if any(k in text for k in ["war","conflict","iran","geopolitical","tension","military"]):
        impact["gold"] = "Bullish"
        impact["oil"] = "Bullish"
        impact["nifty"] = "Bearish"

    if any(k in text for k in ["inflation","rate hike","fed","interest rate","central bank"]):
        impact["gold"] = "Bullish"
        impact["crypto"] = "Bearish"
        impact["nifty"] = "Bearish"

    if any(k in text for k in ["opec","oil supply","production cut"]):
        impact["oil"] = "Bullish"

    if any(k in text for k in ["bitcoin","crypto","etf","blockchain"]):
        impact["crypto"] = "Bullish"

    return impact


# -----------------------------
# FETCH MARKET DATA
# -----------------------------
@st.cache_data(ttl=60)
def get_market_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1d", interval="15m")
    return hist


# -----------------------------
# FETCH NEWS
# -----------------------------
@st.cache_data(ttl=60)
def get_news():

    API_KEY = st.secrets["NEWS_API_KEY"]

    query = "(gold OR silver OR bitcoin OR crypto OR oil OR inflation OR fed OR geopolitics OR recession OR central bank OR india economy)"

    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={API_KEY}"

    response = requests.get(url).json()

    return response.get("articles", [])


# -----------------------------
# LAYOUT
# -----------------------------
col_left, col_right = st.columns([1,2.5])


# =============================
# LEFT COLUMN (MARKET TRACKER)
# =============================
with col_left:

    st.markdown("### LIVE COMMODITY TRACKER")

    assets = {
        "SILVER (XAG/USD)": {"ticker":"SI=F","icon":"🥈","color":"#00FF7F"},
        "GOLD (XAU/USD)": {"ticker":"GC=F","icon":"🟡","color":"#FFD700"},
        "WTI CRUDE": {"ticker":"CL=F","icon":"🛢️","color":"#00FF7F"},
        "BITCOIN": {"ticker":"BTC-USD","icon":"₿","color":"#FF8C00"},
        "NIFTY 50": {"ticker":"^NSEI","icon":"🇮🇳","color":"#00BFFF"}
    }

    for name,info in assets.items():

        try:

            hist = get_market_data(info["ticker"])

            if not hist.empty:

                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]

                pct_change = ((current_price-prev_price)/prev_price)*100

                status = "Bullish" if pct_change>0 else "Bearish"

                color = "#00FF7F" if pct_change>0 else "#FF4B4B"

                st.markdown(f"""
                <div style="background:#161B22;padding:12px;border-radius:8px;margin-bottom:5px;border:1px solid #30363D">
                <div style="display:flex;justify-content:space-between">
                <span style="color:#8B949E;font-size:11px;font-weight:bold">{info['icon']} {name}</span>
                <span style="color:{color};font-size:11px;font-weight:bold">{status}</span>
                </div>

                <div style="font-size:22px;color:white;font-weight:bold">
                ${current_price:,.2f}
                </div>

                <div style="color:{color};font-size:13px">
                {'▲' if pct_change>0 else '▼'} {pct_change:+.2f}%
                </div>

                </div>
                """,unsafe_allow_html=True)

                st.line_chart(hist['Close'],height=100)

        except:
            st.warning(f"Syncing {name}...")


# =============================
# RIGHT COLUMN (NEWS STREAM)
# =============================
with col_right:

    st.markdown("### NEWS IMPACT STREAM")

    news = get_news()

    sentiment_total = []

    for art in news:

        title = art["title"]
        desc = art.get("description","")

        text = f"{title} {desc}"

        score = analyzer.polarity_scores(text)["compound"]

        sentiment_total.append(score)

        if score > 0.1:
            color = "#00FF7F"
        elif score < -0.1:
            color = "#FF4B4B"
        else:
            color = "#8B949E"

        impact = detect_asset_impact(text)

        high_impact = abs(score) > 0.6

        st.markdown(f"""
        <div style="border-left:5px solid {color};background:#161B22;padding:15px;border-radius:0 8px 8px 0;margin-bottom:10px;border:1px solid #30363D">

        <h5 style="margin:0;color:white">{title}</h5>

        <p style="font-size:12px;color:#8B949E;margin:4px 0">
        Source: {art['source']['name']}
        </p>

        <p style="font-size:12px;color:#00BFFF">
        Gold: {impact['gold']} | Oil: {impact['oil']} | Crypto: {impact['crypto']} | Nifty: {impact['nifty']}
        </p>

        </div>
        """,unsafe_allow_html=True)

        if high_impact:
            st.warning("⚠ High Market Impact News")


# =============================
# GLOBAL SENTIMENT INDICATOR
# =============================
if sentiment_total:

    avg_sentiment = sum(sentiment_total)/len(sentiment_total)

    st.markdown("---")

    if avg_sentiment > 0.2:
        st.success("GLOBAL MARKET SENTIMENT: RISK ON")

    elif avg_sentiment < -0.2:
        st.error("GLOBAL MARKET SENTIMENT: RISK OFF")

    else:
        st.info("GLOBAL MARKET SENTIMENT: NEUTRAL")
