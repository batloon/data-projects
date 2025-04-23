# Smartphone Active Use Score Analysis

This project analyzes smartphone active use scores across different manufacturers and models. The analysis includes trends over time, company comparisons, and other interesting insights about smartphone battery performance.

## Project Structure

```
smartphone_active_use_score/
├── data/                      # Data directory
│   └── phone_active_use_scores_full.csv  # Raw data file
├── reports/                   # Generated analysis reports
├── src/                      # Source code
│   ├── visualize_phone_scores.py    # Main visualization script
│   ├── advanced_analysis.py         # Advanced analysis functions
│   └── config.py                    # Configuration settings
├── add_price_column.py       # Script to add price data to the dataset
├── requirements.txt          # Project dependencies
├── .gitignore               # Git ignore rules
├── venv/                    # Virtual environment directory
└── README.md                # This file
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the main analysis:
```bash
python src/visualize_phone_scores.py
```

## Data Description

The dataset contains the following columns:
- phone: Smartphone model name
- active_use_score: Battery life score in hours:minutes format
- company: Manufacturing company
- year_of_release: Release year
- month_of_release: Release month

## Analysis Features

1. Time series analysis of active use scores by company
2. Company performance comparisons
3. Top performing models identification
4. Release patterns and trends
5. Statistical analysis of scores distribution

## Datasource
- [Final spreadhseet of data](https://docs.google.com/spreadsheets/d/16y0KW-pMc-8WF1tQnnMqaOBHZKz5smxV1EADZs81Tpw/edit?usp=sharing)

## Dependencies

See `requirements.txt` for the complete list of dependencies. 