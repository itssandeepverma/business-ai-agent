import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Claude / Anthropic API key
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY (or CLAUDE_API_KEY) is not set in the environment variables.")

# Single-model configuration pulled from environment.
MODEL_NAME = os.getenv("ANTHROPIC_MODEL")
if not MODEL_NAME:
    raise ValueError("ANTHROPIC_MODEL is not set in the environment variables.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
