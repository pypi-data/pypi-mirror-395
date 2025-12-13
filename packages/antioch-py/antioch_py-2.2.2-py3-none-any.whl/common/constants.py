import os
from pathlib import Path

ANTIOCH_ENV = os.environ.get("ANTIOCH_ENV", "prod").lower()
if ANTIOCH_ENV not in ("prod", "staging"):
    raise ValueError(f"Invalid ANTIOCH_ENV: {ANTIOCH_ENV}")

if ANTIOCH_ENV == "staging":
    ANTIOCH_API_URL = "https://staging.api.antioch.com"
    AUTH_DOMAIN = "https://staging.auth.antioch.com"
    AUTH_CLIENT_ID = "x0aOquV43Xe76ehqAm6Zir80O0MWpqTV"
else:
    ANTIOCH_API_URL = "https://api.antioch.com"
    AUTH_DOMAIN = "https://auth.antioch.com"
    AUTH_CLIENT_ID = "8RLoPEgMP3ih10sfJsGPkwbUWGilsoyX"

ANTIOCH_API_URL = os.environ.get("ANTIOCH_API_URL", ANTIOCH_API_URL)
AUTH_DOMAIN = os.environ.get("AUTH_DOMAIN", AUTH_DOMAIN)
ANTIOCH_DIR = os.environ.get("ANTIOCH_DIR", str(Path.home() / ".antioch" / ANTIOCH_ENV))


def get_auth_dir() -> Path:
    """
    Get the auth storage directory path.

    Creates the auth directory if it doesn't exist.

    :return: Path to the auth directory.
    """

    auth_dir = Path(ANTIOCH_DIR) / "auth"
    auth_dir.mkdir(parents=True, exist_ok=True)
    return auth_dir


def get_ark_dir() -> Path:
    """
    Get the arks storage directory path.

    Creates the arks directory if it doesn't exist.

    :return: Path to the arks directory.
    """

    ark_dir = Path(ANTIOCH_DIR) / "arks"
    ark_dir.mkdir(parents=True, exist_ok=True)
    return ark_dir


def get_asset_dir() -> Path:
    """
    Get the assets storage directory path.

    Creates the assets directory if it doesn't exist.

    :return: Path to the assets directory.
    """

    asset_dir = Path(ANTIOCH_DIR) / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    return asset_dir
