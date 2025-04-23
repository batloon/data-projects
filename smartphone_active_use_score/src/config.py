"""Configuration settings for the smartphone active use score analysis."""

# File paths
DATA_FILE = 'data/phone_active_use_scores_full.csv'
REPORTS_DIR = 'reports'

# Plot settings
PLOT_STYLE = 'seaborn'
FIGURE_DPI = 300
FIGURE_FORMAT = 'png'

# Analysis settings
TOP_N_MODELS = 20
HIGH_END_KEYWORDS = ['Pro', 'Ultra', 'Plus', 'Max']

# Color settings
COLOR_PALETTE = 'husl'
PLOT_BACKGROUND = 'white'

# Font settings
FONT_FAMILY = 'sans-serif'
FONT_SIZE = 10

# Export settings
CSV_DECIMAL = '.'
CSV_SEPARATOR = ','

# Interactive plot settings
PLOTLY_TEMPLATE = 'plotly_white'
PLOT_HEIGHT = 600
PLOT_WIDTH = 1000 