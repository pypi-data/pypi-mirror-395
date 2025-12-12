"""
DICOM Tools Package

提供DICOM医学影像文件分析的核心功能。
"""

from .types import (
    DicomFileInfo,
    SeriesInfo,
    PatientInfo,
    DicomStatistics,
    ScanSummary,
    ToolOutput
)

from .utils import (
    is_standard_dicom_file,
    get_all_files,
    parse_dicom_file,
    scan_dicom_directory,
    format_dicom_statistics_as_json,
    format_dicom_statistics_as_compact_json,
    generate_patient_series_file_mapping
)

__version__ = "1.0.1"
__author__ = "himozzie@gmail.com"

__all__ = [
    # Types
    'DicomFileInfo',
    'SeriesInfo', 
    'PatientInfo',
    'DicomStatistics',
    'ScanSummary',
    'ToolOutput',
    
    # Utils
    'is_standard_dicom_file',
    'get_all_files',
    'parse_dicom_file',
    'scan_dicom_directory', 
    'format_dicom_statistics_as_json',
    'format_dicom_statistics_as_compact_json',
    'generate_patient_series_file_mapping'
]