"""
Upload operations for DICOM series and metadata.
"""
import time
from typing import Dict
from argparse import Namespace

from src.api.dicom_api import DICOMUploader
from src.api.metadata_api import SeriesMetadataUploader
from src.api.query_api import find_result
from .series_processor import assemble_metadata_for_upload


def upload_series_metadata(
    series_info: Dict, 
    patient_name: str, 
    series_type: int, 
    upload_status: int, 
    base_url: str, 
    cookie: str,
    verbose: bool = False
) -> Dict:
    """
    Upload series metadata to the server.
    
    Args:
        series_info: Series information dictionary
        patient_name: Patient name
        series_type: Series type
        upload_status: Upload status code
        base_url: Base URL for the API
        cookie: Authentication cookie
        verbose: Whether to print detailed output
        
    Returns:
        Dict: Metadata dictionary
    """
    metadata = assemble_metadata_for_upload(series_info, patient_name, series_type, upload_status)
    
    if verbose:
        print(f"上传元数据 (状态 {upload_status})...")
    
    uploader = SeriesMetadataUploader(base_url, cookie)
    response = uploader.upload(metadata)
    
    if verbose:
        import os
        import json
        #print(f"响应: {response}")
        try:
            os.makedirs('logs', exist_ok=True)
            filepath = os.path.join('logs', f'response_{int(time.time())}.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                try:
                    f.write(json.dumps(response, ensure_ascii=False, indent=2))
                except Exception:
                    f.write(str(response))
            if verbose:
                print(f"响应已写入: {filepath}")
        except Exception as write_err:
            if verbose:
                print(f"写入响应文件失败: {write_err}")
    
    return metadata


def upload_dicom_files(series, upload_config: Namespace, verbose: bool = False):
    """
    Upload DICOM files for a series with progress bar.
    
    Args:
        series: DICOM series object
        upload_config: Upload configuration namespace
        verbose: Whether to print detailed output
    """
    if not verbose:
        # Suppress detailed output from DICOMUploader
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
    
    try:
        upload_dcm = DICOMUploader(upload_config)
        upload_dcm.upload_series(series)
    finally:
        if not verbose:
            sys.stdout = old_stdout


def get_viewer_url(
    study_instance_uid: str, 
    api_url: str, 
    base_url: str, 
    cookie: str,
    config_series_type: int = None,
    max_attempts: int = 30,
    poll_interval: int = 2
) -> str:
    """
    Get the viewer URL for uploaded series with polling until status is 42.
    
    Args:
        study_instance_uid: Study Instance UID
        api_url: API URL for querying series
        base_url: Base URL for viewer
        cookie: Authentication cookie
        config_series_type: Series type from config (if provided, will override server response)
        max_attempts: Maximum number of polling attempts (default: 30)
        poll_interval: Seconds to wait between polls (default: 2)
        
    Returns:
        str: Viewer URL if status reaches 42, None otherwise
    """
    from tqdm import tqdm
    
    # Initialize variables
    study_uid = series_uid = series_type = status = None
    
    with tqdm(total=max_attempts, desc="等待服务器处理", unit="次", ncols=80) as pbar:
        for attempt in range(max_attempts):
            try:
                study_uid, series_uid, series_type, status = find_result(
                    api_url, study_instance_uid, cookie
                )
                
                # Use config series_type if provided, otherwise use server response
                if config_series_type is not None:
                    series_type = config_series_type
                
                # Update progress bar description based on status
                if status == 42:
                    pbar.set_description("[完成] 处理完成")
                    pbar.update(max_attempts - attempt)  # Complete the bar
                    viewer_url = (
                        f'{base_url}viewer/{study_uid}'
                        f'?seriesInstanceUID={series_uid}'
                        f'&type={series_type}'
                        f'&status={status}'
                    )
                    return viewer_url
                elif status == 41:
                    pbar.set_description(f"[处理中] 状态:{status}")
                else:
                    pbar.set_description(f"[警告] 异常状态:{status}")
                
                pbar.update(1)
                
                if attempt < max_attempts - 1:
                    time.sleep(poll_interval)
                    
            except Exception as e:
                pbar.set_description(f"[错误] 查询错误")
                pbar.update(1)
                if attempt < max_attempts - 1:
                    time.sleep(poll_interval)
    
    # Timeout - return URL anyway
    print(f"\n[警告] 超时后状态为 {status}, 未达到完成状态(42)")
    if study_uid and series_uid:
        # Use config series_type if provided, otherwise use server response
        if config_series_type is not None:
            series_type = config_series_type
        viewer_url = (
            f'{base_url}viewer/{study_uid}'
            f'?seriesInstanceUID={series_uid}'
            f'&type={series_type}'
            f'&status={status}'
        )
        return viewer_url
    return None
