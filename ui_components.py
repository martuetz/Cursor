"""
UI Components module for market dashboard
Handles all visual elements, charts, and layout components
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class DashboardComponents:
    """UI components for the market dashboard"""
    
    def __init__(self):
        self.color_scheme = {
            'green': '#10B981',
            'yellow': '#F59E0B', 
            'red': '#EF4444',
            'blue': '#3B82F6',
            'indigo': '#6366F1',
            'purple': '#8B5CF6',
            'gray': '#6B7280',
            'light_gray': '#F3F4F6'
        }
    
    def create_metric_tile(self, title: str, value: float, state: str, 
                          subtitle: str = "", source: str = "", 
                          last_updated: str = "", trend: str = "neutral") -> None:
        """Create a metric tile with traffic light indicator"""
        
        # Color mapping
        state_colors = {
            'green': self.color_scheme['green'],
            'yellow': self.color_scheme['yellow'],
            'red': self.color_scheme['red']
        }
        
        # Trend arrow
        trend_arrows = {
            'up': '↗️',
            'down': '↘️',
            'neutral': '→'
        }
        
        with st.container():
            # Main tile
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{title}**")
                st.markdown(f"<h2 style='margin: 0; color: {state_colors.get(state, self.color_scheme['gray'])}'>{value:.2f}</h2>", unsafe_allow_html=True)
                if subtitle:
                    st.caption(subtitle)
            
            with col2:
                # Traffic light indicator
                st.markdown(f"<div style='text-align: center;'>")
                st.markdown(f"<div style='width: 20px; height: 20px; border-radius: 50%; background-color: {state_colors.get(state, self.color_scheme['gray'])}; margin: auto;'></div>", unsafe_allow_html=True)
                st.markdown(f"<small>{trend_arrows.get(trend, '→')}</small>")
                st.markdown(f"</div>", unsafe_allow_html=True)
            
            # Source and timestamp
            if source or last_updated:
                st.caption(f"Source: {source} | Updated: {last_updated}")
            
            st.divider()
    
    def create_sparkline_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                              title: str = "", height: int = 100) -> None:
        """Create a sparkline chart using Altair"""
        try:
            if data.empty:
                st.caption("No data available")
                return
            
            # Prepare data for sparkline
            chart_data = data[[x_col, y_col]].copy()
            chart_data = chart_data.dropna()
            
            if len(chart_data) < 2:
                st.caption("Insufficient data for chart")
                return
            
            # Create sparkline
            chart = alt.Chart(chart_data).mark_line(
                color=self.color_scheme['blue'],
                strokeWidth=2
            ).encode(
                x=alt.X(f'{x_col}:T', title=None, axis=None),
                y=alt.Y(f'{y_col}:Q', title=None, axis=None)
            ).properties(
                width=200,
                height=height,
                title=title
            ).configure_axis(
                grid=False,
                domain=False
            ).configure_view(
                strokeWidth=0
            )
            
            st.altair_chart(chart, use_container_width=True)
            
        except Exception as e:
            st.caption(f"Chart error: {str(e)}")
    
    def create_trend_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                          title: str = "", show_ma: bool = True) -> None:
        """Create a trend chart with moving averages"""
        try:
            if data.empty:
                st.caption("No data available")
                return
            
            # Prepare data
            chart_data = data[[x_col, y_col]].copy()
            chart_data = chart_data.dropna()
            
            if len(chart_data) < 50:
                st.caption("Insufficient data for trend analysis")
                return
            
            # Calculate moving averages if requested
            if show_ma and len(chart_data) >= 200:
                chart_data['SMA_50'] = chart_data[y_col].rolling(50).mean()
                chart_data['SMA_200'] = chart_data[y_col].rolling(200).mean()
            
            # Create chart
            fig = go.Figure()
            
            # Main price line
            fig.add_trace(go.Scatter(
                x=chart_data[x_col],
                y=chart_data[y_col],
                mode='lines',
                name=y_col,
                line=dict(color=self.color_scheme['blue'], width=2)
            ))
            
            # Moving averages
            if show_ma and 'SMA_50' in chart_data.columns:
                fig.add_trace(go.Scatter(
                    x=chart_data[x_col],
                    y=chart_data['SMA_50'],
                    mode='lines',
                    name='50-Day MA',
                    line=dict(color=self.color_scheme['yellow'], width=1, dash='dash')
                ))
                
                fig.add_trace(go.Scatter(
                    x=chart_data[x_col],
                    y=chart_data['SMA_200'],
                    mode='lines',
                    name='200-Day MA',
                    line=dict(color=self.color_scheme['red'], width=1, dash='dash')
                ))
            
            # Layout
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Value",
                height=400,
                showlegend=True,
                hovermode='x unified',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.caption(f"Chart error: {str(e)}")
    
    def create_gauge_chart(self, value: float, min_val: float, max_val: float,
                          title: str = "", color: str = "blue") -> None:
        """Create a gauge chart for metrics"""
        try:
            # Normalize value to 0-1 range
            normalized_value = (value - min_val) / (max_val - min_val)
            normalized_value = max(0, min(1, normalized_value))  # Clamp to 0-1
            
            # Create gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': title},
                delta={'reference': (min_val + max_val) / 2},
                gauge={
                    'axis': {'range': [min_val, max_val]},
                    'bar': {'color': self.color_scheme.get(color, self.color_scheme['blue'])},
                    'steps': [
                        {'range': [min_val, (min_val + max_val) / 2], 'color': self.color_scheme['light_gray']},
                        {'range': [(min_val + max_val) / 2, max_val], 'color': self.color_scheme['light_gray']}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_val * 0.8
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.caption(f"Gauge chart error: {str(e)}")
    
    def create_heatmap(self, data: pd.DataFrame, title: str = "") -> None:
        """Create a correlation heatmap"""
        try:
            if data.empty:
                st.caption("No data available for heatmap")
                return
            
            # Calculate correlation matrix
            corr_matrix = data.corr()
            
            # Create heatmap
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu",
                title=title
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.caption(f"Heatmap error: {str(e)}")
    
    def create_summary_strip(self, metrics: Dict, composite_score: Dict) -> None:
        """Create the 'What this means' summary strip"""
        try:
            # Count states
            states = {'green': 0, 'yellow': 0, 'red': 0}
            for metric in metrics.values():
                if metric and 'state' in metric:
                    states[metric['state']] += 1
            
            # Determine overall assessment
            if states['red'] >= 3:
                overall_state = "Overvalued"
                state_color = self.color_scheme['red']
            elif states['green'] >= 3:
                overall_state = "Undervalued"
                state_color = self.color_scheme['green']
            else:
                overall_state = "Mixed"
                state_color = self.color_scheme['yellow']
            
            # Get action from composite score
            action = composite_score.get('action', 'Neutral')
            
            # Create summary
            with st.container():
                st.markdown("### 📊 What This Means")
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**Overall Assessment:** {overall_state}")
                    st.markdown(f"**Action Guidance:** {action}")
                
                with col2:
                    st.markdown("**Traffic Light Summary:**")
                    st.markdown(f"🟢 {states['green']} | 🟡 {states['yellow']} | 🔴 {states['red']}")
                
                with col3:
                    st.markdown("**Composite Score:**")
                    valuation_score = composite_score.get('valuation_score', 50)
                    trend_score = composite_score.get('trend_score', 50)
                    st.markdown(f"Valuation: {valuation_score:.0f}")
                    st.markdown(f"Trend: {trend_score:.0f}")
                
                st.divider()
                
        except Exception as e:
            st.error(f"Error creating summary strip: {str(e)}")
    
    def create_asset_filter(self) -> str:
        """Create asset class filter"""
        st.sidebar.markdown("### 🎯 Asset Filter")
        
        asset_class = st.sidebar.selectbox(
            "Select Asset Class",
            ["US Equities", "Europe Equities", "Asia Equities", "Commodities", "Bonds", "Crypto"],
            index=0
        )
        
        return asset_class
    
    def create_region_filter(self) -> str:
        """Create region filter for equities"""
        st.sidebar.markdown("### 🌍 Region Filter")
        
        region = st.sidebar.selectbox(
            "Select Region",
            ["United States", "Europe", "Asia"],
            index=0
        )
        
        return region
    
    def create_time_period_filter(self) -> str:
        """Create time period filter"""
        st.sidebar.markdown("### ⏰ Time Period")
        
        period = st.sidebar.selectbox(
            "Select Period",
            ["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years"],
            index=3
        )
        
        return period
    
    def create_loading_spinner(self, message: str = "Loading data..."):
        """Create a loading spinner"""
        with st.spinner(message):
            time.sleep(0.1)  # Small delay for visual effect
    
    def create_error_message(self, error: str, suggestion: str = ""):
        """Create a styled error message"""
        st.error(f"❌ **Error:** {error}")
        if suggestion:
            st.info(f"💡 **Suggestion:** {suggestion}")
    
    def create_success_message(self, message: str):
        """Create a styled success message"""
        st.success(f"✅ {message}")
    
    def create_info_box(self, title: str, content: str, icon: str = "ℹ️"):
        """Create an info box"""
        with st.expander(f"{icon} {title}"):
            st.markdown(content)
    
    def create_metric_grid(self, metrics: Dict, cols: int = 3) -> None:
        """Create a grid of metric tiles"""
        if not metrics:
            st.warning("No metrics available")
            return
        
        # Create columns
        cols = st.columns(cols)
        
        # Distribute metrics across columns
        metric_items = list(metrics.items())
        for i, (metric_name, metric_data) in enumerate(metric_items):
            if metric_data:
                col_idx = i % len(cols)
                with cols[col_idx]:
                    self.create_metric_tile(
                        title=metric_name.replace('_', ' ').title(),
                        value=metric_data.get('current', 0),
                        state=metric_data.get('state', 'yellow'),
                        subtitle=f"Source: {metric_data.get('source', 'Unknown')}",
                        last_updated=metric_data.get('last_updated', 'Unknown')
                    )
    
    def create_disclaimer(self):
        """Create the disclaimer footer"""
        st.markdown("---")
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ef4444;'>
        <h4 style='color: #ef4444; margin: 0;'>⚠️ Disclaimer</h4>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
        This dashboard is for educational purposes only and does not constitute investment advice. 
        All data is sourced from public APIs and should be verified independently before making investment decisions. 
        Past performance does not guarantee future results.
        </p>
        </div>
        """, unsafe_allow_html=True)


