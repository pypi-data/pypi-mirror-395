"""
DICOM series processing functions.
"""
from typing import Dict


def should_upload_series(series_info: Dict) -> bool:
    """
    Decide whether the series meets the criteria for uploading.

    Args:
        series_info (Dict): The dictionary containing series metadata.

    Returns:
        bool: True if it should be uploaded, False otherwise.
    """
    return (
        series_info["SliceThickness"] is not None
        and series_info["SliceThickness"] <= 1
        and 100 < series_info["imageCount"] < 600
    )


def get_series_info(series) -> Dict:
    """
    Extract key DICOM tags from the series into a dictionary.

    Args:
        series (Series): The DICOM series.

    Returns:
        Dict: A dictionary containing specific DICOM metadata.
    """
    tags = [
        "SliceThickness",
        "PatientAge",
        "PatientSex",
        "PatientID",
        "PatientName",
        "SeriesInstanceUID",
        "SeriesDescription",
        "SeriesNumber",
        "StudyDate",
        "StudyInstanceUID",
    ]
    series_info = {tag: series.get_dicom_tag(tag) for tag in tags}
    series_info["SliceNum"] = series_info["imageCount"] = len(series.instances)
    return series_info


def assemble_metadata_for_upload(
    series_info: Dict, 
    hashed_name: str, 
    series_type: int, 
    upload_status: int
) -> Dict:
    """
    Assemble a SeriesMetadata dictionary from raw series information.

    Args:
        series_info: Dictionary containing series information
        hashed_name: Patient name after hashing
        series_type: An integer representing the type of series
        upload_status: The current status code for the upload

    Returns:
        Dict: A dictionary containing the formatted metadata
    """
    return {
        "SliceThickness": str(series_info["SliceThickness"]),
        "SliceNum": int(series_info["SliceNum"]),
        "imageCount": int(series_info["imageCount"]),
        "PatientAge": str(series_info["PatientAge"]),
        "PatientSex": str(series_info["PatientSex"]),
        "PatientID": str(series_info["PatientID"]),
        "PatientName": str(hashed_name),
        "SeriesInstanceUID": str(series_info["SeriesInstanceUID"]),
        "SeriesDescription": str(series_info["SeriesDescription"]),
        "SeriesNumber": int(series_info["SeriesNumber"]),
        "StudyDate": str(series_info["StudyDate"]),
        "StudyInstanceUID": str(series_info["StudyInstanceUID"]),
        "seriesName": str(series_info["SeriesDescription"]),
        "nameAfterHash": str(hashed_name),
        "seriesType": series_type,
        "status": upload_status,
    }
