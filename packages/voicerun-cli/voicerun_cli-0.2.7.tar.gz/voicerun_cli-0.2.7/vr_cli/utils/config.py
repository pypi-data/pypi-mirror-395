# Configuration and constants for voicerun-cli

import json
import os
from pathlib import Path

# Context configuration file
CONTEXT_CONFIG_FILE = Path.home() / ".voicerun_context"

# Predefined contexts - only default (production)
CONTEXTS = {
    "default": {
        "api_url": "https://api.primvoices.com",
        "frontend_url": "https://app.primvoices.com"
    }
}

def get_current_context():
    """Get the currently selected context from config file."""
    if CONTEXT_CONFIG_FILE.exists():
        try:
            with open(CONTEXT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get("current_context", "default")
        except (json.JSONDecodeError, IOError):
            pass
    return "default"

def set_current_context(context_name, custom_api_url=None):
    """Set the current context and optionally a custom API URL."""
    config = {}
    if CONTEXT_CONFIG_FILE.exists():
        try:
            with open(CONTEXT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            config = {}
    
    config["current_context"] = context_name
    if custom_api_url:
        config["custom_api_url"] = custom_api_url
    elif "custom_api_url" in config:
        del config["custom_api_url"]
    
    with open(CONTEXT_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_all_contexts():
    """Get all available contexts (predefined + user-defined)."""
    all_contexts = CONTEXTS.copy()
    
    # Add user-defined contexts from config file
    if CONTEXT_CONFIG_FILE.exists():
        try:
            with open(CONTEXT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                user_contexts = config.get("user_contexts", {})
                all_contexts.update(user_contexts)
        except (json.JSONDecodeError, IOError):
            pass
    
    return all_contexts

def create_context(name, api_url, frontend_url):
    """Create a new user-defined context."""
    config = {}
    if CONTEXT_CONFIG_FILE.exists():
        try:
            with open(CONTEXT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            config = {}
    
    if "user_contexts" not in config:
        config["user_contexts"] = {}
    
    config["user_contexts"][name] = {
        "api_url": api_url,
        "frontend_url": frontend_url
    }
    
    with open(CONTEXT_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def delete_context(name):
    """Delete a user-defined context."""
    if name in CONTEXTS:
        return False, f"Cannot delete predefined context '{name}'"
    
    if not CONTEXT_CONFIG_FILE.exists():
        return False, f"Context '{name}' not found"
    
    try:
        with open(CONTEXT_CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return False, f"Context '{name}' not found"
    
    user_contexts = config.get("user_contexts", {})
    if name not in user_contexts:
        return False, f"Context '{name}' not found"
    
    del user_contexts[name]
    config["user_contexts"] = user_contexts
    
    # If deleting current context, switch to default
    if config.get("current_context") == name:
        config["current_context"] = "default"
    
    with open(CONTEXT_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    return True, f"Context '{name}' deleted successfully"

def get_context_urls():
    """Get the API and frontend URLs for the current context."""
    current_context = get_current_context()
    
    # Check for custom URL override
    if CONTEXT_CONFIG_FILE.exists():
        try:
            with open(CONTEXT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                if "custom_api_url" in config:
                    # For custom URLs, derive frontend URL by replacing 'api' with 'app'
                    api_url = config["custom_api_url"]
                    frontend_url = api_url.replace("api", "app").replace("api-", "app-")
                    return api_url, frontend_url
        except (json.JSONDecodeError, IOError):
            pass
    
    # Check all contexts (predefined + user-defined)
    all_contexts = get_all_contexts()
    if current_context in all_contexts:
        context = all_contexts[current_context]
        return context["api_url"], context["frontend_url"]
    
    # Fallback to default
    context = CONTEXTS["default"]
    return context["api_url"], context["frontend_url"]

# API Configuration - can be overridden with environment variables or context
API_BASE_URL = os.getenv("VOICERUN_API_URL")
FRONTEND_URL = os.getenv("VOICERUN_FRONTEND_URL")

if not API_BASE_URL or not FRONTEND_URL:
    context_api_url, context_frontend_url = get_context_urls()
    if not API_BASE_URL:
        API_BASE_URL = context_api_url
    if not FRONTEND_URL:
        FRONTEND_URL = context_frontend_url

# Default URLs for different environments:
# - Production: https://api.primvoices.com / https://app.primvoices.com
# - Development: https://api-dev.primvoices.com / https://app-dev.primvoices.com  
# - Local: http://localhost:8080 / http://localhost:3000
#
# Override via environment variables:
#   export VOICERUN_API_URL="https://api-dev.primvoices.com"
#   export VOICERUN_FRONTEND_URL="https://app-dev.primvoices.com"

# Map file extension to language name
EXT_TO_LANG = {
    "c": "c",
    "cpp": "cpp",
    "cs": "csharp",
    "dart": "dart",
    "go": "go",
    "java": "java",
    "jl": "julia",
    "js": "javascript",
    "kt": "kotlin",
    "lua": "lua",
    "m": "matlab",
    "pl": "perl",
    "php": "php",
    "py": "python",
    "r": "r",
    "rb": "ruby",
    "rs": "rust",
    "scala": "scala",
    "sh": "shell",
    "sql": "sql",
    "swift": "swift",
    "ts": "typescript",
}

# Color constants
TITLE_COLOR = "magenta"
SUCCESS_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
INFO_COLOR = "dim"
TRUE_COLOR = "green"
FALSE_COLOR = "red"
ID_COLOR = "bright_blue"
PATH_COLOR = "cyan"
USER_COLOR = "cyan"
AGENT_COLOR = "green"

# Style constants
TITLE_STYLE = f"bold {TITLE_COLOR}"
SUCCESS_STYLE = f"bold {SUCCESS_COLOR}"
WARNING_STYLE = f"bold {WARNING_COLOR}"
ERROR_STYLE = f"bold {ERROR_COLOR}"
INFO_STYLE = INFO_COLOR
TRUE_STYLE = TRUE_COLOR
FALSE_STYLE = FALSE_COLOR
ID_STYLE = ID_COLOR
PATH_STYLE = PATH_COLOR
USER_STYLE = f"bold {USER_COLOR}"
AGENT_STYLE = f"bold {AGENT_COLOR}"

# Constant strings
UNNAMED = "Unnamed"
NOT_AVAILABLE = "N/A"
COOKIE_FILE = Path.home() / ".voicerun_cookie"
API_KEY_FILE = Path.home() / ".voicerun_apikey"
DEBUG_ENV_NAME = "debug"

# Auth constants
MAX_POLL_ATTEMPTS = 60
POLL_INTERVAL = 2

# Audio input constants
INPUT_SAMPLE_RATE = 16000
INPUT_CHUNK_SIZE = 1024
INPUT_SOUND_THRESHOLD = 0.015
INTERRUPTION_DURATION_MS = 50
DEFAULT_ECHO_DELAY_CHUNKS = 3
ECHO_ALIGNMENT_WINDOW = 20
ECHO_ALIGNMENT_THRESHOLD_FACTOR = 1.5
ECHO_ALIGNMENT_BASELINE_FACTOR = 0.1
ECHO_GRACE_PERIOD = 5
RESIDUAL_THRESHOLD_FACTOR = 0.8
ECHO_ALIGNMENT_SPIKE_FACTOR = 3

# Audio output constants
OUTPUT_SAMPLE_RATE = 24000
OUTPUT_CHUNK_SIZE = 1024
ECHO_BUFFER_SIZE = 50
