"""
Market Dashboard - Main Application
A comprehensive dashboard for macro market indicators and valuation metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Import custom modules
from data_sources import DataManager
from ui_components import DashboardComponents

# Page configuration
st.set_page_config(
    page_title="Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 0.5rem 0.5rem 0 0;
        gap: 1rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Initialize components
    data_manager = DataManager()
    ui = DashboardComponents()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Market Dashboard</h1>
        <p>Real-time macro market indicators and valuation metrics</p>
        <small>Last updated: {}</small>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("## 🔧 Dashboard Controls")
    
    # Time period filter
    time_period = ui.create_time_period_filter()
    
    # Asset filter
    asset_class = ui.create_asset_filter()
    
    # Region filter
    region = ui.create_region_filter()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Market Overview", 
        "📈 Asset Browser", 
        "📊 Valuation Detail", 
        "🚦 Signals"
    ])
    
    with tab1:
        show_market_overview(data_manager, ui)
    
    with tab2:
        show_asset_browser(data_manager, ui, asset_class, region, time_period)
    
    with tab3:
        show_valuation_detail(data_manager, ui)
    
    with tab4:
        show_signals_dashboard(data_manager, ui)
    
    # Footer disclaimer
    ui.create_disclaimer()

def show_market_overview(data_manager: DataManager, ui: DashboardComponents):
    """Display the market overview dashboard"""
    
    st.markdown("## 🎯 Market Overview")
    st.markdown("Key valuation metrics and market indicators")
    
    try:
        # Load data with spinner
        with ui.create_loading_spinner("Fetching market data..."):
            metrics = data_manager.get_all_metrics()
            composite_score = data_manager.calculate_composite_score(metrics)
        
        if not metrics:
            ui.create_error_message("Failed to load market data", "Please check your internet connection and try again")
            return
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
        st.info("Using demo data instead...")
        # Fallback to demo data
        from demo_data import get_demo_metrics, get_demo_composite_score
        metrics = get_demo_metrics()
        composite_score = get_demo_composite_score()
    
    # Create metric grid
    ui.create_metric_grid(metrics, cols=3)
    
    # Summary strip
    ui.create_summary_strip(metrics, composite_score)
    
    # Additional insights
    st.markdown("### 💡 Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Market health indicator
        if composite_score:
            valuation_score = composite_score.get('valuation_score', 50)
            trend_score = composite_score.get('trend_score', 50)
            
            st.metric(
                label="Market Health Score",
                value=f"{valuation_score:.0f}/100",
                delta=f"{trend_score - 50:+.0f}"
            )
            
            # Health status
            if valuation_score <= 30:
                st.success("🟢 Market appears undervalued")
            elif valuation_score >= 70:
                st.error("🔴 Market appears overvalued")
            else:
                st.warning("🟡 Market appears fairly valued")
    
    with col2:
        # Recent changes
        st.markdown("**📅 Recent Changes**")
        st.caption("Data updates and market movements")
        
        # Simulate recent changes
        changes = [
            "S&P 500 P/E: +0.2 (22.5)",
            "VIX: -1.5 (18.2)",
            "Gold: +$15 ($2,045)",
            "10Y Yield: +0.05% (4.25%)"
        ]
        
        for change in changes:
            st.caption(f"• {change}")

def show_asset_browser(data_manager: DataManager, ui: DashboardComponents, 
                      asset_class: str, region: str, time_period: str):
    """Display the asset browser with detailed analysis"""
    
    st.markdown(f"## 📈 Asset Browser - {asset_class}")
    
    # Asset selection
    if asset_class == "US Equities":
        assets = ["^GSPC", "^IXIC", "^RUT"]  # S&P 500, Nasdaq, Russell
        asset_names = ["S&P 500", "Nasdaq-100", "Russell 2000"]
    elif asset_class == "Europe Equities":
        assets = ["^STOXX", "^GDAXI", "^FTSE"]
        asset_names = ["STOXX 600", "DAX", "FTSE 100"]
    elif asset_class == "Asia Equities":
        assets = ["^N225", "^TOPX", "^HSI"]
        asset_names = ["Nikkei 225", "TOPIX", "Hang Seng"]
    elif asset_class == "Commodities":
        assets = ["CL=F", "BZ=F", "GC=F", "HG=F"]
        asset_names = ["WTI Crude", "Brent Crude", "Gold", "Copper"]
    elif asset_class == "Bonds":
        assets = ["^TNX", "^IRX", "^TYX"]
        asset_names = ["10Y Treasury", "13W Treasury", "30Y Treasury"]
    elif asset_class == "Crypto":
        assets = ["BTC-USD", "ETH-USD"]
        asset_names = ["Bitcoin", "Ethereum"]
    else:
        assets = ["^GSPC"]
        asset_names = ["S&P 500"]
    
    # Asset selector
    selected_asset = st.selectbox("Select Asset", asset_names, index=0)
    selected_symbol = assets[asset_names.index(selected_asset)]
    
    # Load asset data
    try:
        with ui.create_loading_spinner(f"Loading {selected_asset} data..."):
            asset_data = data_manager.get_stock_price(selected_symbol, period="1y")
        
        if asset_data.empty:
            ui.create_error_message(f"Failed to load {selected_asset} data")
            return
    except Exception as e:
        st.error(f"Error loading {selected_asset} data: {str(e)}")
        st.info("Using demo data instead...")
        # Fallback to demo data
        from demo_data import generate_demo_stock_data
        asset_data = generate_demo_stock_data(selected_symbol, 365)
    
    # Main chart
    st.markdown(f"### {selected_asset} Price Chart")
    ui.create_trend_chart(asset_data, 'Date', 'Close', f"{selected_asset} Price", show_ma=True)
    
    # Technical indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Current price
        current_price = asset_data['Close'].iloc[-1]
        price_change = asset_data['Close'].iloc[-1] - asset_data['Close'].iloc[-2]
        price_change_pct = (price_change / asset_data['Close'].iloc[-2]) * 100
        
        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}",
            delta=f"{price_change_pct:+.2f}%"
        )
    
    with col2:
        # 50/200 DMA
        if len(asset_data) >= 200:
            sma_50 = asset_data['Close'].rolling(50).mean().iloc[-1]
            sma_200 = asset_data['Close'].rolling(200).mean().iloc[-1]
            
            st.metric(
                label="50-Day MA",
                value=f"${sma_50:.2f}",
                delta=f"{((current_price - sma_50) / sma_50) * 100:+.2f}%"
            )
    
    with col3:
        # RSI
        if len(asset_data) >= 14:
            delta = asset_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            st.metric(
                label="RSI(14)",
                value=f"{current_rsi:.1f}",
                delta="Oversold" if current_rsi < 30 else "Overbought" if current_rsi > 70 else "Neutral"
            )
    
    # Additional metrics
    st.markdown("### 📊 Additional Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Drawdown
        if len(asset_data) >= 252:  # 1 year of trading days
            peak = asset_data['Close'].rolling(252, min_periods=1).max()
            drawdown = (asset_data['Close'] - peak) / peak * 100
            current_drawdown = drawdown.iloc[-1]
            
            st.metric(
                label="Current Drawdown",
                value=f"{current_drawdown:.2f}%",
                delta="From 52-week high"
            )
    
    with col2:
        # Volatility
        if len(asset_data) >= 20:
            returns = asset_data['Close'].pct_change()
            volatility = returns.rolling(20).std() * np.sqrt(252) * 100
            current_vol = volatility.iloc[-1]
            
            st.metric(
                label="20-Day Volatility",
                value=f"{current_vol:.1f}%",
                delta="Annualized"
            )

def show_valuation_detail(data_manager: DataManager, ui: DashboardComponents):
    """Display detailed valuation analysis"""
    
    st.markdown("## 📊 Valuation Detail")
    st.markdown("Deep dive into valuation metrics and historical context")
    
    # Load all metrics
    try:
        with ui.create_loading_spinner("Loading valuation data..."):
            metrics = data_manager.get_all_metrics()
        
        if not metrics:
            ui.create_error_message("Failed to load valuation data")
            return
    except Exception as e:
        st.error(f"Error loading valuation data: {str(e)}")
        st.info("Using demo data instead...")
        # Fallback to demo data
        from demo_data import get_demo_metrics
        metrics = get_demo_metrics()
    
    # Create tabs for each metric
    metric_names = {
        'cape': 'Shiller CAPE',
        'pe_ratio': 'S&P 500 P/E Ratio',
        'buffett': 'Buffett Indicator',
        'margin_debt': 'Margin Debt',
        'concentration': 'Market Concentration',
        'sentiment': 'Market Sentiment'
    }
    
    metric_tabs = st.tabs(list(metric_names.values()))
    
    for i, (metric_key, metric_name) in enumerate(metric_names.items()):
        with metric_tabs[i]:
            if metric_key in metrics and metrics[metric_key]:
                metric_data = metrics[metric_key]
                
                # Metric overview
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {metric_name}")
                    st.markdown(f"**Current Value:** {metric_data.get('current', 0):.2f}")
                    st.markdown(f"**Status:** {metric_data.get('state', 'Unknown').title()}")
                    st.markdown(f"**Source:** {metric_data.get('source', 'Unknown')}")
                    st.markdown(f"**Last Updated:** {metric_data.get('last_updated', 'Unknown')}")
                
                with col2:
                    # Traffic light indicator
                    state = metric_data.get('state', 'yellow')
                    state_colors = {'green': '#10B981', 'yellow': '#F59E0B', 'red': '#EF4444'}
                    st.markdown(f"""
                    <div style='text-align: center; padding: 1rem;'>
                        <div style='width: 60px; height: 60px; border-radius: 50%; background-color: {state_colors.get(state, '#6B7280')}; margin: auto;'></div>
                        <p style='margin-top: 0.5rem; font-weight: bold;'>{state.upper()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Historical chart if available
                if 'data' in metric_data and not metric_data['data'].empty:
                    st.markdown("### Historical Trend")
                    ui.create_trend_chart(
                        metric_data['data'], 
                        'Date', 
                        list(metric_data['data'].columns)[1],  # Second column is usually the value
                        f"{metric_name} Over Time",
                        show_ma=False
                    )
                
                # Thresholds and explanation
                st.markdown("### 📋 Thresholds & Interpretation")
                
                if metric_key == 'cape':
                    st.markdown("""
                    **Shiller CAPE (Cyclically Adjusted Price-Earnings Ratio)**
                    
                    - **Green (< 20):** Undervalued - historically good buying opportunities
                    - **Yellow (20-30):** Fairly valued - moderate risk/reward
                    - **Red (> 30):** Overvalued - historically poor returns expected
                    
                    The CAPE ratio smooths out earnings volatility by using 10-year average earnings.
                    """)
                
                elif metric_key == 'pe_ratio':
                    st.markdown("""
                    **S&P 500 P/E Ratio (Trailing Twelve Months)**
                    
                    - **Green (< 18):** Undervalued relative to historical norms
                    - **Yellow (18-24):** Fairly valued
                    - **Red (> 24):** Overvalued - high earnings expectations
                    
                    Based on current S&P 500 price divided by trailing 12-month earnings.
                    """)
                
                elif metric_key == 'buffett':
                    st.markdown("""
                    **Buffett Indicator (Total Market Cap / GDP)**
                    
                    - **Green (< 120%):** Undervalued - market cap below GDP
                    - **Yellow (120-150%):** Fairly valued
                    - **Red (> 150%):** Overvalued - market cap significantly above GDP
                    
                    Warren Buffett's preferred market valuation metric.
                    """)
                
                elif metric_key == 'margin_debt':
                    st.markdown("""
                    **Margin Debt (Year-over-Year Change)**
                    
                    - **Green (≤ 0%):** Decreasing leverage - bullish signal
                    - **Yellow (0-10%):** Moderate growth
                    - **Red (> 10%):** Rapid leverage growth - potential risk
                    
                    High margin debt often precedes market corrections.
                    """)
                
                elif metric_key == 'concentration':
                    st.markdown("""
                    **Market Concentration (Top 10 S&P 500 Weight)**
                    
                    - **Green (< 25%):** Diversified market - lower concentration risk
                    - **Yellow (25-35%):** Moderate concentration
                    - **Red (> 35%):** High concentration - "Magnificent 7" dominance
                    
                    High concentration can indicate market euphoria and concentration risk.
                    """)
                
                elif metric_key == 'sentiment':
                    st.markdown("""
                    **Market Sentiment (Fear/Greed Index)**
                    
                    - **Green (≤ 25):** Extreme fear - contrarian buying opportunity
                    - **Yellow (25-75):** Neutral sentiment
                    - **Red (≥ 75):** Extreme greed - potential market top
                    
                    Combines VIX, put/call ratios, and credit spreads.
                    """)
                
                st.divider()

def show_signals_dashboard(data_manager: DataManager, ui: DashboardComponents):
    """Display the signals dashboard with composite analysis"""
    
    st.markdown("## 🚦 Signals Dashboard")
    st.markdown("Composite analysis and action guidance")
    
    # Load data
    try:
        with ui.create_loading_spinner("Calculating signals..."):
            metrics = data_manager.get_all_metrics()
            composite_score = data_manager.calculate_composite_score(metrics)
        
        if not composite_score:
            ui.create_error_message("Failed to calculate composite score")
            return
    except Exception as e:
        st.error(f"Error calculating signals: {str(e)}")
        st.info("Using demo data instead...")
        # Fallback to demo data
        from demo_data import get_demo_metrics, get_demo_composite_score
        metrics = get_demo_metrics()
        composite_score = get_demo_composite_score()
    
    # Two-lens approach
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Valuation Lens (Slow-Moving)")
        
        # Valuation breakdown
        valuation_metrics = ['cape', 'pe_ratio', 'buffett', 'margin_debt', 'concentration']
        valuation_scores = []
        
        for metric in valuation_metrics:
            if metric in metrics and metrics[metric]:
                state = metrics[metric].get('state', 'yellow')
                if state == 'green':
                    score = 25
                elif state == 'yellow':
                    score = 50
                else:
                    score = 75
                valuation_scores.append(score)
        
        if valuation_scores:
            avg_valuation = np.mean(valuation_scores)
            
            # Valuation gauge
            ui.create_gauge_chart(
                avg_valuation, 0, 100, 
                "Valuation Score", 
                "red" if avg_valuation > 70 else "green" if avg_valuation < 30 else "yellow"
            )
            
            # Individual metric scores
            st.markdown("**Individual Scores:**")
            for i, metric in enumerate(valuation_metrics):
                if i < len(valuation_scores):
                    score = valuation_scores[i]
                    metric_name = metric.replace('_', ' ').title()
                    st.caption(f"• {metric_name}: {score:.0f}/100")
    
    with col2:
        st.markdown("### 📈 Trend Lens (Fast-Moving)")
        
        # Trend score (simplified for demo)
        trend_score = composite_score.get('trend_score', 50)
        
        # Trend gauge
        ui.create_gauge_chart(
            trend_score, 0, 100,
            "Trend Score",
            "green" if trend_score > 60 else "red" if trend_score < 40 else "yellow"
        )
        
        # Trend indicators
        st.markdown("**Trend Indicators:**")
        st.caption("• 50/200 DMA Cross: Bullish")
        st.caption("• Price vs 200-DMA: +5.2%")
        st.caption("• Market Breadth: Neutral")
        st.caption("• Credit Spreads: Tightening")
    
    # Action matrix
    st.markdown("### 🎯 Action Matrix")
    
    valuation_score = composite_score.get('valuation_score', 50)
    trend_score = composite_score.get('trend_score', 50)
    
    # Create action matrix
    matrix_data = pd.DataFrame({
        'Trend': ['Bearish', 'Neutral', 'Bullish'],
        'Undervalued': ['Accumulate', 'Accumulate', 'Accumulate'],
        'Fair Value': ['Neutral', 'Neutral', 'Neutral'],
        'Overvalued': ['Trim', 'Trim', 'Wait']
    })
    
    # Highlight current position
    if valuation_score <= 30:
        valuation_col = 'Undervalued'
    elif valuation_score >= 70:
        valuation_col = 'Overvalued'
    else:
        valuation_col = 'Fair Value'
    
    if trend_score <= 40:
        trend_row = 0
    elif trend_score >= 60:
        trend_row = 2
    else:
        trend_row = 1
    
    # Display matrix
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("**Valuation × Trend = Action**")
        
        # Create styled matrix
        matrix_html = """
        <table style='width: 100%; border-collapse: collapse; margin: 1rem 0;'>
            <tr style='background-color: #f8f9fa;'>
                <th style='border: 1px solid #dee2e6; padding: 0.5rem;'>Trend</th>
                <th style='border: 1px solid #dee2e6; padding: 0.5rem;'>Undervalued</th>
                <th style='border: 1px solid #dee2e6; padding: 0.5rem;'>Fair Value</th>
                <th style='border: 1px solid #dee2e6; padding: 0.5rem;'>Overvalued</th>
            </tr>
        """
        
        for i, trend in enumerate(['Bearish', 'Neutral', 'Bullish']):
            matrix_html += f"<tr>"
            matrix_html += f"<td style='border: 1px solid #dee2e6; padding: 0.5rem; font-weight: bold;'>{trend}</td>"
            
            for j, valuation in enumerate(['Undervalued', 'Fair Value', 'Overvalued']):
                action = matrix_data.iloc[i, j+1]
                cell_style = "border: 1px solid #dee2e6; padding: 0.5rem;"
                
                # Highlight current position
                if i == trend_row and j == (0 if valuation_col == 'Undervalued' else 1 if valuation_col == 'Fair Value' else 2):
                    cell_style += "background-color: #667eea; color: white; font-weight: bold;"
                
                matrix_html += f"<td style='{cell_style}'>{action}</td>"
            
            matrix_html += f"</tr>"
        
        matrix_html += "</table>"
        
        st.markdown(matrix_html, unsafe_allow_html=True)
        
        # Current position
        current_action = matrix_data.iloc[trend_row, 0 if valuation_col == 'Undervalued' else 1 if valuation_col == 'Fair Value' else 2]
        st.markdown(f"**Current Position:** {valuation_col} + {matrix_data.iloc[trend_row, 0]} Trend")
        st.markdown(f"**Recommended Action:** **{current_action}**")
    
    # Disclaimer
    st.warning("""
    ⚠️ **Important:** This analysis is for educational purposes only and does not constitute investment advice. 
    Always conduct your own research and consider consulting with a financial advisor before making investment decisions.
    """)

if __name__ == "__main__":
    main()


