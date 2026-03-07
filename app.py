# ==========================================
# --- TOP ROW: HORIZONTAL TRACKER & PREDICTION ---
# ==========================================
st.markdown("<h4 style='color: #8B949E; font-size: 14px; margin-bottom: 15px;'>📡 LIVE TRACKER & AI TREND FORECAST</h4>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

assets = [
    {"name": "SILVER (XAG)", "ticker": "SI=F", "icon": "🥈", "color": "#00FF7F", "col": col1}, 
    {"name": "GOLD (XAU)", "ticker": "GC=F", "icon": "🟡", "color": "#FFD700", "col": col2},   
    {"name": "WTI CRUDE", "ticker": "CL=F", "icon": "🛢️", "color": "#00FF7F", "col": col3},       
    {"name": "NIFTY 50", "ticker": "^NSEI", "icon": "🇮🇳", "color": "#00BFFF", "col": col4}        
]

for info in assets:
    with info["col"]:
        try:
            ticker_data = yf.Ticker(info["ticker"])
            # Fetching 5 days of data to calculate the future trend
            hist_5d = ticker_data.history(period="5d", interval="1h")
            hist_1d = ticker_data.history(period="1d", interval="15m")
            
            if not hist_1d.empty and not hist_5d.empty:
                current_price = hist_1d['Close'].iloc[-1]
                prev_price = hist_1d['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                
                # --- THE PREDICTION MATH (Momentum + Moving Average) ---
                # We calculate the average price of the last 5 days
                moving_average = hist_5d['Close'].mean()
                
                if current_price > moving_average and pct_change > 0:
                    forecast_text = "FORECAST: STRONG UPTREND 📈"
                    forecast_color = "#00FF7F" # Green
                elif current_price < moving_average and pct_change < 0:
                    forecast_text = "FORECAST: STRONG DOWNTREND 📉"
                    forecast_color = "#FF4B4B" # Red
                elif current_price > moving_average and pct_change < 0:
                    forecast_text = "FORECAST: PULLBACK (LIKELY TO BOUNCE) ⚠️"
                    forecast_color = "#FFD700" # Yellow
                else:
                    forecast_text = "FORECAST: RECOVERY (LIKELY TO RISE) ⏳"
                    forecast_color = "#00BFFF" # Blue
                # --------------------------------------------------------

                if pct_change > 0:
                    status, label_color = "Bullish", "#00FF7F"
                elif pct_change < 0:
                    status, label_color = "Bearish", "#FF4B4B"
                else:
                    status, label_color = "Neutral", "#AAAAAA"
                    
                bg_color = hex_to_rgba(label_color, 0.15)
                price_str = f"₹{current_price:,.2f}" if "NIFTY" in info["name"] else f"${current_price:,.2f}"

                st.markdown(f"""
                <div style="background-color: #1A1D24; border: 1px solid #2A2E39; border-bottom: none; border-radius: 8px 8px 0 0; padding: 15px 15px 0 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #FFFFFF; font-size: 12px; font-weight: 700;">{info['icon']} {info['name']}</span>
                        <span style="background-color: {bg_color}; color: {label_color}; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">{status}</span>
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="color: white; font-size: 20px; font-weight: bold;">{price_str}</span>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <span style="color: {label_color}; font-size: 12px; font-weight: bold;">{'▲' if pct_change > 0 else '▼'} {pct_change:+.2f}%</span>
                    </div>
                    
                    <div style="margin-top: 10px; margin-bottom: 5px; padding-top: 5px; border-top: 1px dashed #30363D;">
                        <span style="color: {forecast_color}; font-size: 10px; font-weight: bold; letter-spacing: 0.5px;">{forecast_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Mini Plotly Chart
                fig = go.Figure(go.Scatter(
                    x=hist_1d.index, y=hist_1d['Close'], mode='lines',
                    line=dict(color=info["color"], width=2),
                    fill='tozeroy', fillcolor=hex_to_rgba(info["color"], 0.1) 
                ))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0), height=40,
                    paper_bgcolor='#1A1D24', plot_bgcolor='#1A1D24',
                    xaxis=dict(showgrid=False, zeroline=False, visible=False), 
                    yaxis=dict(showgrid=False, zeroline=False, visible=False), showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown("""<div style="border-top: 1px solid #2A2E39; margin-bottom: 20px; margin-top: -10px;"></div>""", unsafe_allow_html=True)
        except Exception as e:
            st.write("Loading Data...")
