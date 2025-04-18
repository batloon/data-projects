# Coffee and Happiness Analysis
A Batloon project exploring the relationship between coffee consumption and happiness across nations.

## Overview
This project analyzes the correlation between coffee consumption per capita and happiness scores across different countries. It generates interactive visualizations to explore potential relationships between these metrics.

## Features
- Interactive world maps showing:
  - Coffee consumption distribution (≥1.0 kg per capita/year threshold)
  - Happiness score distribution (≥6.0 threshold)
  - Combined analysis showing intersections between high coffee consumption and happiness
- Detailed analysis report with distribution statistics
- Configurable thresholds and visualization parameters
- Beautiful, interactive Plotly visualizations

## Project Structure
```
coffee_is_happiness/
├── config.py              # Configuration settings
├── visualize_coffee_happiness.py  # Main visualization script
├── analysis.txt          # Detailed analysis report
├── data/                 # Data directory
│   └── coffee_happiness_correlation.csv
└── reports/             # Generated visualizations
    ├── coffee_consumption_map.html
    ├── happiness_map.html
    └── intersection_map.html
```

## Configuration
All major parameters are configurable through `config.py`:
- Coffee consumption thresholds
- Happiness score thresholds
- Color schemes
- Coffee consumption categories
- Output settings

## Recent Updates
- Improved visualization layout with bottom-aligned legends
- Simplified color schemes for better clarity
- Added configurable thresholds for analysis
- Enhanced map interactivity and information display
- Updated analysis with new moderate coffee consumption threshold (1.0 kg)
- Improved visual appeal with custom color schemes

## Usage
```bash
python visualize_coffee_happiness.py
```
This will generate three interactive HTML maps in the reports directory.

## Dependencies
- pandas
- plotly
- seaborn
- matplotlib
- scipy

## Key Findings

- Strong positive correlation between coffee consumption and happiness scores
- Nordic countries consistently rank high in both metrics
- Clear regional and economic patterns in coffee consumption
- Interesting outliers providing cultural insights

For detailed findings, please refer to `reports/analysis.txt`.

## Data Sources

- [Coffee consumption data](https://cafely.com/blogs/research/which-country-consumes-the-most-coffee?srsltid=AfmBOop1soKql0EsXfICurn7mcJHnpQkht6sjaTHc4VBP6nZY8TLfjKU)
- [Happiness scores](https://data.worldhappiness.report/table)
- Geographic data: Natural Earth

## Contributing

This is a proprietary project by Batloon. For any queries or project requests, please contact our team at info@batloon.com.

## About Batloon

Batloon transforms complex data into compelling visual stories. From technology trends to societal shifts, we help you see the patterns that shape our world. Each visualization brings clarity to complexity, making data not just accessible, but unforgettable.

Checkout more stories @ [batloon.com](https://www.batloon.com/)
---

*"Data Stories That Illuminate"* - Batloon
