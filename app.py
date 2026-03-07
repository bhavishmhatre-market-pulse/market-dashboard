# ==========================================
# --- BOTTOM ROW: AI EXECUTIVE SUMMARY ---
# ==========================================
st.markdown("<br><h4 style='color: #8B949E; font-size: 14px; margin-bottom: 10px;'>🤖 AI EXECUTIVE BRIEFING</h4>", unsafe_allow_html=True)

try:
    # Calculate the overall mood of the entire market based on the news feed
    if 'news' in locals() and len(news) > 0:
        total_score = sum([analyzer.polarity_scores(art['title'])['compound'] for art in news])
        avg_score = total_score / len(news)
        
        # AI Logic Tree: Deciding what story the market is telling
        if avg_score > 0.15:
            market_mood = "OPTIMISTIC 🟢"
            border_glow = "#00FF7F"
            action = "investors are actively buying. Risk appetite is high, and money is flowing into equities and growth assets."
        elif avg_score < -0.15:
            market_mood = "FEARFUL 🔴"
            border_glow = "#FF4B4B"
            action = "capital is rapidly fleeing to safe-haven assets (like Gold and Silver) due to emerging macroeconomic or geopolitical stress."
        else:
            market_mood = "CAUTIOUS & CONSOLIDATING ⚪"
            border_glow = "#AAAAAA"
            action = "markets are trading sideways. Investors are holding their positions and awaiting clearer economic signals or major data drops."
            
        # The dynamically generated paragraph
        summary_text = f"Based on the real-time velocity of breaking news and technical chart momentum, broader market sentiment is currently <strong>{market_mood}</strong>. The aggregate news impact score reads at {round(avg_score, 2)}, indicating that {action} Continue to monitor the 15-minute Pulse lines above for sudden momentum reversals."
        
        st.markdown(f"""
        <div style="background-color: #1A1D24; border: 1px solid {border_glow}; box-shadow: 0px 0px 10px {hex_to_rgba(border_glow, 0.2)}; border-radius: 8px; padding: 20px;">
            <p style="color: #E0E0E0; font-size: 15px; margin: 0; line-height: 1.6; font-family: 'Segoe UI', sans-serif;">
                {summary_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.write("Aggregating market data for summary...")

# ==========================================
# AUTO REFRESH
# ==========================================
time.sleep(60)
st.rerun()
