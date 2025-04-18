"""
Configuration settings for the Coffee Happiness Analysis
"""

# Threshold configurations
COFFEE_CONSUMPTION_THRESHOLD = 2.0  # kg per capita/year
HAPPINESS_SCORE_THRESHOLD = 6.0     # happiness index

# Coffee consumption categories (in kg per capita/year)
COFFEE_CATEGORIES = {
    'Exceptionally High': 14.0,
    'Very High': 6.0,
    'High': 3.0,
    'Moderate': 1.0,
    'Low': 0.5,
    'Very Low': 0.0
}

# Visualization colors
COLORS = {
    'coffee_only': '#FFA500',    # Orange
    'happiness_only': '#006400', # Dark Green
    'intersection': '#8B4513',   # Brown
    'base': '#EAEAEA'           # Light Gray
}

# Output settings
OUTPUT_DIR = 'reports'
DATA_FILE = 'data/coffee_happiness_correlation.csv'

# Map settings
MAP_WIDTH = 1200
MAP_HEIGHT = 800 