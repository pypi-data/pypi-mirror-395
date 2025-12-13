import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

# AWS configuration
AWS_PROFILE = os.getenv("AWS_PROFILE", "kolomolo")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Bedrock model from environment
BEDROCK_MODEL = os.getenv("BEDROCK_MODEL")
MAX_TOKENS = 4096
