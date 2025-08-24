# Market Dashboard - Macro Market Indicators

A comprehensive, real-time dashboard aggregating free macro-market indicators with valuation metrics, trend analysis, and actionable insights.

## Features

### 🎯 Market Overview
- **Valuation Metrics**: S&P 500 P/E, Shiller CAPE, Buffett Indicator, Margin Debt, Concentration, Sentiment
- **Traffic Light System**: Red/Yellow/Green indicators for quick assessment
- **Real-time Data**: Live updates from multiple free data sources
- **Actionable Insights**: Rule-based buy/hold/trim suggestions

### 📊 Asset Browser
- **Multi-Asset Coverage**: US, Europe, Asia equities, Commodities, Bonds, Crypto
- **Technical Analysis**: 50/200-DMA, drawdown, RSI, trend analysis
- **Context Metrics**: Asset-specific indicators (yield curves, volatility, etc.)

### 📈 Valuation Detail
- **Historical Context**: Long-run charts and percentile rankings
- **Threshold Definitions**: Clear explanation of R/Y/G criteria
- **Source Attribution**: Transparent data sourcing

### 🚦 Signals Dashboard
- **Valuation Lens**: Slow-moving fundamental indicators
- **Trend Lens**: Fast-moving technical signals
- **Composite Scoring**: Equal-weighted percentile rankings
- **Action Guidance**: Matrix-based recommendations

## Data Sources

- **Prices/Indices**: Stooq, Yahoo Finance
- **Earnings Data**: Yale/Shiller monthly data
- **Economic Data**: FRED API (GDP, yields, spreads)
- **Market Data**: FINRA margin debt, CBOE VIX/options
- **Crypto**: CoinGecko API

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Usage

1. **Market Overview**: Default landing page with key metrics
2. **Asset Browser**: Filter by region/asset class for detailed analysis
3. **Valuation Detail**: Deep dive into specific metrics
4. **Signals**: Composite analysis and action guidance

## Disclaimer

This application is for educational purposes only and does not constitute investment advice. All data is sourced from public APIs and should be verified independently before making investment decisions.

## Deployment

Deploy to Streamlit Cloud with one-click deployment or run locally with `streamlit run app.py`.

## Data Refresh

- **Intraday**: 5-15 minutes (prices)
- **Daily**: 24 hours (VIX, options)
- **Monthly**: 30 days (margin debt, earnings)
- **Quarterly**: 1 week (GDP data)


