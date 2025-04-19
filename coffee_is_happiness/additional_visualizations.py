"""
Additional visualizations for Coffee Happiness Analysis
A Batloon Data Science Project

This script creates additional visualizations to analyze the relationship between
coffee consumption and happiness scores across different countries.

Copyright (c) 2025 Batloon. All rights reserved.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os
from config import *

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the data
df = pd.read_csv(DATA_FILE)

# Add Batloon watermark to figures
def add_batloon_watermark(fig):
    fig.add_annotation(
        text="© 2025 Batloon",
        xref="paper",
        yref="paper",
        x=0.98,
        y=0.02,
        showarrow=False,
        font=dict(size=10, color="gray"),
        opacity=0.7
    )

# 1. Scatter Plot with Quadrants
def create_quadrant_plot():
    # Calculate median values for quadrant lines
    coffee_median = df['Coffee_Consumption_Per_Capita_KG'].median()
    happiness_median = df['Happiness_Score'].median()
    
    # Create the scatter plot
    fig = px.scatter(
        df,
        x='Coffee_Consumption_Per_Capita_KG',
        y='Happiness_Score',
        color='Continent',
        title='Coffee Consumption vs Happiness Score by Continent',
        labels={
            'Coffee_Consumption_Per_Capita_KG': 'Coffee Consumption (kg/capita)',
            'Happiness_Score': 'Happiness Score',
            'Continent': 'Continent'
        }
    )
    
    # Add quadrant lines
    fig.add_vline(x=coffee_median, line_dash="dash", line_color="gray")
    fig.add_hline(y=happiness_median, line_dash="dash", line_color="gray")
    
    # Add quadrant labels
    fig.add_annotation(
        x=coffee_median/2,
        y=happiness_median*1.1,
        text="Low Coffee<br>High Happiness",
        showarrow=False,
        font=dict(size=12)
    )
    fig.add_annotation(
        x=coffee_median*1.5,
        y=happiness_median*1.1,
        text="High Coffee<br>High Happiness",
        showarrow=False,
        font=dict(size=12)
    )
    fig.add_annotation(
        x=coffee_median/2,
        y=happiness_median*0.9,
        text="Low Coffee<br>Low Happiness",
        showarrow=False,
        font=dict(size=12)
    )
    fig.add_annotation(
        x=coffee_median*1.5,
        y=happiness_median*0.9,
        text="High Coffee<br>Low Happiness",
        showarrow=False,
        font=dict(size=12)
    )
    
    # Add trendline
    fig.add_traces(px.scatter(df, x='Coffee_Consumption_Per_Capita_KG', y='Happiness_Score', trendline="ols").data)
    
    # Update layout
    fig.update_layout(
        template='plotly_white',
        width=1000,
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    add_batloon_watermark(fig)
    fig.write_html(f'{OUTPUT_DIR}/quadrant_plot.html')

# 2. Correlation Plot
def create_correlation_plot():
    # Calculate correlation coefficient
    correlation = df['Coffee_Consumption_Per_Capita_KG'].corr(df['Happiness_Score'])
    
    # Create the scatter plot with regression line
    fig = px.scatter(
        df,
        x='Coffee_Consumption_Per_Capita_KG',
        y='Happiness_Score',
        trendline="ols",
        title=f'Coffee Consumption vs Happiness Score (r = {correlation:.3f})',
        labels={
            'Coffee_Consumption_Per_Capita_KG': 'Coffee Consumption (kg/capita)',
            'Happiness_Score': 'Happiness Score'
        }
    )
    
    # Update layout
    fig.update_layout(
        template='plotly_white',
        width=1000,
        height=800
    )
    
    add_batloon_watermark(fig)
    fig.write_html(f'{OUTPUT_DIR}/correlation_plot.html')

# 3. Bubble Chart
def create_bubble_chart():
    # Create the bubble chart
    fig = px.scatter(
        df,
        x='Coffee_Consumption_Per_Capita_KG',
        y='Happiness_Score',
        size='Daily_Coffee_Cups',
        color='Continent',
        title='Coffee Consumption vs Happiness Score by Continent and Daily Cups',
        labels={
            'Coffee_Consumption_Per_Capita_KG': 'Coffee Consumption (kg/capita)',
            'Happiness_Score': 'Happiness Score',
            'Daily_Coffee_Cups': 'Daily Coffee Cups',
            'Continent': 'Continent'
        }
    )
    
    # Update layout
    fig.update_layout(
        template='plotly_white',
        width=1000,
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    add_batloon_watermark(fig)
    fig.write_html(f'{OUTPUT_DIR}/bubble_chart.html')

if __name__ == "__main__":
    create_quadrant_plot()
    create_correlation_plot()
    create_bubble_chart() 