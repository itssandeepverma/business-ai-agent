import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Claude / Anthropic API key
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY (or CLAUDE_API_KEY) is not set in the environment variables.")

# Model preference: env override first, then newest 3.5 Sonnet, then broadly available 3 Sonnet.
MODEL_PREFERENCE = [
    os.getenv("ANTHROPIC_MODEL"),
    "claude-sonnet-4-5-20250929"
]

# Remove empty entries and expose primary + fallbacks for downstream use.
MODEL_PREFERENCE = [model for model in MODEL_PREFERENCE if model]
MODEL_NAME = MODEL_PREFERENCE[0]
MODEL_FALLBACKS = MODEL_PREFERENCE[1:]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
