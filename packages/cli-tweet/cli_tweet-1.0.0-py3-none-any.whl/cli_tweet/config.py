# src/cli_tweet/config.py
from __future__ import annotations
import os
import sys
from pathlib import Path
from getpass import getpass

from dotenv import load_dotenv

APP_NAME = "cli_tweet"

# Where we store the user's .env file


def _default_config_dir() -> Path:
    # Respect XDG on Linux, works fine on macOS too
    xdg = os.getenv("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / APP_NAME
    return Path.home() / ".config" / APP_NAME


CONFIG_DIR = Path(os.getenv("CLI_TWEET_CONFIG_DIR", _default_config_dir()))
ENV_FILE = CONFIG_DIR / ".env"

ENV_VARS = [
    "TWITTER_API_KEY",
    "TWITTER_API_KEY_SECRET",
    "ACCESS_TOKEN",
    "ACCESS_TOKEN_SECRET",
]


def load_secrets() -> dict[str, str]:
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE, override=False)

    secrets: dict[str, str | None] = {
        name: os.getenv(name) for name in ENV_VARS
    }

    missing = [name for name, value in secrets.items() if not value]

    # Always create CONFIG_DIR early (helps debugging)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not ENV_FILE.exists():
        ENV_FILE.touch()
        try:
            ENV_FILE.chmod(0o600)
        except Exception:
            pass

    if missing:
        if not sys.stdin.isatty():
            # Don't silently skip prompting; be explicit.
            raise RuntimeError(
                "Missing Twitter API credentials: "
                + ", ".join(missing)
                + "\nCannot prompt for them because stdin is not a TTY.\n"
                "Either:\n"
                "  - set them as environment variables, or\n"
                f"  - run `autotweet` directly in a terminal to be prompted, or\n"
                f"  - manually edit {ENV_FILE}"
            )

        print("Twitter API credentials not found for:", ", ".join(missing))
        print("They will be stored in:", ENV_FILE)

        with ENV_FILE.open("a", encoding="utf-8") as f:
            for name in missing:
                from getpass import getpass
                value = getpass(f"Enter {name}: ").strip()
                if not value:
                    continue
                f.write(f"{name}={value}\n")
                secrets[name] = value

    still_missing = [name for name, value in secrets.items() if not value]
    if still_missing:
        raise RuntimeError(
            "Missing Twitter API credentials even after prompting: "
            + ", ".join(still_missing)
        )

    return {k: str(v) for k, v in secrets.items()}


TWEET_LIMIT = 280
