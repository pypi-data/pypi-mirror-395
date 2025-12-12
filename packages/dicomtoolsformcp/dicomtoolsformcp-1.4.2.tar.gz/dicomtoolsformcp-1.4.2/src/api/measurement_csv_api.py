"""
Measurement CSV export API module.
"""
import json
import logging
import traceback
import requests
from typing import Dict, Any, List

from src.utils.config_loader import load_config
from src.utils.cookie_manager import CookieManager
from src.utils.crypto import encrypt

logger = logging.getLogger(__name__)


def get_authenticated_config() -> Dict[str, Any]:
    """
    Load configuration and ensure authentication (cookie).
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


async def export_measurement_csv(study_instance_uids: List[str]) -> Dict[str, Any]:
    """
    Export measurement CSV file for given StudyInstanceUIDs.
    
    Args:
        study_instance_uids: List of StudyInstanceUID strings
        
    Returns:
        Dictionary containing download URL and result information
    """
    try:
        config = get_authenticated_config()
        base_url = config.get('base_url')
        cookie_val = config.get('cookie')
        
        if not base_url or not cookie_val:
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps({
                        "error": True,
                        "message": "Configuration error: Missing base_url or cookie."
                    }, ensure_ascii=False)
                }]
            }

        if not cookie_val.startswith("ls="):
            cookie = "ls=" + cookie_val
        else:
            cookie = cookie_val

        # API endpoint
        api_url = f"{base_url}/cad/case/measurement/export"
        
        # Request headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": f"i18next=zh-CN; {cookie}",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            "lang": "zh-CN"
        }
        
        # Request payload
        payload = {
            "studyInstanceUids": study_instance_uids
        }
        
        logger.info(f"Exporting measurement CSV for {len(study_instance_uids)} studies")
        logger.info(f"API URL: {api_url}")
        
        # Send POST request
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Check if request was successful
        if response_data.get("success") and response_data.get("code") == 1:
            data = response_data.get("data", {})
            route = data.get("route", "")
            params = data.get("params", "")
            
            # Construct download URL
            if route and params:
                # Remove leading slash from route if present
                route = route.lstrip('/')
                download_url = f"{base_url}/{route}?{params}"
            else:
                # Fallback: use route and params from response directly
                route = response_data.get("route", "")
                params = response_data.get("params", "")
                if route and params:
                    route = route.lstrip('/')
                    download_url = f"{base_url}/{route}?{params}"
                else:
                    download_url = None
            
            result = {
                "success": True,
                "message": response_data.get("msg", "操作成功"),
                "download_url": download_url,
                "route": route,
                "params": params,
                "study_count": len(study_instance_uids)
            }
        else:
            result = {
                "success": False,
                "message": response_data.get("msg", "导出失败"),
                "error": response_data
            }
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, indent=2)
            }]
        }
        
    except requests.exceptions.RequestException as e:
        error_info = f"Request failed: {str(e)}"
        logger.error(error_info)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "error": True,
                    "message": error_info
                }, ensure_ascii=False)
            }]
        }
    except Exception as e:
        error_info = f"Error during CSV export: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_info)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "error": True,
                    "message": error_info
                }, ensure_ascii=False)
            }]
        }

