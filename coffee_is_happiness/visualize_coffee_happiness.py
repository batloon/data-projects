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

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the data
df = pd.read_csv(DATA_FILE)

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
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.15,  # Moved further down
        xanchor='center',
        x=0.5,
        bgcolor='rgba(255,255,255,0.8)',  # Semi-transparent white background
        bordercolor='gray',
        borderwidth=1
    ),
    margin=dict(r=50, l=50, t=100, b=150)  # Increased bottom margin for legend
)

add_batloon_watermark(fig3)

# Save the intersection map
fig3.write_html(f'{OUTPUT_DIR}/intersection_map.html')

# Print countries with high coffee consumption
print("\nCountries with high coffee consumption (≥{:.2f} kg):".format(COFFEE_CONSUMPTION_THRESHOLD))
high_coffee_countries = df[df['High_Coffee']].sort_values('Coffee_Consumption_Per_Capita_KG', ascending=False)
for _, row in high_coffee_countries.iterrows():
    print(f"{row['Country']}: {row['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita, Happiness: {row['Happiness_Score']:.2f}")

# Print countries with high happiness score
print("\nCountries with high happiness (≥{:.2f}):".format(HAPPINESS_SCORE_THRESHOLD))
high_happiness_countries = df[df['High_Happiness']].sort_values('Happiness_Score', ascending=False)
for _, row in high_happiness_countries.iterrows():
    print(f"{row['Country']}: {row['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita, Happiness: {row['Happiness_Score']:.2f}")

# Print analysis
print("\nBatloon Coffee Happiness Analysis")
print("================================")
print("\nAnalysis Summary:")
print(f"Total countries in dataset: {len(df)}")
print(f"Countries with high coffee consumption (≥{COFFEE_CONSUMPTION_THRESHOLD} kg): {df['High_Coffee'].sum()}")
print(f"Countries with high happiness (≥{HAPPINESS_SCORE_THRESHOLD}): {df['High_Happiness'].sum()}")
print(f"Countries with both: {df['Intersection'].sum()}")
print(f"Intersection percentage: {intersection_pct:.1f}%")

# Print detailed list of intersection countries
print("\nCountries with both high coffee consumption and high happiness:")
intersection_countries = df[df['Intersection']].sort_values('Coffee_Consumption_Per_Capita_KG', ascending=False)
for _, row in intersection_countries.iterrows():
    print(f"{row['Country']}: {row['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita, Happiness: {row['Happiness_Score']:.2f}")

# Print countries with only high coffee consumption
print("\nCountries with high coffee consumption only (not high happiness):")
coffee_only_countries = df[df['High_Coffee'] & ~df['High_Happiness']].sort_values('Coffee_Consumption_Per_Capita_KG', ascending=False)
for _, row in coffee_only_countries.iterrows():
    print(f"{row['Country']}: {row['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita, Happiness: {row['Happiness_Score']:.2f}")

# Print countries with only high happiness
print("\nCountries with high happiness only (not high coffee consumption):")
happiness_only_countries = df[~df['High_Coffee'] & df['High_Happiness']].sort_values('Happiness_Score', ascending=False)
for _, row in happiness_only_countries.iterrows():
    print(f"{row['Country']}: {row['Coffee_Consumption_Per_Capita_KG']:.2f} kg/capita, Happiness: {row['Happiness_Score']:.2f}")