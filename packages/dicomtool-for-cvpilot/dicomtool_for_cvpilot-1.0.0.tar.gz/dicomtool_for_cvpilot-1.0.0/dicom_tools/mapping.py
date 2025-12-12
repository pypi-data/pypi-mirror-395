"""
序列映射工具

生成患者-序列的详细映射关系
"""

import json
import logging
from typing import Dict, Any
from pathlib import Path

from .utils import scan_dicom_directory
from .types import ToolOutput

logger = logging.getLogger(__name__)


async def series_mapping_tool(directory_path: str) -> ToolOutput:
    """
    生成患者-序列的详细映射关系
    
    Args:
        directory_path: 要扫描的目录路径
        
    Returns:
        ToolOutput: 包含序列映射的工具输出
    """
    try:
        statistics = scan_dicom_directory(directory_path)
        
        # 生成序列映射
        result = []
        for patient_id, patient_info in statistics.patients.items():
            series_list = []
            for series_uid, series_info in patient_info.series.items():
                # 重建完整文件路径
                full_paths = [
                    str(Path(series_info.dir_path) / filename)
                    for filename in series_info.file_names
                ]
                
                series_list.append({
                    "SeriesInstanceUID": series_uid,
                    "SeriesDescription": series_info.series_description,
                    "fileCount": series_info.file_count,
                    "files": full_paths
                })
                
            result.append({
                "PatientID": patient_id,
                "PatientName": patient_info.patient_name,
                "seriesCount": len(patient_info.series),
                "series": series_list
            })
            
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2, ensure_ascii=False)
                }
            ]
        }
        
    except Exception as error:
        error_message = str(error)
        logger.error(f"生成序列映射失败: {error_message}")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "error": True,
                        "message": f"生成序列映射失败: {error_message}"
                    }, ensure_ascii=False)
                }
            ]
        }


async def file_mapping_tool(directory_path: str) -> ToolOutput:
    """
    生成优化的文件路径映射（格式：患者ID|序列UID -> 文件路径列表）
    
    Args:
        directory_path: 要扫描的目录路径
        
    Returns:
        ToolOutput: 包含文件映射的工具输出  
    """
    try:
        statistics = scan_dicom_directory(directory_path)
        
        # 生成文件路径映射
        mapping = {}
        for patient_id, patient_info in statistics.patients.items():
            for series_uid, series_info in patient_info.series.items():
                key = f"{patient_id}|{series_uid}"
                
                # 重建完整文件路径
                full_paths = [
                    str(Path(series_info.dir_path) / filename) 
                    for filename in series_info.file_names
                ]
                
                mapping[key] = full_paths
                
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(mapping, indent=2, ensure_ascii=False)
                }
            ]
        }
        
    except Exception as error:
        error_message = str(error)
        logger.error(f"生成文件映射失败: {error_message}")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "error": True,
                        "message": f"生成文件映射失败: {error_message}"
                    }, ensure_ascii=False)
                }
            ]
        }