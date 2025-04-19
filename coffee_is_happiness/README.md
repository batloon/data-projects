# [Coffee Happiness Analysis by Batloon](https://www.batloon.com/articles/the-world-s-happiest-countries-also-love-their-coffee)

A data science project exploring the relationship between coffee consumption and happiness scores across countries.

## Overview

This project analyzes the correlation between coffee consumption per capita and happiness scores across different countries. The analysis includes:

- World maps showing coffee consumption and happiness score distributions
- Intersection analysis of countries with both high coffee consumption and happiness
- Statistical correlation analysis
- Interactive visualizations

## Data

The dataset (`data/coffee_happiness_correlation.csv`) contains:
- Country names
- Happiness scores (0-10 scale)
- Coffee consumption per capita (kg/year)

## Visualizations

The project generates several interactive visualizations:

1. **Coffee Consumption Map**: Shows coffee consumption per capita across countries
2. **Happiness Score Map**: Displays happiness scores across countries
3. **Intersection Map**: Highlights countries with both high coffee consumption and happiness
4. **Scatter Plot**: Visualizes the correlation between coffee consumption and happiness

All visualizations are saved as interactive HTML files in the `reports` directory.

## Analysis

The analysis includes:
- Statistical correlation between coffee consumption and happiness
- Distribution of countries across different coffee consumption and happiness categories
- Top countries by coffee consumption and happiness scores
- Detailed breakdown of countries with high coffee consumption and/or happiness

## Requirements

- Python 3.8+
- Required packages (see `requirements.txt`):
  - pandas
  - plotly
  - seaborn
  - matplotlib
  - scipy
  - numpy

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the analysis script:
```bash
python visualize_coffee_happiness.py
```

This will generate:
- Interactive HTML visualizations in the `reports` directory
- Statistical analysis in `reports/analysis.txt`

## Results

The analysis reveals:
- Correlation between coffee consumption and happiness scores
- Countries with both high coffee consumption and happiness
- Regional patterns in coffee consumption and happiness
- Statistical significance of the relationship

## Key Findings

- Strong positive correlation between coffee consumption and happiness scores
- Nordic countries consistently rank high in both metrics
- Clear regional and economic patterns in coffee consumption
- Interesting outliers providing cultural insights

For detailed findings and datasources, please refer to `reports/analysis.txt`.

## Contributing

This is a proprietary project by Batloon. For any queries or project requests, please contact our team at info@batloon.com.

## About Batloon

Batloon transforms complex data into compelling visual stories. From technology trends to societal shifts, we help you see the patterns that shape our world. Each visualization brings clarity to complexity, making data not just accessible, but unforgettable.


*"Data Stories That Illuminate"* - Checkout more stories @ [batloon.com](https://www.batloon.com/)
