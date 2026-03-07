# --- LEFT COLUMN: LIVE PRO TRACKER (SHARP GRAPHS) ---
with col_left:
    st.markdown("### LIVE COMMODITY TRACKER")
    
    assets = {
        "SILVER (XAG/USD)": {"ticker": "SI=F", "icon": "🥈", "color": "#00FF7F"}, 
        "GOLD (XAU/USD)": {"ticker": "GC=F", "icon": "🟡", "color": "#FFD700"},   
        "WTI CRUDE": {"ticker": "CL=F", "icon": "🛢️", "color": "#00FF7F"},       
        "BITCOIN (BTC)": {"ticker": "BTC-USD", "icon": "₿", "color": "#FF8C00"}, 
        "NIFTY 50": {"ticker": "^NSEI", "icon": "🇮🇳", "color": "#00BFFF"}        
    }

    for name, info in assets.items():
        try:
            ticker_data = yf.Ticker(info["ticker"])
            # Fetching 24-hour data
            hist = ticker_data.history(period="1d", interval="15m") # 15m makes the line even sharper
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                status, label_color = ("Bullish", "#00FF7F") if pct_change > 0 else ("Bearish", "#FF4B4B")
                bg_color = f"rgba({0 if pct_change > 0 else 255}, {255 if pct_change > 0 else 75}, {127 if pct_change > 0 else 75}, 0.1)"

                # Card Layout
                st.markdown(f"""
                <div style="background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 12px; margin-bottom: -5px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #8B949E; font-size: 11px; font-weight: bold;">{info['icon']} {name}</span>
                        <span style="background-color: {bg_color}; color: {label_color}; padding: 1px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">{status}</span>
                    </div>
                    <div style="margin: 2px 0;">
                        <span style="color: white; font-size: 24px; font-weight: bold;">${current_price:,.2f}</span>
                    </div>
                    <div style="color: {label_color}; font-size: 13px; font-weight: bold;">
                        {'▲' if pct_change > 0 else '▼'} {pct_change:+.2f}% <span style="color: #555; font-size: 10px; margin-left: 5px;">24H Trend</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # SHARP LINE CHART (Replacing Area Chart)
                # We use only the 'Close' column to ensure a single sharp line
                st.line_chart(hist['Close'], color=info["color"], height=100, use_container_width=True)
        except:
            st.error(f"Syncing {name}...")
