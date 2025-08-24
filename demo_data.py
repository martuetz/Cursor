"""
Demo data module for Market Dashboard
Provides sample data for testing and development
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_demo_stock_data(symbol: str = "SPY", days: int = 365) -> pd.DataFrame:
    """Generate demo stock price data"""
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate price data with realistic patterns
    np.random.seed(42)  # For reproducible data
    
    # Start with a base price
    base_price = 400 if "SPY" in symbol else 100
    
    # Generate daily returns with some trend and volatility
    daily_returns = np.random.normal(0.0005, 0.015, len(dates))  # 0.05% daily return, 1.5% volatility
    
    # Add some trend
    trend = np.linspace(0, 0.1, len(dates))  # 10% annual trend
    daily_returns += trend / 252
    
    # Add some cyclicality
    cycles = 0.02 * np.sin(2 * np.pi * np.arange(len(dates)) / 63)  # Quarterly cycles
    daily_returns += cycles
    
    # Calculate prices
    prices = [base_price]
    for ret in daily_returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Generate other OHLC data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC from close price
        volatility = 0.01  # 1% intraday volatility
        
        high = price * (1 + np.random.uniform(0, volatility))
        low = price * (1 - np.random.uniform(0, volatility))
        open_price = np.random.uniform(low, high)
        
        # Generate volume
        volume = np.random.randint(1000000, 10000000)
        
        data.append({
            'Date': date,
            'Open': open_price,
            'High': high,
            'Low': low,
            'Close': price,
            'Volume': volume
        })
    
    return pd.DataFrame(data)

def generate_demo_cape_data() -> pd.DataFrame:
    """Generate demo Shiller CAPE data"""
    
    # Generate monthly data from 1990 to present
    start_date = datetime(1990, 1, 1)
    end_date = datetime.now()
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    np.random.seed(42)
    
    # Base CAPE with realistic range
    base_cape = 20
    
    # Add trend and cycles
    trend = np.linspace(0, 5, len(dates))  # Gradual increase
    cycles = 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 120)  # 10-year cycles
    noise = np.random.normal(0, 2, len(dates))
    
    cape_values = base_cape + trend + cycles + noise
    cape_values = np.clip(cape_values, 10, 40)  # Realistic bounds
    
    return pd.DataFrame({
        'Date': dates,
        'CAPE': cape_values
    })

def generate_demo_economic_data() -> dict:
    """Generate demo economic indicators"""
    
    np.random.seed(42)
    
    # GDP data (quarterly)
    gdp_data = {
        'current_gdp': 25000,  # Billion USD
        'gdp_growth': 2.5,     # Annual %
        'gdp_forecast': 2.8    # Next quarter %
    }
    
    # Interest rates
    rates_data = {
        'fed_funds': 5.25,     # Current rate
        '10y_treasury': 4.25,  # 10-year yield
        '2y_treasury': 4.75,   # 2-year yield
        'yield_curve': -0.5,   # 2s10s spread
    }
    
    # Inflation
    inflation_data = {
        'cpi_yoy': 3.2,        # Year-over-year
        'core_cpi': 3.8,       # Core inflation
        'pce': 2.9,            # PCE inflation
    }
    
    # Employment
    employment_data = {
        'unemployment': 3.7,   # Unemployment rate
        'nonfarm_payrolls': 175,  # Thousands
        'labor_force_participation': 62.5,  # %
    }
    
    return {
        'gdp': gdp_data,
        'rates': rates_data,
        'inflation': inflation_data,
        'employment': employment_data
    }

def generate_demo_market_data() -> dict:
    """Generate demo market indicators"""
    
    np.random.seed(42)
    
    # Market breadth
    breadth_data = {
        'advancing_stocks': 1250,
        'declining_stocks': 750,
        'advance_decline_ratio': 1.67,
        'new_highs': 45,
        'new_lows': 12
    }
    
    # Volatility
    volatility_data = {
        'vix': 18.5,
        'vix_percentile': 35,
        'realized_vol_30d': 15.2,
        'realized_vol_60d': 16.8
    }
    
    # Sentiment
    sentiment_data = {
        'fear_greed_index': 45,
        'put_call_ratio': 0.85,
        'bull_bear_ratio': 1.2,
        'aaii_bullish': 38.5
    }
    
    # Technical indicators
    technical_data = {
        'sp500_above_200ma': 0.75,  # 75% of stocks above 200-day MA
        'sp500_above_50ma': 0.65,   # 65% of stocks above 50-day MA
        'golden_cross': 0.60,       # 60% of stocks with golden cross
        'death_cross': 0.15         # 15% of stocks with death cross
    }
    
    return {
        'breadth': breadth_data,
        'volatility': volatility_data,
        'sentiment': sentiment_data,
        'technical': technical_data
    }

def generate_demo_crypto_data() -> dict:
    """Generate demo cryptocurrency data"""
    
    np.random.seed(42)
    
    # Bitcoin data
    btc_data = {
        'price': 43250,
        'market_cap': 850000000000,
        'volume_24h': 25000000000,
        'price_change_24h': 2.5,
        'price_change_7d': -1.2,
        'dominance': 52.5
    }
    
    # Ethereum data
    eth_data = {
        'price': 2650,
        'market_cap': 320000000000,
        'volume_24h': 15000000000,
        'price_change_24h': 1.8,
        'price_change_7d': 3.5,
        'dominance': 18.2
    }
    
    # Market overview
    market_data = {
        'total_market_cap': 1650000000000,
        'total_volume_24h': 85000000000,
        'btc_dominance': 52.5,
        'defi_market_cap': 45000000000,
        'nft_volume_24h': 25000000
    }
    
    return {
        'bitcoin': btc_data,
        'ethereum': eth_data,
        'market': market_data
    }

def get_demo_metrics() -> dict:
    """Get all demo metrics for testing"""
    
    return {
        'cape': {
            'current': 28.5,
            'state': 'yellow',
            'data': generate_demo_cape_data(),
            'percentile': 75,
            'source': 'Yale/Shiller (Demo)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        'pe_ratio': {
            'current': 22.5,
            'state': 'yellow',
            'price': 4325.50,
            'source': 'Yahoo Finance (Demo)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        'buffett': {
            'current': 135.2,
            'state': 'yellow',
            'market_cap': 45000,
            'gdp': 25000,
            'source': 'FRED + Market Data (Demo)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        'margin_debt': {
            'current': 8.5,
            'state': 'yellow',
            'source': 'FINRA (Demo)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        'concentration': {
            'current': 32.5,
            'state': 'yellow',
            'source': 'SPY Holdings (Demo)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        'sentiment': {
            'current': 45.0,
            'state': 'yellow',
            'vix': 18.5,
            'put_call_ratio': 0.85,
            'hy_spread': 350,
            'source': 'CBOE + FRED (Demo)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    }

def get_demo_composite_score() -> dict:
    """Get demo composite score for testing"""
    
    return {
        'valuation_score': 55.0,
        'trend_score': 60.0,
        'action': 'Neutral',
        'last_calculated': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

if __name__ == "__main__":
    # Test demo data generation
    print("Testing demo data generation...")
    
    # Test stock data
    stock_data = generate_demo_stock_data("SPY", 30)
    print(f"Generated {len(stock_data)} days of stock data")
    print(f"Latest price: ${stock_data['Close'].iloc[-1]:.2f}")
    
    # Test CAPE data
    cape_data = generate_demo_cape_data()
    print(f"Generated {len(cape_data)} months of CAPE data")
    print(f"Latest CAPE: {cape_data['CAPE'].iloc[-1]:.2f}")
    
    # Test metrics
    metrics = get_demo_metrics()
    print(f"Generated {len(metrics)} demo metrics")
    
    # Test composite score
    score = get_demo_composite_score()
    print(f"Demo composite score: {score}")
    
    print("\n✅ Demo data generation successful!")


