"""
Query API module for querying series status from the server.
"""
import json
import sys
import requests
from typing import Tuple, Optional


def find_result(
    url: str, 
    study_instance_uid: str, 
    cookie: str
) -> Tuple[Optional[str], Optional[str], Optional[int], Optional[int]]:
    """
    Query series information by StudyInstanceUID.
    
    Args:
        url: API endpoint URL
        study_instance_uid: Study Instance UID to query
        cookie: Authentication cookie
        
    Returns:
        Tuple containing (StudyInstanceUID, SeriesInstanceUID, seriesType, status)
        or (None, None, None, None) if request fails
    """
    # Request headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"i18next=zh-CN; {cookie}",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "lang": "zh-CN"
    }

    # Request body data
    payload = {
        "StudyInstanceUID": study_instance_uid
    }

    # Send POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Try to parse JSON response
        response_data = response.json()
        response_data = response_data['data'][0]
        study_uid = response_data['StudyInstanceUID']
        series_uid = response_data['SeriesInstanceUID']
        series_type = response_data['seriesType']
        status = response_data['status']

        return study_uid, series_uid, series_type, status

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return None, None, None, None
    except (KeyError, IndexError) as e:
        print(f"Failed to parse response: {e}", file=sys.stderr)
        return None, None, None, None
