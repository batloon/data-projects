"""
Coffee Happiness Analysis
A Batloon Data Science Project

This script analyzes the relationship between coffee consumption and happiness scores
across different countries, generating visualizations and statistical insights.

Copyright (c) 2025 Batloon. All rights reserved.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os
from config import *
import numpy as np

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the data
df = pd.read_csv(DATA_FILE)

# Filter out countries with zero coffee consumption
df = df[df['Coffee_Consumption_Per_Capita_KG'] > 0]

# Create coffee consumption categories
def get_coffee_category(consumption):
    for category, threshold in COFFEE_CATEGORIES.items():
        if consumption >= threshold:
            return category
    return 'Very Low'

df['Coffee_Category'] = df['Coffee_Consumption_Per_Capita_KG'].apply(get_coffee_category)
df['High_Coffee'] = df['Coffee_Consumption_Per_Capita_KG'] >= COFFEE_CONSUMPTION_THRESHOLD
df['High_Happiness'] = df['Happiness_Score'] >= HAPPINESS_SCORE_THRESHOLD
df['Intersection'] = df['High_Coffee'] & df['High_Happiness']

# Calculate intersection percentage
intersection_pct = (df['Intersection'].sum() / len(df)) * 100

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

# 1. Coffee Consumption World Map
fig1 = go.Figure()

fig1.add_trace(go.Choropleth(
    locations=df['Country'],
    locationmode='country names',
    z=df['High_Coffee'].astype(int),
    text=df.apply(lambda x: f"{x['Country']}<br>Consumption: {x['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita<br>Category: {x['Coffee_Category']}", axis=1),
    colorscale=[[0, COLORS['base']], [0.5, COLORS['base']], [0.5, COLORS['coffee_only']], [1, COLORS['coffee_only']]],
    showscale=True,
    colorbar=dict(
        title=dict(
            text='Coffee Consumption',
            side='top'
        ),
        ticks='outside',
        ticktext=['Low', 'High'],
        tickvals=[0, 1],
        tickmode='array',
        thickness=20,
        len=0.3,
        yanchor='top',
        y=0,
        x=0.5,
        orientation='h'
    ),
    hoverinfo='text'
))

fig1.update_layout(
    title=dict(
        text=f'Coffee Consumption Per Capita (≥{COFFEE_CONSUMPTION_THRESHOLD} kg)',
        x=0.5,
        y=0.95,
        font=dict(size=20)
    ),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        showland=True,
        landcolor='lightgray',
        showcountries=True,
        countrycolor='white'
    ),
    width=MAP_WIDTH,
    height=MAP_HEIGHT,
    template='plotly_white',
    margin=dict(r=50, l=50, t=80, b=50)
)
add_batloon_watermark(fig1)

# Save the coffee consumption map
fig1.write_html(f'{OUTPUT_DIR}/coffee_consumption_map.html')

# 2. Happiness Score World Map
fig2 = go.Figure()

fig2.add_trace(go.Choropleth(
    locations=df['Country'],
    locationmode='country names',
    z=df['High_Happiness'].astype(int),
    text=df.apply(lambda x: f"{x['Country']}<br>Happiness Score: {x['Happiness_Score']:.2f}", axis=1),
    colorscale=[[0, COLORS['base']], [0.5, COLORS['base']], [0.5, COLORS['happiness_only']], [1, COLORS['happiness_only']]],
    showscale=True,
    colorbar=dict(
        title=dict(
            text='Happiness Score',
            side='top'
        ),
        ticks='outside',
        ticktext=['Low', 'High'],
        tickvals=[0, 1],
        tickmode='array',
        thickness=20,
        len=0.3,
        yanchor='top',
        y=0,
        x=0.5,
        orientation='h'
    ),
    hoverinfo='text'
))

fig2.update_layout(
    title=dict(
        text=f'Happiness Score (≥{HAPPINESS_SCORE_THRESHOLD})',
        x=0.5,
        y=0.95,
        font=dict(size=20)
    ),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        showland=True,
        landcolor='lightgray',
        showcountries=True,
        countrycolor='white'
    ),
    width=MAP_WIDTH,
    height=MAP_HEIGHT,
    template='plotly_white',
    margin=dict(r=50, l=50, t=80, b=50)
)
add_batloon_watermark(fig2)

# Save the happiness map
fig2.write_html(f'{OUTPUT_DIR}/happiness_map.html')

# 3. Intersection World Map
fig3 = go.Figure()

# Calculate percentages for the title
coffee_only_pct = (len(df[df['High_Coffee'] & ~df['High_Happiness']]) / len(df)) * 100
happiness_only_pct = (len(df[~df['High_Coffee'] & df['High_Happiness']]) / len(df)) * 100
both_pct = (len(df[df['Intersection']]) / len(df)) * 100

# Add dummy traces for legend
fig3.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='markers',
    marker=dict(size=10, color=COLORS['coffee_only']),
    name='High Coffee Consumption Only',
    showlegend=True
))

fig3.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='markers',
    marker=dict(size=10, color=COLORS['happiness_only']),
    name='High Happiness Only',
    showlegend=True
))

fig3.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='markers',
    marker=dict(size=10, color=COLORS['intersection']),
    name='Both High',
    showlegend=True
))

# Add the choropleth layers
fig3.add_trace(go.Choropleth(
    locations=df[df['High_Coffee'] & ~df['High_Happiness']]['Country'],
    locationmode='country names',
    z=[1] * len(df[df['High_Coffee'] & ~df['High_Happiness']]),
    text=df[df['High_Coffee'] & ~df['High_Happiness']].apply(
        lambda x: f"{x['Country']}<br>Coffee: {x['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita<br>Happiness: {x['Happiness_Score']:.2f}", axis=1),
    colorscale=[[0, COLORS['coffee_only']], [1, COLORS['coffee_only']]],
    showscale=False,
    showlegend=False,
    hoverinfo='text'
))

fig3.add_trace(go.Choropleth(
    locations=df[~df['High_Coffee'] & df['High_Happiness']]['Country'],
    locationmode='country names',
    z=[1] * len(df[~df['High_Coffee'] & df['High_Happiness']]),
    text=df[~df['High_Coffee'] & df['High_Happiness']].apply(
        lambda x: f"{x['Country']}<br>Coffee: {x['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita<br>Happiness: {x['Happiness_Score']:.2f}", axis=1),
    colorscale=[[0, COLORS['happiness_only']], [1, COLORS['happiness_only']]],
    showscale=False,
    showlegend=False,
    hoverinfo='text'
))

fig3.add_trace(go.Choropleth(
    locations=df[df['Intersection']]['Country'],
    locationmode='country names',
    z=[1] * len(df[df['Intersection']]),
    text=df[df['Intersection']].apply(
        lambda x: f"{x['Country']}<br>Coffee: {x['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita<br>Happiness: {x['Happiness_Score']:.2f}", axis=1),
    colorscale=[[0, COLORS['intersection']], [1, COLORS['intersection']]],
    showscale=False,
    showlegend=False,
    hoverinfo='text'
))

# Update layout for the intersection map
fig3.update_layout(
    title=dict(
        text=f'Coffee Consumption Per Capita (≥{COFFEE_CONSUMPTION_THRESHOLD} kg) and Happiness Score (≥{HAPPINESS_SCORE_THRESHOLD}) Distribution<br>' +
             f'Both: {both_pct:.1f}% | High Coffee Consumption Only: {coffee_only_pct:.1f}% | High Happiness Only: {happiness_only_pct:.1f}%',
        x=0.5,
        y=0.95,
        font=dict(size=20)
    ),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        showland=True,
        landcolor='lightgray',
        showcountries=True,
        countrycolor='white'
    ),
    width=MAP_WIDTH,
    height=MAP_HEIGHT,
    template='plotly_white',
    margin=dict(r=50, l=50, t=80, b=50)
)
add_batloon_watermark(fig3)

# Save the intersection map
fig3.write_html(f'{OUTPUT_DIR}/intersection_map.html')

# 4. Scatter Plot
fig4 = go.Figure()

# Add scatter plot points
fig4.add_trace(go.Scatter(
    x=df['Coffee_Consumption_Per_Capita_KG'],
    y=df['Happiness_Score'],
    mode='markers',
    marker=dict(
        size=10,
        color=df.apply(lambda x: COLORS['intersection'] if x['Intersection'] else 
                      COLORS['coffee_only'] if x['High_Coffee'] else 
                      COLORS['happiness_only'] if x['High_Happiness'] else 
                      COLORS['base'], axis=1),
        line=dict(width=1, color='black')
    ),
    text=df.apply(lambda x: f"{x['Country']}<br>Coffee: {x['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita<br>Happiness: {x['Happiness_Score']:.2f}", axis=1),
    hoverinfo='text'
))

# Add trend line
z = np.polyfit(df['Coffee_Consumption_Per_Capita_KG'], df['Happiness_Score'], 1)
p = np.poly1d(z)
fig4.add_trace(go.Scatter(
    x=df['Coffee_Consumption_Per_Capita_KG'],
    y=p(df['Coffee_Consumption_Per_Capita_KG']),
    mode='lines',
    line=dict(color='black', width=2, dash='dash'),
    name='Trend Line'
))

# Calculate correlation coefficient
correlation = df['Coffee_Consumption_Per_Capita_KG'].corr(df['Happiness_Score'])

# Update layout for scatter plot
fig4.update_layout(
    title=dict(
        text=f'Coffee Consumption vs Happiness Score<br>Correlation: {correlation:.3f}',
        x=0.5,
        y=0.95,
        font=dict(size=20)
    ),
    xaxis=dict(
        title='Coffee Consumption Per Capita (kg/year)',
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        title='Happiness Score',
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    ),
    width=MAP_WIDTH,
    height=MAP_HEIGHT,
    template='plotly_white',
    margin=dict(r=50, l=50, t=80, b=50)
)
add_batloon_watermark(fig4)

# Save the scatter plot
fig4.write_html(f'{OUTPUT_DIR}/scatter_plot.html')

# Generate statistical analysis
analysis = f"""Coffee Happiness Analysis
=====================

Data Overview:
-------------
Total Countries: {len(df)}
Countries with High Coffee Consumption (≥{COFFEE_CONSUMPTION_THRESHOLD} kg/capita): {df['High_Coffee'].sum()}
Countries with High Happiness (≥{HAPPINESS_SCORE_THRESHOLD}): {df['High_Happiness'].sum()}
Countries with Both High Coffee and Happiness: {df['Intersection'].sum()}

Distribution:
------------
High Coffee Consumption Only: {coffee_only_pct:.1f}%
High Happiness Only: {happiness_only_pct:.1f}%
Both High: {both_pct:.1f}%
Neither High: {100 - (coffee_only_pct + happiness_only_pct + both_pct):.1f}%

Correlation Analysis:
-------------------
Correlation Coefficient: {correlation:.3f}

Top 10 Countries by Coffee Consumption:
------------------------------------
{df.nlargest(10, 'Coffee_Consumption_Per_Capita_KG')[['Country', 'Coffee_Consumption_Per_Capita_KG', 'Happiness_Score']].to_string()}

Top 10 Countries by Happiness Score:
---------------------------------
{df.nlargest(10, 'Happiness_Score')[['Country', 'Happiness_Score', 'Coffee_Consumption_Per_Capita_KG']].to_string()}

Countries with Both High Coffee and Happiness:
-------------------------------------------
{df[df['Intersection']][['Country', 'Coffee_Consumption_Per_Capita_KG', 'Happiness_Score']].to_string()}

Countries by Category:
-------------------
High Coffee Consumption Only (≥{COFFEE_CONSUMPTION_THRESHOLD} kg/capita, <{HAPPINESS_SCORE_THRESHOLD} happiness):
{df[df['High_Coffee'] & ~df['High_Happiness']][['Country', 'Coffee_Consumption_Per_Capita_KG', 'Happiness_Score']].to_string()}

High Happiness Only (≥{HAPPINESS_SCORE_THRESHOLD} happiness, <{COFFEE_CONSUMPTION_THRESHOLD} kg/capita):
{df[~df['High_Coffee'] & df['High_Happiness']][['Country', 'Coffee_Consumption_Per_Capita_KG', 'Happiness_Score']].to_string()}

Neither High (both <{COFFEE_CONSUMPTION_THRESHOLD} kg/capita and <{HAPPINESS_SCORE_THRESHOLD} happiness):
{df[~df['High_Coffee'] & ~df['High_Happiness']][['Country', 'Coffee_Consumption_Per_Capita_KG', 'Happiness_Score']].to_string()}

"""

# Save the analysis
with open(f'{OUTPUT_DIR}/analysis.txt', 'w') as f:
    f.write(analysis)

# Print the analysis to the console
print(analysis)