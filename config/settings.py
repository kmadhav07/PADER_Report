"""
Global Application Configuration & Settings.

Author: Madhav Kumar
Module: config.settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# Ensure required directories exist
for path in [DATA_DIR, OUTPUT_DIR, PROMPTS_DIR, CONFIG_DIR]:
    os.makedirs(path, exist_ok=True)

DEFAULT_DATASET = os.path.join(DATA_DIR, "Bisoprolol_icsr_sample_1068rows.csv")

# LLM Engine Defaults
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = 0.15
DEFAULT_PROVIDER = "groq"
