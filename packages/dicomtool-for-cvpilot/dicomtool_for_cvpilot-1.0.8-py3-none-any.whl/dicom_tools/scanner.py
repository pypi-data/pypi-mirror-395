"""
目录扫描工具

基础扫描工具 - 只负责扫描和基础统计
"""

import json
import logging
from typing import Dict, Any

from .utils import scan_dicom_directory
from .types import ScanSummary, ToolOutput

logger = logging.getLogger(__name__)


async def scan_dicom_directory_tool(directory_path: str) -> ToolOutput:
    """
    扫描指定目录下的所有 DICOM 文件，返回统计摘要
    
    Args:
        directory_path: 要扫描的目录路径
        
    Returns:
        ToolOutput: 包含统计摘要的工具输出
    """
    try:
        statistics = scan_dicom_directory(directory_path)
        
        # 只返回统计摘要，不返回详细信息（避免token浪费）
        patient_list = []
        for patient_id, patient_info in statistics.patients.items():
            patient_list.append({
                "id": patient_id,
                "name": patient_info.patient_name,
                "seriesCount": len(patient_info.series)
            })
            
        result = {
            "totalFiles": statistics.total_files,
            "totalPatients": statistics.total_patients,
            "totalSeries": statistics.total_series,
            "patientCount": len(statistics.patients),
            "patientList": patient_list
        }
        
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
        logger.error(f"扫描DICOM目录失败: {error_message}")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "error": True,
                        "message": f"扫描 DICOM 目录失败: {error_message}"
                    }, ensure_ascii=False)
                }
            ]
        }