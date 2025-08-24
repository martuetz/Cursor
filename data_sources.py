"""
Data sources module for market dashboard
Handles all external API calls and data fetching
"""

import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st
from typing import Dict, List, Optional, Tuple
import time

# Constants
FRED_API_KEY = "demo"  # Use demo key for development
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
STOOQ_BASE_URL = "https://stooq.com/q/d/l"

class DataManager:
    """Centralized data management for all market indicators"""
    
    def __init__(self):
        self.cache = {}
        self.last_update = {}
        
    @st.cache_data(ttl=300)  # 5 minutes for price data
    def get_stock_price(_self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get stock price data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            st.error(f"Error fetching {symbol}: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=3600)  # 1 hour for daily data
    def get_vix_data(_self) -> pd.DataFrame:
        """Get VIX data from Yahoo Finance"""
        try:
            vix = yf.Ticker("^VIX")
            data = vix.history(period="1y")
            return data
        except Exception as e:
            st.error(f"Error fetching VIX data: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=86400)  # 24 hours for monthly data
    def get_shiller_cape(_self) -> Dict:
        """Get Shiller CAPE data (simulated for demo)"""
        # In production, this would fetch from Yale/Shiller
        try:
            # Simulate historical CAPE data
            dates = pd.date_range(start='1990-01-01', end=datetime.now(), freq='M')
            np.random.seed(42)  # For reproducible demo data
            cape_values = 15 + np.random.normal(0, 5, len(dates))
            cape_values = np.clip(cape_values, 10, 40)
            
            # Add some trend and cycles
            trend = np.linspace(0, 5, len(dates))
            cape_values += trend + 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 120)
            
            df = pd.DataFrame({
                'Date': dates,
                'CAPE': cape_values
            })
            
            current_cape = cape_values[-1]
            
            # Determine traffic light state
            if current_cape < 20:
                state = "green"
            elif current_cape < 30:
                state = "yellow"
            else:
                state = "red"
                
            return {
                'current': current_cape,
                'state': state,
                'data': df,
                'percentile': np.percentile(cape_values, 85),  # Demo: 85th percentile
                'source': 'Yale/Shiller (Simulated)',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        except Exception as e:
            st.error(f"Error fetching CAPE data: {str(e)}")
            return {}
    
    @st.cache_data(ttl=3600)  # 1 hour
    def get_sp500_pe(_self) -> Dict:
        """Get S&P 500 P/E ratio"""
        try:
            # Get S&P 500 data
            spy = yf.Ticker("^GSPC")
            sp500_data = spy.history(period="1y")
            
            # Get earnings data (simulated for demo)
            # In production, this would fetch from Shiller or other sources
            current_price = sp500_data['Close'].iloc[-1]
            current_pe = 22.5  # Demo value
            
            # Determine traffic light state
            if current_pe < 18:
                state = "green"
            elif current_pe < 24:
                state = "yellow"
            else:
                state = "red"
                
            return {
                'current': current_pe,
                'state': state,
                'price': current_price,
                'source': 'Yahoo Finance + Shiller (Simulated)',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        except Exception as e:
            st.error(f"Error fetching P/E data: {str(e)}")
            return {}
    
    @st.cache_data(ttl=86400)  # 24 hours
    def get_buffett_indicator(_self) -> Dict:
        """Get Buffett Indicator (Market Cap / GDP)"""
        try:
            # Simulate market cap and GDP data
            # In production, this would fetch from FRED and market data sources
            market_cap = 45000  # Billion USD (simulated)
            gdp = 25000  # Billion USD (simulated)
            ratio = market_cap / gdp * 100
            
            # Determine traffic light state
            if ratio < 120:
                state = "green"
            elif ratio < 150:
                state = "yellow"
            else:
                state = "red"
                
            return {
                'current': ratio,
                'state': state,
                'market_cap': market_cap,
                'gdp': gdp,
                'source': 'FRED + Market Data (Simulated)',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        except Exception as e:
            st.error(f"Error fetching Buffett Indicator: {str(e)}")
            return {}
    
    @st.cache_data(ttl=86400)  # 24 hours
    def get_margin_debt(_self) -> Dict:
        """Get margin debt data (simulated)"""
        try:
            # Simulate margin debt YoY change
            # In production, this would fetch from FINRA
            margin_debt_yoy = 8.5  # Percent YoY change (simulated)
            
            # Determine traffic light state
            if margin_debt_yoy <= 0:
                state = "green"
            elif margin_debt_yoy <= 10:
                state = "yellow"
            else:
                state = "red"
                
            return {
                'current': margin_debt_yoy,
                'state': state,
                'source': 'FINRA (Simulated)',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        except Exception as e:
            st.error(f"Error fetching margin debt data: {str(e)}")
            return {}
    
    @st.cache_data(ttl=3600)  # 1 hour
    def get_concentration(_self) -> Dict:
        """Get S&P 500 concentration (Top 10 weight)"""
        try:
            # Simulate concentration data
            # In production, this would fetch from SPY holdings
            concentration = 32.5  # Percent (simulated)
            
            # Determine traffic light state
            if concentration < 25:
                state = "green"
            elif concentration < 35:
                state = "yellow"
            else:
                state = "red"
                
            return {
                'current': concentration,
                'state': state,
                'source': 'SPY Holdings (Simulated)',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        except Exception as e:
            st.error(f"Error fetching concentration data: {str(e)}")
            return {}
    
    @st.cache_data(ttl=3600)  # 1 hour
    def get_sentiment(_self) -> Dict:
        """Get market sentiment (Fear/Greed proxy)"""
        try:
            # Get VIX data for sentiment calculation
            vix_data = _self.get_vix_data()
            if vix_data.empty:
                return {}
            
            # Calculate sentiment score (0-100)
            current_vix = vix_data['Close'].iloc[-1]
            vix_percentile = np.percentile(vix_data['Close'], 75)  # Higher VIX = more fear
            
            # Simulate other sentiment components
            put_call_ratio = 0.8  # Simulated
            hy_spread = 350  # Basis points (simulated)
            
            # Composite sentiment score (0-100, higher = more greed)
            sentiment_score = 50 + (25 - vix_percentile/4) + (put_call_ratio - 0.5) * 20 + (400 - hy_spread) / 4
            sentiment_score = np.clip(sentiment_score, 0, 100)
            
            # Determine traffic light state
            if sentiment_score <= 25:
                state = "green"  # Fear = good for future returns
            elif sentiment_score <= 75:
                state = "yellow"
            else:
                state = "red"  # Greed = bad for future returns
                
            return {
                'current': sentiment_score,
                'state': state,
                'vix': current_vix,
                'put_call_ratio': put_call_ratio,
                'hy_spread': hy_spread,
                'source': 'CBOE + FRED (Simulated)',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        except Exception as e:
            st.error(f"Error fetching sentiment data: {str(e)}")
            return {}
    
    @st.cache_data(ttl=3600)  # 1 hour
    def get_crypto_data(_self, coin_id: str = "bitcoin") -> Dict:
        """Get cryptocurrency data from CoinGecko"""
        try:
            url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '365'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Extract price data
                prices = data['prices']
                df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                
                current_price = df['price'].iloc[-1]
                
                # Calculate technical indicators
                df['sma_50'] = df['price'].rolling(50).mean()
                df['sma_200'] = df['price'].rolling(200).mean()
                
                # Current values
                sma_50 = df['sma_50'].iloc[-1]
                sma_200 = df['sma_200'].iloc[-1]
                
                # Determine trend
                if sma_50 > sma_200:
                    trend = "bullish"
                else:
                    trend = "bearish"
                
                return {
                    'current_price': current_price,
                    'sma_50': sma_50,
                    'sma_200': sma_200,
                    'trend': trend,
                    'data': df,
                    'source': 'CoinGecko',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            else:
                st.error(f"Error fetching crypto data: {response.status_code}")
                return {}
                
        except Exception as e:
            st.error(f"Error fetching crypto data: {str(e)}")
            return {}
    
    def get_all_metrics(self) -> Dict:
        """Get all market metrics for overview"""
        return {
            'cape': self.get_shiller_cape(),
            'pe_ratio': self.get_sp500_pe(),
            'buffett': self.get_buffett_indicator(),
            'margin_debt': self.get_margin_debt(),
            'concentration': self.get_concentration(),
            'sentiment': self.get_sentiment()
        }
    
    def calculate_composite_score(self, metrics: Dict) -> Dict:
        """Calculate composite valuation and trend scores"""
        try:
            # Valuation score (average of percentile ranks)
            valuation_metrics = ['cape', 'pe_ratio', 'buffett', 'margin_debt', 'concentration']
            valuation_scores = []
            
            for metric in valuation_metrics:
                if metric in metrics and metrics[metric]:
                    # Convert traffic light to numeric score
                    state = metrics[metric].get('state', 'yellow')
                    if state == 'green':
                        score = 25
                    elif state == 'yellow':
                        score = 50
                    else:
                        score = 75
                    valuation_scores.append(score)
            
            avg_valuation = np.mean(valuation_scores) if valuation_scores else 50
            
            # Trend score (simplified for demo)
            trend_score = 60  # Simulated trend score
            
            # Determine action guidance
            if avg_valuation <= 30 and trend_score >= 60:
                action = "Accumulate"
            elif avg_valuation >= 70 and trend_score <= 40:
                action = "Trim"
            else:
                action = "Neutral"
            
            return {
                'valuation_score': avg_valuation,
                'trend_score': trend_score,
                'action': action,
                'last_calculated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            
        except Exception as e:
            st.error(f"Error calculating composite score: {str(e)}")
            return {}


