"""
Test script for Market Dashboard
Verifies that all components can be imported and basic functionality works
"""

import sys
import traceback

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import yfinance as yf
        print("✅ yfinance imported successfully")
    except ImportError as e:
        print(f"❌ yfinance import failed: {e}")
        return False
    
    try:
        import altair as alt
        print("✅ altair imported successfully")
    except ImportError as e:
        print(f"❌ altair import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ plotly imported successfully")
    except ImportError as e:
        print(f"❌ plotly import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test that custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from data_sources import DataManager
        print("✅ DataManager imported successfully")
    except ImportError as e:
        print(f"❌ DataManager import failed: {e}")
        return False
    
    try:
        from ui_components import DashboardComponents
        print("✅ DashboardComponents imported successfully")
    except ImportError as e:
        print(f"❌ DashboardComponents import failed: {e}")
        return False
    
    try:
        import config
        print("✅ config imported successfully")
    except ImportError as e:
        print(f"❌ config import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of custom modules"""
    print("\nTesting basic functionality...")
    
    try:
        from data_sources import DataManager
        from ui_components import DashboardComponents
        
        # Test DataManager initialization
        dm = DataManager()
        print("✅ DataManager initialized successfully")
        
        # Test DashboardComponents initialization
        ui = DashboardComponents()
        print("✅ DashboardComponents initialized successfully")
        
        # Test basic methods
        metrics = dm.get_all_metrics()
        print(f"✅ get_all_metrics returned {len(metrics)} metrics")
        
        composite_score = dm.calculate_composite_score(metrics)
        print(f"✅ calculate_composite_score returned: {composite_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Starting Market Dashboard tests...\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies.")
        return False
    
    # Test custom modules
    if not test_custom_modules():
        print("\n❌ Custom module tests failed. Check file structure.")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed. Check implementation.")
        return False
    
    print("\n🎉 All tests passed! The Market Dashboard is ready to run.")
    print("\nTo run the application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the app: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


