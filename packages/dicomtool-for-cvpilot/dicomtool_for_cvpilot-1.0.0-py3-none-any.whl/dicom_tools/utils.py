"""
DICOM 工具核心功能函数

提供DICOM文件识别、解析、目录扫描等核心功能。
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pydicom
from pydicom.errors import InvalidDicomError
import json
import logging

from .types import DicomFileInfo, DicomStatistics, PatientInfo, SeriesInfo

# 设置日志
logger = logging.getLogger(__name__)


def is_standard_dicom_file(file_path: str) -> bool:
    """
    检查文件是否为标准 DICOM 文件
    标准 DICOM 文件的前 128 字节是前导码，第 129-132 字节应该是 "DICM"
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 是否为标准DICOM文件
    """
    try:
        with open(file_path, 'rb') as f:
            # 读取前132字节
            header = f.read(132)
            
            if len(header) < 132:
                return False
                
            # 检查第128-131字节（索引从0开始）是否为"DICM"
            magic_word = header[128:132].decode('ascii', errors='ignore')
            return magic_word == 'DICM'
            
    except (IOError, OSError, UnicodeDecodeError):
        return False


def get_all_files(dir_path: str) -> List[str]:
    """
    递归扫描目录下所有文件
    
    Args:
        dir_path: 目录路径
        
    Returns:
        List[str]: 所有文件路径列表
    """
    files = []
    
    try:
        path_obj = Path(dir_path)
        if not path_obj.exists() or not path_obj.is_dir():
            logger.error(f"目录不存在或不是目录: {dir_path}")
            return files
            
        # 递归遍历所有文件
        for item in path_obj.rglob('*'):
            if item.is_file():
                files.append(str(item.absolute()))
                
    except Exception as e:
        logger.error(f"读取目录失败: {dir_path}, 错误: {e}")
        
    return files


def parse_dicom_file(file_path: str) -> Optional[DicomFileInfo]:
    """
    解析 DICOM 文件并提取关键信息
    
    Args:
        file_path: DICOM文件路径
        
    Returns:
        Optional[DicomFileInfo]: 解析成功返回文件信息，失败返回None
    """
    try:
        # 首先检查是否为标准DICOM文件
        if not is_standard_dicom_file(file_path):
            return None
            
        # 使用pydicom解析DICOM文件
        ds = pydicom.dcmread(file_path, force=True)
        
        # 提取关键信息
        # (0010,0020) = Patient ID
        # (0010,0010) = Patient Name
        # (0020,000E) = Series Instance UID  
        # (0008,103E) = Series Description
        
        patient_id = getattr(ds, 'PatientID', 'UNKNOWN')
        patient_name = str(getattr(ds, 'PatientName', 'UNKNOWN'))
        series_instance_uid = getattr(ds, 'SeriesInstanceUID', 'UNKNOWN')
        series_description = getattr(ds, 'SeriesDescription', 'UNKNOWN')
        
        return DicomFileInfo(
            file_path=file_path,
            patient_id=patient_id,
            patient_name=patient_name,
            series_instance_uid=series_instance_uid,
            series_description=series_description
        )
        
    except (InvalidDicomError, Exception) as e:
        logger.debug(f"解析DICOM文件失败: {file_path}, 错误: {e}")
        return None


def get_common_dir_path(file_paths: List[str]) -> str:
    """
    提取一组路径的公共父目录
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        str: 公共父目录路径
    """
    if not file_paths:
        return ''
    if len(file_paths) == 1:
        return str(Path(file_paths[0]).parent)
        
    # 将所有路径转为Path对象并获取父目录
    dirs = [Path(p).parent for p in file_paths]
    
    # 获取第一个路径的parts作为基准
    common_parts = list(dirs[0].parts)
    
    # 与其他路径比较，保留公共部分
    for dir_path in dirs[1:]:
        current_parts = list(dir_path.parts)
        
        # 找到公共前缀的长度
        common_length = 0
        for i in range(min(len(common_parts), len(current_parts))):
            if common_parts[i] == current_parts[i]:
                common_length = i + 1
            else:
                break
                
        # 截取公共部分
        common_parts = common_parts[:common_length]
        
    # 重建路径
    if common_parts:
        return str(Path(*common_parts))
    else:
        return str(Path.cwd().anchor)  # 返回根目录


def scan_dicom_directory(dir_path: str) -> DicomStatistics:
    """
    扫描目录并分析所有 DICOM 文件
    
    Args:
        dir_path: 要扫描的目录路径
        
    Returns:
        DicomStatistics: 扫描统计结果
        
    Raises:
        ValueError: 当目录不存在或不是目录时
    """
    # 检查目录是否存在
    path_obj = Path(dir_path)
    if not path_obj.exists():
        raise ValueError(f"目录不存在: {dir_path}")
    if not path_obj.is_dir():
        raise ValueError(f"路径不是目录: {dir_path}")
        
    # 获取所有文件
    all_files = get_all_files(dir_path)
    
    # 存储患者、序列的层级结构
    patients: Dict[str, PatientInfo] = {}
    # 临时存储：series_key -> 文件路径列表
    series_file_paths: Dict[str, List[str]] = {}
    total_files = 0
    
    # 逐个解析文件
    for file_path in all_files:
        dicom_info = parse_dicom_file(file_path)
        
        if not dicom_info:
            continue  # 跳过非DICOM文件
            
        total_files += 1
        
        patient_id = dicom_info.patient_id
        patient_name = dicom_info.patient_name
        series_instance_uid = dicom_info.series_instance_uid
        series_description = dicom_info.series_description
        
        series_key = f"{patient_id}|{series_instance_uid}"
        
        # 存储文件路径用于后续提取公共路径
        if series_key not in series_file_paths:
            series_file_paths[series_key] = []
        series_file_paths[series_key].append(file_path)
        
        # 获取或创建患者信息
        if patient_id not in patients:
            patients[patient_id] = PatientInfo(
                patient_id=patient_id,
                patient_name=patient_name
            )
            
        patient = patients[patient_id]
        
        # 获取或创建序列信息
        if series_instance_uid not in patient.series:
            patient.series[series_instance_uid] = SeriesInfo(
                series_instance_uid=series_instance_uid,
                series_description=series_description,
                file_count=0,
                dir_path='',
                file_names=[]
            )
            
        series = patient.series[series_instance_uid]
        series.file_count += 1
        
    # 提取公共路径并设置文件名
    for series_key, file_paths in series_file_paths.items():
        patient_id, series_instance_uid = series_key.split('|', 1)
        patient = patients[patient_id]
        series = patient.series[series_instance_uid]
        
        common_dir = get_common_dir_path(file_paths)
        series.dir_path = common_dir
        series.file_names = [Path(p).name for p in file_paths]
        
    # 计算统计信息
    total_series = sum(len(patient.series) for patient in patients.values())
    
    return DicomStatistics(
        total_files=total_files,
        total_patients=len(patients),
        total_series=total_series,
        patients=patients
    )


def format_dicom_statistics_as_json(stats: DicomStatistics) -> str:
    """
    将DICOM统计信息转换为优化的JSON格式（合并文件路径以节省token）
    
    Args:
        stats: DICOM统计信息
        
    Returns:
        str: JSON格式字符串
    """
    output = []
    
    for patient_id, patient_info in stats.patients.items():
        series_list = []
        for series_uid, series_info in patient_info.series.items():
            # 重建完整路径
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
            
        output.append({
            "PatientID": patient_id,
            "PatientName": patient_info.patient_name,
            "seriesCount": len(patient_info.series),
            "series": series_list
        })
        
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_dicom_statistics_as_compact_json(stats: DicomStatistics) -> str:
    """
    精简版 JSON 导出 - 减少 token 消耗
    使用缩短的字段名
    
    Args:
        stats: DICOM统计信息
        
    Returns:
        str: 紧凑JSON格式字符串
    """
    output = []
    
    for patient_id, patient_info in stats.patients.items():
        series_list = []
        for series_uid, series_info in patient_info.series.items():
            # 重建完整路径
            full_paths = [
                str(Path(series_info.dir_path) / filename)
                for filename in series_info.file_names
            ]
            
            series_list.append({
                "sid": series_uid,
                "sname": series_info.series_description, 
                "fc": len(full_paths),
                "f": full_paths
            })
            
        output.append({
            "pid": patient_id,
            "pname": patient_info.patient_name,
            "scs": len(patient_info.series),
            "ser": series_list
        })
        
    return json.dumps(output, ensure_ascii=False)


def generate_patient_series_file_mapping(stats: DicomStatistics) -> Dict[str, str]:
    """
    生成优化的患者序列文件路径映射（格式：患者ID|序列UID|文件路径）
    
    Args:
        stats: DICOM统计信息
        
    Returns:
        Dict[str, str]: 映射字典
    """
    mapping = {}
    
    for patient_id, patient_info in stats.patients.items():
        for series_uid, series_info in patient_info.series.items():
            key = f"{patient_id}|{series_uid}"
            
            # 重建完整路径
            full_paths = [
                str(Path(series_info.dir_path) / filename)
                for filename in series_info.file_names  
            ]
            
            mapping[key] = json.dumps(full_paths, ensure_ascii=False)
            
    return mapping