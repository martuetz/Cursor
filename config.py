"""
Configuration file for Market Dashboard
Contains API keys, settings, and constants
"""

import os
from typing import Dict, List

# API Configuration
FRED_API_KEY = os.getenv("FRED_API_KEY", "demo")  # Get from environment variable
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")  # Optional for higher rate limits

# Data Source URLs
FRED_BASE_URL = "https://api.stlouisfed.org/fred"
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
STOOQ_BASE_URL = "https://stooq.com/q/d/l"
YALE_SHILLER_URL = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"

# Cache TTL Settings (in seconds)
CACHE_TTL = {
    'price_data': 300,      # 5 minutes for live prices
    'daily_data': 3600,     # 1 hour for daily data
    'monthly_data': 86400,  # 24 hours for monthly data
    'quarterly_data': 604800, # 1 week for quarterly data
}

# Market Indicators Configuration
VALUATION_THRESHOLDS = {
    'sp500_pe': {
        'green': {'max': 18, 'description': 'Undervalued'},
        'yellow': {'min': 18, 'max': 24, 'description': 'Fairly valued'},
        'red': {'min': 24, 'description': 'Overvalued'}
    },
    'shiller_cape': {
        'green': {'max': 20, 'description': 'Undervalued'},
        'yellow': {'min': 20, 'max': 30, 'description': 'Fairly valued'},
        'red': {'min': 30, 'description': 'Overvalued'}
    },
    'buffett_indicator': {
        'green': {'max': 120, 'description': 'Undervalued'},
        'yellow': {'min': 120, 'max': 150, 'description': 'Fairly valued'},
        'red': {'min': 150, 'description': 'Overvalued'}
    },
    'margin_debt': {
        'green': {'max': 0, 'description': 'Decreasing leverage'},
        'yellow': {'min': 0, 'max': 10, 'description': 'Moderate growth'},
        'red': {'min': 10, 'description': 'Rapid leverage growth'}
    },
    'concentration': {
        'green': {'max': 25, 'description': 'Diversified market'},
        'yellow': {'min': 25, 'max': 35, 'description': 'Moderate concentration'},
        'red': {'min': 35, 'description': 'High concentration'}
    },
    'sentiment': {
        'green': {'max': 25, 'description': 'Extreme fear (contrarian opportunity)'},
        'yellow': {'min': 25, 'max': 75, 'description': 'Neutral sentiment'},
        'red': {'min': 75, 'description': 'Extreme greed (potential top)'}
    }
}

# Asset Symbols and Names
ASSET_MAPPING = {
    'US Equities': {
        'S&P 500': '^GSPC',
        'Nasdaq-100': '^IXIC',
        'Russell 2000': '^RUT',
        'Dow Jones': '^DJI'
    },
    'Europe Equities': {
        'STOXX 600': '^STOXX',
        'DAX': '^GDAXI',
        'FTSE 100': '^FTSE',
        'CAC 40': '^FCHI'
    },
    'Asia Equities': {
        'Nikkei 225': '^N225',
        'TOPIX': '^TOPX',
        'Hang Seng': '^HSI',
        'Shanghai Composite': '^SSEC'
    },
    'Commodities': {
        'WTI Crude': 'CL=F',
        'Brent Crude': 'BZ=F',
        'Gold': 'GC=F',
        'Copper': 'HG=F',
        'Silver': 'SI=F'
    },
    'Bonds': {
        '10Y Treasury': '^TNX',
        '13W Treasury': '^IRX',
        '30Y Treasury': '^TYX',
        '2Y Treasury': '^UST2YR'
    },
    'Crypto': {
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD',
        'Binance Coin': 'BNB-USD',
        'Cardano': 'ADA-USD'
    }
}

# Technical Indicators Configuration
TECHNICAL_INDICATORS = {
    'moving_averages': [20, 50, 100, 200],
    'rsi_period': 14,
    'volatility_period': 20,
    'bollinger_bands_period': 20,
    'bollinger_bands_std': 2
}

# Chart Configuration
CHART_CONFIG = {
    'default_height': 400,
    'sparkline_height': 100,
    'color_scheme': {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'success': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
        'info': '#3B82F6'
    },
    'template': 'plotly_white'
}

# UI Configuration
UI_CONFIG = {
    'page_title': 'Market Dashboard',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'max_width': 1200
}

# Error Messages
ERROR_MESSAGES = {
    'data_fetch_failed': 'Failed to fetch data from source',
    'insufficient_data': 'Insufficient data for analysis',
    'api_rate_limit': 'API rate limit exceeded. Please try again later.',
    'network_error': 'Network error. Please check your internet connection.',
    'invalid_symbol': 'Invalid symbol provided'
}

# Success Messages
SUCCESS_MESSAGES = {
    'data_loaded': 'Data loaded successfully',
    'analysis_complete': 'Analysis completed successfully',
    'cache_updated': 'Cache updated successfully'
}

# Disclaimer Text
DISCLAIMER_TEXT = """
This dashboard is for educational purposes only and does not constitute investment advice. 
All data is sourced from public APIs and should be verified independently before making investment decisions. 
Past performance does not guarantee future results. 
Always consult with a qualified financial advisor before making investment decisions.
"""

# Data Quality Settings
DATA_QUALITY = {
    'min_data_points': 50,
    'max_data_age_days': 30,
    'required_fields': ['Date', 'Close', 'Volume'],
    'data_validation': True
}

# Performance Settings
PERFORMANCE = {
    'parallel_requests': True,
    'max_concurrent_requests': 5,
    'request_timeout': 10,
    'retry_attempts': 3,
    'retry_delay': 1
}


