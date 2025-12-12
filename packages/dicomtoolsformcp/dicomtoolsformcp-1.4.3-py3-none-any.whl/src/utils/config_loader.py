"""
Configuration loading utilities.
"""
import os
import json
import logging
from argparse import Namespace
from typing import Dict, Any
from dotenv import load_dotenv

from src.utils.cookie_manager import CookieManager
from src.utils.crypto import encrypt

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

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


def get_authenticated_config() -> Dict[str, Any]:
    """
    Load configuration and ensure authentication (cookie).
    
    Returns:
        Configuration dictionary with authentication cookie.
    """
    config = load_config()
    
    # If cookie is already in config (from env), use it
    if config.get("cookie"):
        # Ensure it has 'ls=' prefix if needed, or just pass it
        # The original code checked for 'ls=' prefix
        pass
    else:
        # Try to login
        base_url = config.get("base_url")
        name = config.get("name")
        password = config.get("password")
        tel = config.get("tel")
        
        if base_url and name and password:
            payload = {"username": name, "password": password}
            if tel:
                payload["phoneNumber"] = tel
                
            plain = json.dumps(payload, ensure_ascii=False)
            cipher = encrypt(plain)
            
            cookie_manager = CookieManager(base_url, cipher)
            cookie = cookie_manager.get_cookie()
            
            if cookie:
                config["cookie"] = cookie
            else:
                logger.warning("Failed to obtain cookie via login.")
        else:
            logger.warning("Missing credentials for login (name, password, base_url).")
            
    return config
