"""
Studies API module for querying patient studies and series information.
"""
import json
import logging
import traceback
import requests
from typing import Dict, Any, List, Optional

from src.utils.config_loader import get_authenticated_config

logger = logging.getLogger(__name__)


def get_series_by_study_instance_uid(
    base_url: str,
    cookie: str,
    study_instance_uid: str
) -> List[Dict[str, Any]]:
    """
    Get series information by StudyInstanceUID.
    
    Args:
        base_url: Base URL of the API
        cookie: Authentication cookie
        study_instance_uid: Study Instance UID
        
    Returns:
        List of series information dictionaries
    """
    api_url = f"{base_url}/api/v2/getSeriesByStudyInstanceUID"
    
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
    
    payload = {
        "StudyInstanceUID": study_instance_uid
    }
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        response_data = response.json()
        
        if response_data.get("code") == 1:
            return response_data.get("data", [])
        else:
            logger.warning(f"Failed to get series for {study_instance_uid}: {response_data.get('msg', 'Unknown error')}")
            return []
    except Exception as e:
        logger.error(f"Error getting series for {study_instance_uid}: {e}")
        return []


async def get_all_studies_and_series(search_str: Optional[str] = None) -> Dict[str, Any]:
    """
    Get all patient studies and their series information from the account.
    
    Args:
        search_str: Optional search string for patient name, case number, or notes (fuzzy search)
        
    Returns:
        Dictionary containing all studies with their series information
    """
    try:
        config = get_authenticated_config()
        
        base_url = config.get('base_url')
        cookie_val = config.get('cookie')
        
        logger.info(f"[get_all_studies_and_series] Config loaded - base_url: {base_url}, cookie: {cookie_val[:20] if cookie_val else None}...")
        
        if not base_url or not cookie_val:
            logger.error(f"[get_all_studies_and_series] Missing config - base_url: {base_url}, has_cookie: {bool(cookie_val)}")
            return {
                "content": [{
                    "type": "text",
                    "text": "Configuration error: Missing base_url or cookie."
                }]
            }

        if not cookie_val.startswith("ls="):
            cookie = "ls=" + cookie_val
        else:
            cookie = cookie_val

        # API endpoint
        api_url = f"{base_url}/api/v3/getStudies"
        
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
        
        all_studies = []
        cur_page = 1
        page_size = 100  # Fixed page size for efficient pagination
        
        logger.info(f"Starting to fetch all studies (search_str: {search_str}, page_size: {page_size})")
        
        # Loop through all pages
        while True:
            payload = {
                "curPage": cur_page,
                "pageSize": page_size,
                "searchStr": search_str if search_str else "",
                "sorterField": "updateTime",
                "sorterOrder": "DESC",
                "labelFilterParams": {
                    "includeStudyFilterParams": [],
                    "excludeStudyFilterParams": [],
                    "includeSeriesFilterParams": [],
                    "excludeSeriesFilterParams": [],
                    "studyLevelWithoutTags": False,
                    "seriesLevelWithoutTags": False,
                    "relationType": 1
                }
            }
            
            logger.info(f"Fetching page {cur_page}...")
            
            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                response_data = response.json()
                
                if response_data.get("code") != 1:
                    logger.warning(f"API returned error code: {response_data.get('code')}, msg: {response_data.get('msg')}")
                    break
                
                data = response_data.get("data", {})
                study_list = data.get("studyList", [])
                
                if not study_list:
                    logger.info(f"No more studies found at page {cur_page}")
                    break
                
                logger.info(f"Found {len(study_list)} studies on page {cur_page}")
                
                # For each study, get its series information
                for study in study_list:
                    study_instance_uid = study.get("StudyInstanceUID")
                    if study_instance_uid:
                        logger.info(f"Fetching series for StudyInstanceUID: {study_instance_uid}")
                        series_list = get_series_by_study_instance_uid(
                            base_url,
                            cookie,
                            study_instance_uid
                        )
                        study["seriesList"] = series_list
                    else:
                        study["seriesList"] = []
                
                all_studies.extend(study_list)
                
                # Check if there are more pages
                pagination = data.get("pagination", {})
                total_count = pagination.get("totalCount", 0)
                page_count = pagination.get("pageCount", 0)
                
                # If current page has fewer items than page_size, or we've reached the last page
                if len(study_list) < page_size or cur_page >= page_count:
                    logger.info(f"Reached last page. Total studies fetched: {len(all_studies)}")
                    break
                
                cur_page += 1
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed for page {cur_page}: {e}")
                break
            except Exception as e:
                logger.error(f"Error processing page {cur_page}: {e}")
                break
        
        result = {
            "success": True,
            "total_studies": len(all_studies),
            "studies": all_studies,
            "search_str": search_str
        }
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, indent=2)
            }]
        }
        
    except Exception as e:
        error_info = f"Error during studies fetch: {str(e)}\n{traceback.format_exc()}"
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

