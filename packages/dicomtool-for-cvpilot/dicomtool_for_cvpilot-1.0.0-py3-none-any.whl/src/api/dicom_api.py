"""
DICOM uploader module.

This module provides functionality for uploading DICOM files to the Orthanc server.
"""

import os
import time
from typing import Dict, Any, List, Optional, TypedDict
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

import requests
from requests import RequestException, Timeout
from requests.adapters import HTTPAdapter
from pyorthanc import Orthanc


class UploadData(TypedDict):
    filepath: str


class UploadResponse(TypedDict):
    success: bool
    response: Dict[str, Any]


class DICOMUploader:
    """Class for uploading DICOM files to Orthanc server."""

    def __init__(self, config):
        """
        Initialize the DICOM uploader.

        Args:
            config: Configuration namespace with orthanc settings
        """

        self.config = config
        self.session = self._init_session()
        # Normalize base_url and compute the correct instances endpoint.
        # The final endpoint should look like: http://host:port/api/v1/orthanc/instances/
        base_url = str(config.base_url).rstrip('/')
        # Ensure the base path for API exists
        if '/api/v1/orthanc' not in base_url:
            # Assuming a base like http://localhost:29999, append the standard API path
            base_url = f"{base_url}/api/v1/orthanc"

        # Construct the instances endpoint, ensuring it ends with /instances/
        self.instances_endpoint = f"{base_url.split('/instances')[0].rstrip('/')}/instances/"

        self.DEFAULT_CONNECT_TIMEOUT = int(config.DEFAULT_CONNECT_TIMEOUT)
        self.DEFAULT_READ_TIMEOUT = int(config.DEFAULT_READ_TIMEOUT)
        self.DEFAULT_RETRY_DELAY = int(config.DEFAULT_RETRY_DELAY)
        self.DEFAULT_BATCH_SIZE = int(config.DEFAULT_BATCH_SIZE)

    def _init_session(self) -> requests.Session:
        """
        Create and configure the requests session.

        Returns:
            requests.Session: Configured session.
        """
        session = requests.Session()
        # Put cookie into session headers (if provided). Keep key lowercase as in config.
        cookie_value = getattr(self.config, 'cookie', None)
        if cookie_value:
            # Keep Cookie header for compatibility
            session.headers.update({"Cookie": cookie_value})
            # Also populate session.cookie_jar for requests to send cookies properly.
            # cookie_value may be like 'ls=xxxxx' or 'k1=v1; k2=v2'
            try:
                parts = [p.strip() for p in cookie_value.split(';') if p.strip()]
                for part in parts:
                    if '=' in part:
                        k, v = part.split('=', 1)
                        session.cookies.set(k.strip(), v.strip())
            except Exception:
                # If parsing fails, keep header-only approach.
                pass
        adapter = HTTPAdapter(
            max_retries=self.config.max_retries,
            pool_connections=self.config.max_workers,
            pool_maxsize=self.config.max_workers,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def validate(self, data: UploadData) -> bool:
        """
        Validate the data before upload.

        Args:
            data: Dictionary containing the file path.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        filepath = data.get("filepath")
        if not filepath or not isinstance(filepath, str):
            return False
        return os.path.exists(filepath)

    def upload(self, data: UploadData) -> UploadResponse:
        """
        Perform the actual upload request.

        Args:
            data: Dictionary containing the file path.

        Returns:
            UploadResponse: Dictionary containing success flag and response data.

        Raises:
            ValueError: If validation fails.
            Exception: If upload fails with a non-200 status.
        """
        if not self.validate(data):
            raise ValueError(f"Invalid data: {data}")

        filepath = data["filepath"].replace(r'\\', r'/')

        try:
            # Open file and POST to the computed instances endpoint.
            with open(filepath, "rb") as f:
                files = {'file': (filepath, f, 'application/octet-stream')}
                # Let requests set the Content-Type header for multipart/form-data automatically.
                # Only set the Accept header.
                headers = {"Accept": "application/json, text/plain, */*"}
                endpoint = self.instances_endpoint
                # Debugging output
                print(f"DEBUG: Uploading {filepath} to {endpoint}")
                response = self.session.post(
                    endpoint,
                    files=files,
                    headers=headers,
                    timeout=(self.DEFAULT_CONNECT_TIMEOUT, self.DEFAULT_READ_TIMEOUT)
                )

            # Orthanc may return 200 or 201 depending on the API/version; accept both as success.
            if response.status_code in (200, 201):
                # Check if response content is empty
                if not response.text:
                    return {"success": True, "response": {}}

                # Try to parse JSON
                try:
                    json_response = response.json()
                    return {"success": True, "response": json_response}
                except ValueError:
                    # If cannot parse JSON, return raw text
                    return {"success": True, "response": {"text": response.text}}

            # Non-200 status code is considered a failed upload
            print(f"DEBUG: Request URL: {response.request.url}")
            print(f"DEBUG: Request Headers: {response.request.headers}")
            print(f"DEBUG: Response status: {response.status_code}, body: {response.text}")
            raise Exception(f"Upload failed with status {response.status_code}: {response.text}")

        except Exception as e:
            # Re-raise while preserving stack trace; additional logging can be added here.
            raise

    def _upload_single_file(self, filepath: str) -> bool:
        """
        Upload a single DICOM file without retry logic.

        Args:
            filepath: Path to the DICOM file.

        Returns:
            bool: True if upload successful, False otherwise.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If the upload fails.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        result = self.upload({"filepath": filepath})
        return result["success"]

    def _upload_file_with_retry(self, filepath: str, attempt: int = 1) -> bool:
        """
        Upload a single DICOM file with retry logic.

        Args:
            filepath: Path to the DICOM file.
            attempt: Current attempt number.

        Returns:
            bool: True if upload is successful, False otherwise.

        Raises:
            Exception: If the upload fails after all retries.
        """
        try:
            return self._upload_single_file(filepath)

        except (Timeout, RequestException) as e:
            if attempt < self.config.max_retries:
                time.sleep(self.DEFAULT_RETRY_DELAY)
                return self._upload_file_with_retry(filepath, attempt + 1)
            raise Exception(f"Upload failed after {attempt} attempts: {str(e)}")

        except Exception as e:
            if attempt < self.config.max_retries:
                time.sleep(self.DEFAULT_RETRY_DELAY)
                return self._upload_file_with_retry(filepath, attempt + 1)
            raise Exception(f"Upload failed after {attempt} attempts: {str(e)}")

    def upload_file(self, filepath: str) -> bool:
        """
        Public method to upload a single DICOM file with retries.

        Args:
            filepath: Path to the DICOM file.

        Returns:
            bool: True if upload is successful, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            Exception: If upload fails.
        """
        return self._upload_file_with_retry(filepath)

    def upload_series(self, series) -> List[bool]:
        """
        Upload all DICOM files in a series using batched processing.

        Args:
            series: Series object containing DICOM instances.

        Returns:
            List[bool]: A list indicating success for each file.

        Raises:
            Exception: If critical upload failures occur.
        """
        from tqdm import tqdm

        results = []
        total_files = len(series.instances)
        processed_files = 0
        print()
        print(series.instances[0].filepath)
        # Create progress bar for file uploads
        with tqdm(total=total_files, desc="上传DICOM文件", unit="个", ncols=80) as pbar:
            for batch_start in range(0, total_files, self.DEFAULT_BATCH_SIZE):
                batch_end = min(batch_start + self.DEFAULT_BATCH_SIZE, total_files)
                batch = series.instances[batch_start:batch_end]

                with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                    futures: Dict[Future[bool], str] = {
                        executor.submit(self.upload_file, instance.filepath): instance.filepath
                        for instance in batch
                    }

                    for future in as_completed(futures):
                        filepath = futures[future]
                        try:
                            success = future.result()
                            results.append(success)
                            processed_files += 1

                            # Update progress bar
                            if success:
                                pbar.set_description("上传DICOM文件 [成功]")
                            else:
                                pbar.set_description("上传DICOM文件 [失败]")
                            pbar.update(1)

                        except Exception:
                            results.append(False)
                            processed_files += 1
                            pbar.set_description("上传DICOM文件 [失败]")
                            pbar.update(1)

                            # Check if we should abort (failure rate > 50%)
                            failure_rate = results.count(False) / len(results)
                            if failure_rate > 0.5:
                                pbar.close()
                                raise Exception(
                                    f"上传失败: 超过50%的文件失败 "
                                    f"({results.count(False)}/{len(results)})"
                                )

                # Add a small delay between batches
                if batch_end < total_files:
                    time.sleep(0.5)

        successful_uploads = sum(1 for r in results if r)
        print(f"\n上传完成: {successful_uploads}/{total_files} 个文件成功")

        return results
