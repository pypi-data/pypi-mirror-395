"""
Core package initialization.
"""
from .series_processor import should_upload_series, get_series_info, assemble_metadata_for_upload
from .uploader import upload_series_metadata, upload_dicom_files, get_viewer_url

__all__ = [
    'should_upload_series',
    'get_series_info',
    'assemble_metadata_for_upload',
    'upload_series_metadata',
    'upload_dicom_files',
    'get_viewer_url'
]
