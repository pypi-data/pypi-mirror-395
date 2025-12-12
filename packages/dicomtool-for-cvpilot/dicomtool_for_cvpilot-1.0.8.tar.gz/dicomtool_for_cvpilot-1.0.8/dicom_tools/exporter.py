"""
JSON导出工具

导出完整的DICOM扫描结果为JSON格式
"""

import json
import logging
from typing import Dict, Any

from .utils import scan_dicom_directory, format_dicom_statistics_as_json, format_dicom_statistics_as_compact_json
from .types import ToolOutput

logger = logging.getLogger(__name__)


async def export_dicom_json_tool(directory_path: str) -> ToolOutput:
    """
    导出完整的DICOM扫描结果为JSON格式
    
    Args:
        directory_path: 要扫描的目录路径
        
    Returns:
        ToolOutput: 包含完整JSON数据的工具输出
    """
    try:
        statistics = scan_dicom_directory(directory_path)
        
        # 使用标准JSON格式导出
        json_result = format_dicom_statistics_as_json(statistics)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json_result
                }
            ]
        }
        
    except Exception as error:
        error_message = str(error)
        logger.error(f"导出DICOM JSON失败: {error_message}")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "error": True,
                        "message": f"导出 DICOM JSON 失败: {error_message}"
                    }, ensure_ascii=False)
                }
            ]
        }


async def export_dicom_compact_json_tool(directory_path: str) -> ToolOutput:
    """
    导出紧凑格式的DICOM扫描结果（减少token消耗）
    
    Args:
        directory_path: 要扫描的目录路径
        
    Returns:
        ToolOutput: 包含紧凑JSON数据的工具输出
    """
    try:
        statistics = scan_dicom_directory(directory_path)
        
        # 使用紧凑JSON格式导出
        json_result = format_dicom_statistics_as_compact_json(statistics)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json_result
                }
            ]
        }
        
    except Exception as error:
        error_message = str(error)
        logger.error(f"导出紧凑DICOM JSON失败: {error_message}")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "error": True,
                        "message": f"导出紧凑 DICOM JSON 失败: {error_message}"
                    }, ensure_ascii=False)
                }
            ]
        }