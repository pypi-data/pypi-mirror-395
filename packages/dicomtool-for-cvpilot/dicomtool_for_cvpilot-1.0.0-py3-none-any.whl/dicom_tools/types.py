"""
DICOM 工具数据类型定义

定义了DICOM文件解析和处理过程中使用的所有数据结构。
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DicomFileInfo:
    """DICOM 文件信息"""
    file_path: str
    patient_id: str
    patient_name: str
    series_instance_uid: str
    series_description: str


@dataclass 
class SeriesInfo:
    """序列信息"""
    series_instance_uid: str
    series_description: str
    file_count: int
    dir_path: str  # 公共父目录路径
    file_names: List[str] = field(default_factory=list)  # 仅文件名


@dataclass
class PatientInfo:
    """患者信息"""
    patient_id: str
    patient_name: str
    series: Dict[str, SeriesInfo] = field(default_factory=dict)


@dataclass
class DicomStatistics:
    """DICOM 统计信息"""
    total_files: int
    total_patients: int
    total_series: int
    patients: Dict[str, PatientInfo] = field(default_factory=dict)


@dataclass
class SeriesInfoOutput:
    """格式化输出的序列信息（用于节省token）"""
    series_instance_uid: str
    series_description: str
    file_count: int
    files: str  # JSON字符串格式的文件路径数组


@dataclass
class PatientInfoOutput:
    """输出格式的患者信息"""
    patient_id: str
    patient_name: str
    series_count: int
    series: List[SeriesInfoOutput] = field(default_factory=list)


@dataclass
class ScanSummary:
    """扫描摘要（用于基础统计工具）"""
    total_files: int
    total_patients: int
    total_series: int
    patient_count: int
    patient_list: List[Dict[str, any]] = field(default_factory=list)


# 工具输出格式类型
ToolOutput = Dict[str, any]