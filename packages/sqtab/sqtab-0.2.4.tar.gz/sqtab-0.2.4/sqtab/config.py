"""
Configuration management for sqtab.
Centralized loading of environment variables and settings.
"""
import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

_ENV_LOADED = False

def _find_env_file() -> Optional[Path]:
    """
    Find .env file in priority order.

    Returns:
        Path to .env file or None if not found.
    """
    locations = [
        # 1. Current working directory (highest priority)
        Path.cwd() / ".env",
        # 2. Project root (if running from subdirectory)
        Path.cwd().parent / ".env",
        # 3. SQTA_HOME environment variable
        Path(os.getenv("SQTA_HOME", "")) / ".env" if os.getenv("SQTA_HOME") else None,
        # 4. ~/.sqtab/.env
        Path.home() / ".sqtab" / ".env",
        # 5. ~/.config/sqtab/.env
        Path.home() / ".config" / "sqtab" / ".env",
        # 6. ~/.env (global fallback)
        Path.home() / ".env",
    ]

    # Filter out None values
    locations = [loc for loc in locations if loc is not None]

    for location in locations:
        if location.exists():
            return location

    return None


def load_env() -> bool:
    """Load environment variables from .env file, supporting UTF-8 BOM."""
    global _ENV_LOADED

    if _ENV_LOADED:
        return True

    env_file = _find_env_file()

    if not env_file:
        if os.getenv("SQTA_DEBUG"):
            print("[sqtab] No .env file found", file=sys.stderr)
        return False

    try:
        with open(env_file, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()

        env_vars = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

        for key, value in env_vars.items():
            os.environ[key] = value

        _ENV_LOADED = True

        if os.getenv("SQTA_DEBUG"):
            print(f"[sqtab] Loaded {len(env_vars)} variables from: {env_file}", file=sys.stderr)
            if "OPENAI_API_KEY" in env_vars:
                masked = env_vars["OPENAI_API_KEY"][:4] + "..." + env_vars["OPENAI_API_KEY"][-4:]
                print(f"[sqtab] API Key loaded: {masked}", file=sys.stderr)

        return True

    except Exception as e:
        print(f"[sqtab] Error loading .env file {env_file}: {e}", file=sys.stderr)
        return False

def get_api_key() -> Optional[str]:
    """
    Get OpenAI API key.

    Returns:
        OpenAI API key string or None if not set.
    """
    if not _ENV_LOADED:
        load_env()

    return os.getenv("OPENAI_API_KEY")


def require_api_key() -> str:
    """
    Get OpenAI API key, raising error only for AI features.

    Returns:
        OpenAI API key string.

    Raises:
        RuntimeError: If API key is not set (only for AI features).
    """
    api_key = get_api_key()

    if not api_key:
        # Provide helpful error message
        env_file = _find_env_file()
        if env_file:
            raise RuntimeError(
                f"OPENAI_API_KEY not found in {env_file}\n"
                f"AI features require an OpenAI API key.\n\n"
                f"Add the following line to {env_file}:\n"
                f"OPENAI_API_KEY=sk-...\n\n"
                f"Or set it as environment variable:\n"
                f"export OPENAI_API_KEY=sk-..."
            )
        else:
            # Suggest where to create .env file
            suggested_path = Path.cwd() / ".env"
            raise RuntimeError(
                "OPENAI_API_KEY not set.\n"
                "AI features require an OpenAI API key.\n\n"
                f"Create a .env file with your API key:\n"
                f"echo 'OPENAI_API_KEY=sk-...' > {suggested_path}\n\n"
                "Or create the file manually in one of these locations:\n"
                "  - Current folder: .env\n"
                "  - Home folder: ~/.sqtab/.env\n"
                "  - Home folder: ~/.env\n\n"
                "Non-AI features work without API key."
            )

    return api_key


def get_ai_model(default: str = "gpt-4o-mini") -> str:
    """
    Returns AI model name. If SQTAB_AI_MODEL is not set,
    falls back to a sensible default.
    """
    return os.getenv("SQTAB_AI_MODEL", default)


def get_debug() -> bool:
    """
    Check if debug mode is enabled.

    Returns:
        True if debug mode is enabled.
    """
    if not _ENV_LOADED:
        load_env()

    return os.getenv("SQTA_DEBUG", "").lower() in ("1", "true", "yes", "on")

def is_ai_available() -> bool:
    """
    Check if AI features are available.

    Returns:
        True if OpenAI API key is set.
    """
    return get_api_key() is not None

load_env()