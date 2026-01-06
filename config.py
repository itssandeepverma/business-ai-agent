import os
from dotenv import load_dotenv


load_dotenv()

# Claude / Anthropic API key
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY (or CLAUDE_API_KEY) is not set in the environment variables.")

# Default Claude model
MODEL_NAME = "claude-3-sonnet-20240229"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
