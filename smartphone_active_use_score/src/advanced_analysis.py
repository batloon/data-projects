import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go

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

def analyze_yearly_growth(df):
    """Analyze the growth rate of active use scores over years."""
    plt.figure(figsize=(12, 6))
    
    # Calculate yearly means and growth rates
    yearly_means = df.groupby('year_of_release')['active_use_hours'].mean()
    growth_rates = yearly_means.pct_change() * 100
    
    # Save data to CSV
    growth_data = pd.DataFrame({
        'year_of_release': yearly_means.index,
        'mean_active_use_hours': yearly_means.values,
        'growth_rate_percent': growth_rates.values
    })
    growth_data.to_csv(Path(__file__).parent.parent / 'reports' / 'yearly_growth_data.csv', index=False)
    
    # Plot growth rates
    growth_rates.plot(kind='bar', color='skyblue')
    plt.title('Year-over-Year Growth in Active Use Scores')
    plt.xlabel('Year')
    plt.ylabel('Growth Rate (%)')
    plt.xticks(rotation=45)
    
    # Add value labels
    for i, v in enumerate(growth_rates):
        if not pd.isna(v):
            plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom' if v > 0 else 'top')
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'yearly_growth.png')
    plt.close()
    
    return growth_rates

def analyze_company_consistency(df):
    """Analyze the consistency of active use scores across companies."""
    # Calculate coefficient of variation (CV) for each company
    company_stats = df.groupby('company').agg({
        'active_use_hours': ['mean', 'std', 'count']
    }).round(2)
    
    company_stats.columns = ['mean', 'std', 'count']
    company_stats['cv'] = (company_stats['std'] / company_stats['mean'] * 100).round(2)
    company_stats = company_stats.sort_values('cv')
    
    # Save data to CSV
    company_stats.to_csv(Path(__file__).parent.parent / 'reports' / 'company_consistency_data.csv')
    
    # Plot consistency scores
    plt.figure(figsize=(12, 6))
    sns.barplot(x=company_stats.index, y='cv', data=company_stats)
    plt.title('Score Consistency by Company (Lower is Better)')
    plt.xlabel('Company')
    plt.ylabel('Coefficient of Variation (%)')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'company_consistency.png')
    plt.close()
    
    return company_stats

def analyze_performance_trends(df):
    """Analyze performance trends and identify significant improvements."""
    # Calculate yearly statistics for each company
    yearly_stats = df.groupby(['year_of_release', 'company']).agg({
        'active_use_hours': ['mean', 'std', 'count']
    }).round(2)
    
    yearly_stats.columns = ['mean', 'std', 'count']
    yearly_stats = yearly_stats.reset_index()
    
    # Save yearly stats to CSV
    yearly_stats.to_csv(Path(__file__).parent.parent / 'reports' / 'yearly_performance_trends_data.csv', index=False)
    
    # Identify significant improvements (more than 10% increase)
    improvements = []
    for company in df['company'].unique():
        company_data = yearly_stats[yearly_stats['company'] == company].sort_values('year_of_release')
        if len(company_data) > 1:
            for i in range(1, len(company_data)):
                prev_mean = company_data.iloc[i-1]['mean']
                curr_mean = company_data.iloc[i]['mean']
                improvement = ((curr_mean - prev_mean) / prev_mean) * 100
                if improvement > 10:
                    improvements.append({
                        'company': company,
                        'year': company_data.iloc[i]['year_of_release'],
                        'improvement': improvement
                    })
    
    # Create improvement report
    if improvements:
        improvement_df = pd.DataFrame(improvements)
        improvement_df = improvement_df.sort_values('improvement', ascending=False)
        improvement_df.to_csv(Path(__file__).parent.parent / 'reports' / 'significant_improvements.csv', index=False)
    
    return yearly_stats

def analyze_performance_distribution(df):
    """Analyze the distribution of performance scores."""
    plt.figure(figsize=(15, 10))
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # Overall distribution
    sns.histplot(data=df, x='active_use_hours', bins=30, kde=True, ax=ax1)
    ax1.set_title('Overall Distribution of Active Use Scores')
    ax1.set_xlabel('Active Use Score (hours)')
    ax1.set_ylabel('Count')
    
    # Save distribution data
    hist_data = pd.DataFrame({
        'active_use_hours': df['active_use_hours'].values
    })
    hist_data.to_csv(Path(__file__).parent.parent / 'reports' / 'performance_distribution_data.csv', index=False)
    
    # Company-wise distribution
    sns.boxplot(data=df, x='company', y='active_use_hours', ax=ax2)
    ax2.set_title('Score Distribution by Company')
    ax2.set_xlabel('Company')
    ax2.set_ylabel('Active Use Score (hours)')
    plt.xticks(rotation=45)
    
    # Save boxplot data
    boxplot_data = df[['company', 'active_use_hours']]
    boxplot_data.to_csv(Path(__file__).parent.parent / 'reports' / 'company_distribution_data.csv', index=False)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / 'reports' / 'performance_distribution.png')
    plt.close()

def generate_advanced_statistics(df):
    """Generate advanced statistical analysis."""
    stats_report = []
    
    # Overall statistics
    overall_stats = pd.DataFrame({
        'metric': ['mean', 'median', 'std', 'skewness', 'kurtosis'],
        'value': [
            df['active_use_hours'].mean(),
            df['active_use_hours'].median(),
            df['active_use_hours'].std(),
            df['active_use_hours'].skew(),
            df['active_use_hours'].kurtosis()
        ]
    })
    overall_stats.to_csv(Path(__file__).parent.parent / 'reports' / 'overall_statistics.csv', index=False)
    
    stats_report.append("Overall Statistics:")
    stats_report.append(f"Mean score: {df['active_use_hours'].mean():.2f} hours")
    stats_report.append(f"Median score: {df['active_use_hours'].median():.2f} hours")
    stats_report.append(f"Standard deviation: {df['active_use_hours'].std():.2f} hours")
    stats_report.append(f"Skewness: {df['active_use_hours'].skew():.2f}")
    stats_report.append(f"Kurtosis: {df['active_use_hours'].kurtosis():.2f}\n")
    
    # Company-wise statistics
    company_stats = df.groupby('company').agg({
        'active_use_hours': ['count', 'mean', 'std', 'min', 'max']
    }).round(2)
    company_stats.columns = ['count', 'mean', 'std', 'min', 'max']
    company_stats.to_csv(Path(__file__).parent.parent / 'reports' / 'company_statistics.csv')
    
    stats_report.append("Company-wise Statistics:")
    stats_report.append(company_stats.to_string())
    
    # Year-wise statistics
    year_stats = df.groupby('year_of_release').agg({
        'active_use_hours': ['count', 'mean', 'std', 'min', 'max']
    }).round(2)
    year_stats.columns = ['count', 'mean', 'std', 'min', 'max']
    year_stats.to_csv(Path(__file__).parent.parent / 'reports' / 'year_statistics.csv')
    
    stats_report.append("\nYear-wise Statistics:")
    stats_report.append(year_stats.to_string())
    
    # Save report
    with open(Path(__file__).parent.parent / 'reports' / 'advanced_statistics.txt', 'w') as f:
        f.write('\n'.join(stats_report))

def create_company_radar_chart(df):
    """Create a radar chart comparing company performance metrics with box plot-like statistics."""
    # Calculate statistics for each company
    company_stats = df.groupby('company').agg({
        'active_use_hours': ['mean', 'std', 'min', 'max']
    }).round(2)
    
    company_stats.columns = ['mean', 'std', 'min', 'max']
    company_stats = company_stats.reset_index()
    
    # Save the data for external use
    company_stats.to_csv(Path(__file__).parent.parent / 'reports' / 'company_radar_data.csv', index=False)
    
    # Create radar chart
    fig = go.Figure()
    
    # Add min-max range as a filled area
    fig.add_trace(go.Scatterpolar(
        r=company_stats['max'],
        theta=company_stats['company'],
        fill=None,
        line=dict(color='rgba(0,0,0,0.2)'),
        name='Max Score'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=company_stats['min'],
        theta=company_stats['company'],
        fill='tonext',
        line=dict(color='rgba(0,0,0,0.2)'),
        name='Min Score'
    ))
    
    # Add mean as a solid line
    fig.add_trace(go.Scatterpolar(
        r=company_stats['mean'],
        theta=company_stats['company'],
        line=dict(color='blue', width=2),
        name='Mean Score'
    ))
    
    # Add standard deviation markers
    fig.add_trace(go.Scatterpolar(
        r=company_stats['mean'] + company_stats['std'],
        theta=company_stats['company'],
        mode='markers',
        marker=dict(color='red', size=8, symbol='diamond'),
        name='Mean + Std Dev'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=company_stats['mean'] - company_stats['std'],
        theta=company_stats['company'],
        mode='markers',
        marker=dict(color='red', size=8, symbol='diamond'),
        name='Mean - Std Dev'
    ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, df['active_use_hours'].max() * 1.2]
            )
        ),
        showlegend=True,
        title='Company Active Use Scores Distribution',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Save the interactive HTML file
    fig.write_html(Path(__file__).parent.parent / 'reports' / 'company_radar_chart.html')
    
    return company_stats

def main():
    """Main function to run advanced analyses."""
    # Create reports directory if it doesn't exist
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    # Load data
    df = load_data()
    
    # Run analyses
    growth_rates = analyze_yearly_growth(df)
    company_consistency = analyze_company_consistency(df)
    performance_trends = analyze_performance_trends(df)
    analyze_performance_distribution(df)
    generate_advanced_statistics(df)
    company_radar_data = create_company_radar_chart(df)
    
    print("Advanced analysis complete! Check the 'reports' directory for results.")
    print("\nKey findings:")
    print(f"Average yearly growth rate: {growth_rates.mean():.1f}%")
    print(f"Most consistent company: {company_consistency.index[0]} (CV: {company_consistency['cv'].iloc[0]:.1f}%)")
    print(f"Least consistent company: {company_consistency.index[-1]} (CV: {company_consistency['cv'].iloc[-1]:.1f}%)")

if __name__ == "__main__":
    main() 