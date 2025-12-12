"""
单文件解析工具

解析单个DICOM文件，提取关键信息
"""

import json
import logging
from typing import Dict, Any

from .utils import parse_dicom_file
from .types import ToolOutput

logger = logging.getLogger(__name__)


async def parse_dicom_file_tool(file_path: str) -> ToolOutput:
    """
    解析单个 DICOM 文件，提取 PatientID、PatientName、SeriesInstanceUID、SeriesDescription 等关键信息
    
    Args:
        file_path: DICOM 文件的路径
        
    Returns:
        ToolOutput: 包含DICOM文件信息的工具输出
    """
    try:
        dicom_info = parse_dicom_file(file_path)
        
        if not dicom_info:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "error": True,
                            "message": f"文件不是标准的 DICOM 文件（前 128 字节后没有 'DICM' 标识）: {file_path}"
                        }, ensure_ascii=False)
                    }
                ]
            }
            
        # 转换为字典格式
        result = {
            "filePath": dicom_info.file_path,
            "PatientID": dicom_info.patient_id,
            "PatientName": dicom_info.patient_name,
            "SeriesInstanceUID": dicom_info.series_instance_uid,
            "SeriesDescription": dicom_info.series_description
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
        logger.error(f"解析DICOM文件失败: {error_message}")
        
        return {
            "content": [
                {
                    "type": "text", 
                    "text": json.dumps({
                        "error": True,
                        "message": f"解析 DICOM 文件失败: {error_message}"
                    }, ensure_ascii=False)
                }
            ]
        }