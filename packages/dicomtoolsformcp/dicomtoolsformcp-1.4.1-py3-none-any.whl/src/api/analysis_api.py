"""
Analysis API module for DICOM directory analysis and upload.
"""
import json
import logging
import time
import traceback
from pathlib import Path
from typing import Dict, Any, List

from src.models import DICOMDirectory
from src.utils.config_loader import load_config, create_upload_config
from src.utils.cookie_manager import CookieManager
from src.utils.crypto import encrypt
from src.utils.file_utils import copy_dicom
from src.core import (
    get_series_info,
    should_upload_series,
    upload_series_metadata,
    upload_dicom_files
)
from src.api.query_api import find_result

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

def process_single_series(
        series,
        series_count: int,
        patient_name: str,
        series_type: int,
        base_url: str,
        cookie: str,
        upload_config: Any,
        use_series_uid: bool = False
) -> bool:
    """
    Process and upload a single DICOM series.
    """
    series_info = get_series_info(series)

    # If using series UID as patient name
    if use_series_uid:
        patient_name = series_info["PatientID"]

    series_desc = (
        f"{series_info['SeriesDescription']} "
        f"({series_info['SliceNum']} slices)"
    )
    logger.info(f"Processing Series {series_count}: {series_desc}")
    logger.info(f"Patient Name: {patient_name}")

    if not should_upload_series(series_info):
        logger.info("Series does not meet upload criteria, skipping...")
        return False

    logger.info("Series meets criteria, starting upload...")

    try:
        logger.info("[1/3] Uploading initial metadata...")
        upload_series_metadata(
            series_info, patient_name, series_type, 11, base_url, cookie, verbose=False
        )

        logger.info("[2/3] Uploading DICOM files...")
        upload_dicom_files(series, upload_config, verbose=False)
        
        logger.info("[3/3] Uploading final metadata...")
        upload_series_metadata(
            series_info, patient_name, series_type, 12, base_url, cookie, verbose=False
        )
        return True
    except Exception as e:
        logger.error(f"Series {series_count} upload failed: {e}")
        return False

async def analyze_dicom_directory(directory_path: str, series_type: int) -> Dict[str, Any]:
    """
    Analyze DICOM directory and upload series.
    """
    try:
        config = get_authenticated_config()
        
        base_url = config.get('base_url')
        cookie_val = config.get('cookie')
        
        if not base_url or not cookie_val:
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

        # Create upload configuration
        upload_config = create_upload_config(config)

        logger.info(f"Scanning DICOM directory: {directory_path}")
        dicom_directory = DICOMDirectory(directory_path)

        # Get all series
        all_series = list(dicom_directory.get_dicom_series())
        total_series = len(all_series)
        logger.info(f"Found {total_series} series")

        successful_uploads = 0
        
        # We need to determine patient_name strategy. 
        # Original code: if patient_name is None, use 'default' but set use_series_uid=True
        # Here we don't have patient_name in args, so we assume use_series_uid=True behavior
        # unless config has it? Original code checked config.get('patient_name').
        # Let's assume we use series UID if not in config.
        
        config_patient_name = config.get('patient_name')
        use_series_uid = config_patient_name is None
        patient_name = config_patient_name if config_patient_name else 'default'

        for i, series in enumerate(all_series, 1):
            if process_single_series(
                series, i, patient_name, int(series_type), 
                base_url, cookie, upload_config, use_series_uid
            ):
                successful_uploads += 1

        result = {
            "total_series": total_series,
            "successful_uploads": successful_uploads,
            "message": f"Processed {total_series} series, uploaded {successful_uploads}."
        }
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, indent=2)
            }]
        }

    except Exception as e:
        error_info = f"Error during analysis: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_info)
        return {
            "content": [{
                "type": "text",
                "text": error_info
            }]
        }

async def separate_series_by_patient(directory_path: str) -> Dict[str, Any]:
    """
    Separate DICOM files into folders by patient and series.
    """
    try:
        dicom_directory = DICOMDirectory(directory_path)
        all_series = list(dicom_directory.get_dicom_series())

        # Group by patient
        patient_series_map = {}
        for series in all_series:
            info = get_series_info(series)
            pid = info["PatientID"]
            patient_series_map.setdefault(pid, []).append(series)

        base_path = Path(directory_path)
        success_num = 0
        created_dirs = []

        for pid, series_list in patient_series_map.items():
            p_dir = base_path / pid
            p_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(p_dir))
            
            for series in series_list:
                info = get_series_info(series)
                series_uid = info.get("SeriesInstanceUID", "unknown_series")
                s_dir = p_dir / series_uid
                s_dir.mkdir(parents=True, exist_ok=True)

                for instance in getattr(series, "instances", []):
                    src = (
                        getattr(instance, "filepath", None)
                        or getattr(instance, "file_path", None)
                        or getattr(instance, "path", None)
                    )
                    if not src:
                        continue

                    try:
                        copy_dicom(src, s_dir)
                        success_num += 1
                    except Exception as e:
                        logger.warning(f"Copy failed: {src} -> {s_dir}: {e}")

        message = f"Separated {len(all_series)} series for {len(patient_series_map)} patients. Copied {success_num} files."
        result = {
            "totalPatients": len(patient_series_map),
            "totalSeries": len(all_series),
            "totalFilesCopied": success_num,
            "message": message,
            "newDirectories": created_dirs
        }
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False)
            }]
        }
    except Exception as e:
        error_info = f"Error during separation: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_info)
        return {
            "content": [{
                "type": "text",
                "text": error_info
            }]
        }

async def get_analysis_result(study_uid: str) -> Dict[str, Any]:
    """
    Poll for analysis result.
    """
    try:
        config = get_authenticated_config()
        base_url = config.get('base_url')
        cookie_val = config.get('cookie')
        
        if not base_url or not cookie_val:
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

        api_url = f"{base_url}/api/v2/getSeriesByStudyInstanceUID"
        
        logger.info(f"Querying result for StudyUID: {study_uid}")
        
        found = False
        result_data = {}
        
        # Poll for result (up to 120 seconds)
        for _ in range(120):
            # find_result returns (study_uid, series_uid, s_type, status)
            _, series_uid, s_type, status = find_result(api_url, study_uid, cookie)
            
            logger.info(f"Status: {status}")
            
            if status is not None:
                status_int = int(status)
                if status_int == 42:
                    found = True
                    result_data["url"] = f"{base_url}/viewer/{study_uid}?seriesInstanceUID={series_uid}&type={s_type}&status=42"
                    break
                elif status_int == 44:
                    # Error or finished with error? Original code breaks on 44.
                    break
                # 41 is processing?
            
            time.sleep(1)
            
        if not found:
            result_data["message"] = f"Query timeout or failed. Check system: {base_url}/study/studylist"
            
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result_data, ensure_ascii=False, indent=2)
            }]
        }

    except Exception as e:
        error_info = f"Error during result query: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_info)
        return {
            "content": [{
                "type": "text",
                "text": error_info
            }]
        }
