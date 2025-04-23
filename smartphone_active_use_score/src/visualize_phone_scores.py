import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
from datetime import datetime

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_theme()

def load_data():
    """Load and preprocess the smartphone data."""
    data_path = Path(__file__).parent.parent / 'data' / 'phone_active_use_scores_full.csv'
    df = pd.read_csv(data_path)
    
    # Convert active_use_score from HH:MMh format to hours
    def convert_time_to_hours(time_str):
        time_str = time_str.replace('h', '')
        hours, minutes = map(float, time_str.split(':'))
        return hours + minutes/60
    
    df['active_use_hours'] = df['active_use_score'].apply(convert_time_to_hours)
    
    return df

def plot_company_trends(df):
    """Plot trends of active use scores by company."""
    plt.figure(figsize=(15, 8))
    
    # Calculate mean scores by company
    company_means = df.groupby('company')['active_use_hours'].mean().sort_values(ascending=False)
    
    # Create bar plot
    sns.barplot(x=company_means.index, y=company_means.values)
    plt.xticks(rotation=45, ha='right')
    plt.title('Average Active Use Score by Company')
    plt.xlabel('Company')
    plt.ylabel('Active Use Score (hours)')
    
    # Save plot
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'company_trends.png')
    plt.close()

def plot_top_models(df):
    """Plot top performing models."""
    plt.figure(figsize=(15, 8))
    
    # Get top 20 models
    top_20 = df.nlargest(20, 'active_use_hours')
    
    # Create bar plot
    sns.barplot(data=top_20, x='active_use_hours', y='phone', hue='company', dodge=False)
    plt.title('Top 20 Smartphones by Active Use Score')
    plt.xlabel('Active Use Score (hours)')
    plt.ylabel('Phone Model')
    
    # Save plot
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'top_models.png')
    plt.close()

def plot_score_distribution(df):
    """Plot distribution of active use scores."""
    plt.figure(figsize=(12, 6))
    
    sns.histplot(data=df, x='active_use_hours', bins=30, kde=True)
    plt.title('Distribution of Active Use Scores')
    plt.xlabel('Active Use Score (hours)')
    plt.ylabel('Count')
    
    # Save plot
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'score_distribution.png')
    plt.close()

def plot_yearly_trends(df):
    """Plot trends in active use scores over years."""
    plt.figure(figsize=(12, 6))
    
    # Calculate mean scores by year and company
    yearly_means = df.groupby(['year_of_release', 'company'])['active_use_hours'].mean().unstack()
    
    # Plot lines for each company
    yearly_means.plot(marker='o')
    plt.title('Active Use Score Trends by Company Over Years')
    plt.xlabel('Year')
    plt.ylabel('Average Active Use Score (hours)')
    plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Save plot
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'yearly_trends.png')
    plt.close()

def generate_company_statistics(df):
    """Generate statistical summary by company."""
    stats = df.groupby('company').agg({
        'active_use_hours': ['count', 'mean', 'std', 'min', 'max']
    }).round(2)
    
    # Save statistics
    stats.to_csv(Path(__file__).parent.parent / 'reports' / 'company_statistics.csv')

def plot_interactive_scatter(df):
    """Create interactive scatter plot using plotly."""
    fig = px.scatter(df, 
                    x='company', 
                    y='active_use_hours',
                    color='company',
                    hover_data=['phone', 'active_use_score', 'year_of_release'],
                    title='Active Use Scores by Company (Interactive)')
    
    fig.update_layout(
        xaxis_title="Company",
        yaxis_title="Active Use Score (hours)",
        showlegend=False
    )
    
    # Save as HTML
    fig.write_html(str(Path(__file__).parent.parent / 'reports' / 'interactive_scatter.html'))

def main():
    """Main function to run all analyses."""
    # Create reports directory if it doesn't exist
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    # Load data
    df = load_data()
    
    # Generate all plots and statistics
    plot_company_trends(df)
    plot_top_models(df)
    plot_score_distribution(df)
    plot_yearly_trends(df)
    generate_company_statistics(df)
    plot_interactive_scatter(df)
    
    print("Analysis complete! Check the 'reports' directory for results.")

if __name__ == "__main__":
    main() 