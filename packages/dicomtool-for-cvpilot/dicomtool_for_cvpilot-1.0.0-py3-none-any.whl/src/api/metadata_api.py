"""
Metadata uploader module.

This module provides functionality for uploading series metadata to the server,
including series information and status updates.
"""

import json
from typing import Dict, Any, TypedDict, Union
import requests
from requests.exceptions import RequestException


class SeriesMetadata(TypedDict):
    """TypedDict for series metadata."""
    SliceThickness: str
    SliceNum: int
    imageCount: int
    PatientAge: str
    PatientSex: str
    PatientID: str
    PatientName: str
    SeriesInstanceUID: str
    SeriesDescription: str
    SeriesNumber: int
    StudyDate: str
    StudyInstanceUID: str
    seriesName: str
    nameAfterHash: str
    seriesType: int
    status: int


class SeriesInfo(TypedDict):
    """TypedDict for raw series information."""
    SliceThickness: Union[float, str]
    SliceNum: Union[int, str]
    imageCount: Union[int, str]
    PatientAge: str
    PatientSex: str
    PatientID: str
    SeriesInstanceUID: str
    SeriesDescription: str
    SeriesNumber: Union[int, str]
    StudyDate: str
    StudyInstanceUID: str


class SeriesMetadataUploader:
    """
    Class for uploading series metadata to the server.

    This class handles the upload of series metadata, including
    patient information and series details.
    """

    ENDPOINT = "/api/v1/uploadData"

    def __init__(self, base_url: str, cookie: str):
        """
        Initialize the uploader with configuration.

        Args:
            base_url: Base URL of the API server
            cookie: Authentication cookie
        """
        self.base_url = base_url
        self.cookie = cookie

    def _is_metadata_valid(self, series_metadata: SeriesMetadata) -> bool:
        """
        Check if the provided metadata contains all required fields.

        Args:
            series_metadata: Dictionary containing metadata to validate

        Returns:
            bool: True if metadata is valid, False otherwise
        """
        required_fields = [
            "SeriesInstanceUID",
            "StudyInstanceUID",
            "PatientID",
            "nameAfterHash",
            "seriesType",
            "status"
        ]
        return all(series_metadata.get(field) is not None for field in required_fields)

    def _create_request_headers(self) -> Dict[str, str]:
        """
        Build request headers for metadata upload.

        Returns:
            A dictionary containing the headers for the request.
        """
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "pragma": "no-cache",
        }
        if self.cookie:
            headers["cookie"] = self.cookie
        return headers

    def _send_metadata_request(
            self,
            series_metadata: SeriesMetadata,
            request_headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Send the metadata upload request to the server.

        Args:
            series_metadata: Metadata to be uploaded
            request_headers: Request headers

        Returns:
            The JSON response from the server

        Raises:
            RequestException: If the upload fails
        """
        try:
            print("*" * 120)
            print(series_metadata)
            print("*" * 120)
            response = requests.post(
                f"{self.base_url}{self.ENDPOINT}",
                headers=request_headers,
                data=json.dumps(series_metadata)
            )
            response.raise_for_status()
            return response.json()

        except RequestException as exc:
            print(f"RequestException during metadata upload: {exc}")
            raise
        except Exception as exc:
            print(f"Unexpected error during metadata upload: {exc}")
            raise

    def _process_upload_response(self, response_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the server response after metadata upload.

        Args:
            response_content: Dictionary containing the response data from the server

        Returns:
            The response data if no errors are detected
        """
        # code=1000 indicates a login/session expiration
        if response_content.get('code') == 1000:
            raise Exception(response_content.get('msg', '您未登录或登录已过期'))
        return response_content

    def upload(self, series_metadata: SeriesMetadata) -> Dict[str, Any]:
        """
        Upload the provided series metadata to the server.

        Args:
            series_metadata: Dictionary containing metadata to upload

        Returns:
            Dict containing the server's response

        Raises:
            ValueError: If metadata validation fails
            RequestException: If the request fails
        """
        # 1. Validate metadata before upload
        if not self._is_metadata_valid(series_metadata):
            raise ValueError("Invalid metadata")

        # 2. Build request headers
        request_headers = self._create_request_headers()

        # 3. Send the metadata upload request
        response_data = self._send_metadata_request(series_metadata, request_headers)

        # 4. Process and return the response
        return self._process_upload_response(response_data)
