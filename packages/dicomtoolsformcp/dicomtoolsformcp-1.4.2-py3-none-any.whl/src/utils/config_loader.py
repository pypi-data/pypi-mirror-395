"""
Configuration loading utilities.
"""
import os
from argparse import Namespace
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    """
    config = {
        "max_workers": int(os.getenv("MAX_WORKERS", "10")),
        "max_retries": int(os.getenv("MAX_RETRIES", "3")),
        "DEFAULT_CONNECT_TIMEOUT": int(os.getenv("DEFAULT_CONNECT_TIMEOUT", "3")),
        "DEFAULT_READ_TIMEOUT": int(os.getenv("DEFAULT_READ_TIMEOUT", "5")),
        "DEFAULT_RETRY_DELAY": int(os.getenv("DEFAULT_RETRY_DELAY", "5")),
        "DEFAULT_BATCH_SIZE": int(os.getenv("DEFAULT_BATCH_SIZE", "6")),
        "base_url": os.getenv("base_url"),
        "name": os.getenv("name"),
        "password": os.getenv("password"),
        "tel": os.getenv("tel"),
        "cookie": os.getenv("COOKIE") # Optional, if manually set
    }
    return config

def create_upload_config(config: Dict) -> Namespace:
    """
    Create upload configuration namespace from config dictionary.
    """
    return Namespace(
        max_workers=config.get("max_workers", 10),
        max_retries=config.get("max_retries", 3),
        DEFAULT_CONNECT_TIMEOUT=config.get("DEFAULT_CONNECT_TIMEOUT", 3),
        DEFAULT_READ_TIMEOUT=config.get("DEFAULT_READ_TIMEOUT", 5),
        DEFAULT_RETRY_DELAY=config.get("DEFAULT_RETRY_DELAY", 5),
        DEFAULT_BATCH_SIZE=config.get("DEFAULT_BATCH_SIZE", 6)
    )
