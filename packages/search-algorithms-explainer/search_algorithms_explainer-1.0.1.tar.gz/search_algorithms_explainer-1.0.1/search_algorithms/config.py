"""Configuration for the search algorithms CLI project."""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data files
DATA_DIR = PROJECT_ROOT / "data"
QUESTIONS_FILE = DATA_DIR / "questions.json"

# Logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
RESULTS_FILE = PROJECT_ROOT / "results.json"

# Application
APP_NAME = "Search Algorithms Explainer"
APP_VERSION = "1.0.0"

# Output settings
ENABLE_COLORS = True
VERBOSE = False

# Algorithm settings
LINEAR_SEARCH_COMPLEXITY = "O(n)"
BINARY_SEARCH_COMPLEXITY = "O(log n)"

def get_questions_file():
    """Get the path to questions.json file."""
    return str(QUESTIONS_FILE)

def get_results_file():
    """Get the path to results.json file."""
    return str(RESULTS_FILE)
