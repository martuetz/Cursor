# Market Dashboard - Deployment Guide

This guide covers deploying the Market Dashboard to various platforms, with a focus on Streamlit Cloud for easy deployment.

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd market-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

### Test the Application

Before deploying, run the test script to ensure everything works:

```bash
python test_app.py
```

## ☁️ Streamlit Cloud Deployment

### One-Click Deployment

1. **Fork this repository** to your GitHub account
2. **Visit [Streamlit Cloud](https://share.streamlit.io/)**
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Select your forked repository**
6. **Set the path to your app**: `app.py`
7. **Click "Deploy!"**

### Manual Deployment

1. **Push your code to GitHub**
2. **Create a new app in Streamlit Cloud**
3. **Configure deployment settings**:
   - **Repository**: Your GitHub repo
   - **Branch**: `main` or `master`
   - **Main file path**: `app.py`
   - **Python version**: 3.9+

### Environment Variables (Optional)

For production use, you can set environment variables in Streamlit Cloud:

- `FRED_API_KEY`: Your FRED API key for economic data
- `COINGECKO_API_KEY`: Your CoinGecko API key (optional)

## 🔧 Configuration

### Streamlit Configuration

The `.streamlit/config.toml` file contains:
- Theme customization
- Server settings
- Performance optimizations

### Application Configuration

Edit `config.py` to customize:
- API endpoints
- Threshold values
- Asset mappings
- Chart settings

## 📊 Data Sources

### Free Data Sources Used

- **Yahoo Finance**: Stock prices and indices
- **FRED**: Economic indicators (GDP, yields)
- **CoinGecko**: Cryptocurrency data
- **CBOE**: VIX and options data

### Data Refresh Rates

- **Live prices**: 5 minutes
- **Daily data**: 1 hour
- **Monthly data**: 24 hours
- **Quarterly data**: 1 week

## 🚨 Important Notes

### Rate Limits

- **Yahoo Finance**: No API key required, but rate limited
- **FRED**: 1000 requests per day with demo key
- **CoinGecko**: 50 calls/minute free tier

### Data Quality

- All data is cached to minimize API calls
- Graceful fallbacks for failed requests
- Clear source attribution for all metrics

## 🔒 Security Considerations

### Public Data Only

- No sensitive financial data
- No user authentication required
- All data sources are public APIs

### Disclaimer

The application includes prominent disclaimers that:
- Data is for educational purposes only
- Not investment advice
- Users should verify data independently

## 📈 Performance Optimization

### Caching Strategy

- **Streamlit caching**: Built-in data caching
- **TTL-based expiration**: Data refreshes automatically
- **Parallel requests**: Multiple data sources fetched simultaneously

### Monitoring

- **Data health indicators**: Shows data freshness
- **Error handling**: Graceful degradation
- **Loading states**: User feedback during data fetch

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
2. **API rate limits**: Check data source status
3. **Chart rendering**: Verify plotly/altair installation
4. **Memory issues**: Reduce data history periods

### Debug Mode

Enable debug mode in Streamlit Cloud:
1. Go to app settings
2. Set `developmentMode = true`
3. Check logs for detailed error messages

## 🔄 Updates and Maintenance

### Regular Updates

- **Dependencies**: Update requirements.txt monthly
- **Data sources**: Monitor API changes
- **Thresholds**: Review valuation metrics quarterly

### Backup Strategy

- **Code**: GitHub repository
- **Configuration**: Version controlled
- **Data**: No persistent storage (all cached)

## 📚 Additional Resources

### Documentation

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)
- [FRED API](https://fred.stlouisfed.org/docs/api/fred/)
- [Plotly Documentation](https://plotly.com/python/)

### Support

- **GitHub Issues**: Report bugs and feature requests
- **Streamlit Community**: Get help with Streamlit
- **Data Source Issues**: Check respective API status pages

## 🎯 Next Steps

### Enhancements

1. **Real-time data**: WebSocket connections for live updates
2. **User preferences**: Save user settings and watchlists
3. **Advanced analytics**: Machine learning models for predictions
4. **Mobile optimization**: Responsive design improvements

### Scaling

1. **Database integration**: Store historical data locally
2. **Multiple users**: User authentication and profiles
3. **API rate management**: Intelligent request scheduling
4. **CDN integration**: Faster global access

---

**Happy Trading! 📈**

Remember: This dashboard is for educational purposes only. Always do your own research and consult with financial professionals before making investment decisions.


