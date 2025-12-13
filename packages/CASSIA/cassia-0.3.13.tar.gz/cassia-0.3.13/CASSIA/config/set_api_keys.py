"""
API Key Configuration File
--------------------------
This file sets API keys as environment variables for the current Python session.
DO NOT commit this file to git - it contains sensitive credentials.

Usage:
    import set_api_keys  # Run this at the start of your script/notebook
"""

import os

# =============================================================================
# ADD YOUR API KEYS BELOW
# =============================================================================

# Anthropic API Key (for Claude models)
ANTHROPIC_API_KEY = "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"

# OpenAI API Key
OPENAI_API_KEY = "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"

# OpenRouter API Key
OPENROUTER_API_KEY = "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"

# Custom API Key (if needed)
CUSTOMIZED_API_KEY = "your-custom-key-here"

# =============================================================================
# SET ENVIRONMENT VARIABLES (runs automatically on import)
# =============================================================================

def set_keys():
    """Set all API keys as environment variables."""
    keys = {
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "OPENROUTER_API_KEY": OPENROUTER_API_KEY,
        "CUSTOMIZED_API_KEY": CUSTOMIZED_API_KEY,
    }

    for key_name, key_value in keys.items():
        if key_value and not key_value.startswith("your-"):
            os.environ[key_name] = key_value
            print(f"Set {key_name}")

# Auto-run when imported
set_keys()


print(os.getenv("ANTHROPIC_API_KEY"))
print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENROUTER_API_KEY"))
print(os.getenv("CUSTOMIZED_API_KEY"))