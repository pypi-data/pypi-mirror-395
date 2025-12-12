"""Configuration for web dashboard."""

import os
from pathlib import Path
import tempfile


class Config:
    """Base configuration."""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    BASE_DIR = Path(__file__).resolve().parent.parent

    # Template and static folders
    TEMPLATE_FOLDER = BASE_DIR / "web" / "templates"
    STATIC_FOLDER = BASE_DIR / "web" / "static"

    # Export settings
    EXPORT_TEMP_DIR = Path(os.environ.get("EXPORT_TEMP_DIR", tempfile.gettempdir()))

    # Alert thresholds
    DEFAULT_ALERT_THRESHOLDS = {
        "cost": 0.20,  # 20% increase
        "latency": 0.30,  # 30% increase
        "quality": -0.10,  # 10% decrease
        "error_rate": 0.05,  # 5% increase
    }

    # A/B Testing
    MIN_CALLS_FOR_AB_TEST = 5


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
