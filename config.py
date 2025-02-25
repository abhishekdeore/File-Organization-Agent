import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key for Google's Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default workspace directory
DEFAULT_WORKSPACE = os.path.join(Path.home(), "Documents", "agent_workspace")

# Ensure workspace exists
os.makedirs(DEFAULT_WORKSPACE, exist_ok=True)

# Memory file path
MEMORY_FILE = os.path.join(Path.home(), ".file_agent_memory.json")