import json
import csv
import sys
from pathlib import Path
from argparse import Namespace
from ..models import DICOMDirectory
from ..utils import create_upload_config
from ..core import upload_series_metadata, upload_dicom_files
from ..core.series_processor import get_series_info, should_upload_series

def log_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def process_single_series(series,series_count: int,patient_name: str,series_type: int,base_url: str,cookie: str,upload_config: Namespace,api_url,use_series_uid: bool = False) -> bool:
    """
    Process and upload a single DICOM series.

    Args:
        series: DICOM series object
        series_count: Series counter
        patient_name: Patient name
        series_type: Series type
        base_url: Base URL
        cookie: Authentication cookie
        upload_config: Upload configuration
        api_url: API URL for querying
        use_series_uid: Whether to use series UID as patient name

    Returns:
        bool: True if processed successfully, False otherwise
    """
    series_info = get_series_info(series)

    # 如果需要使用 series UID，则覆盖 patient_name
    if use_series_uid:
        patient_name = series_info["PatientID"]

    series_desc = (
        f"{series_info['SeriesDescription']} "
        f"({series_info['SliceNum']} 切片)"
    )
    log_print(f"\n{'=' * 60}")
    log_print(f"序列 {series_count}: {series_desc}")
    log_print(f"Patient Name: {patient_name}")
    log_print(f"{'=' * 60}")

    if not should_upload_series(series_info):
        log_print("X 序列不符合上传标准，跳过...")
        return False

    log_print("* 符合标准，开始上传流程...\n")

    # Step 1: Upload initial metadata (status 11)
    try:
        log_print("[1/3] 上传初始元数据...")
        metadata = upload_series_metadata(
            series_info, patient_name, series_type, 11, base_url, cookie, verbose=False
        )

        log_print("\n[2/3] 上传DICOM文件...")
        upload_dicom_files(series, upload_config, verbose=False)
        log_print("\n[3/3] 上传最终元数据...")
        metadata = upload_series_metadata(
            series_info, patient_name, series_type, 12, base_url, cookie, verbose=False
        )
        return True
    except Exception as e:
        log_print(f"\n[错误] 序列 {series_count} 上传失败: {e}\n")
        return False
def update_csv_status(directory_path, series_info, status):
    csv_path = Path(directory_path) / "文件拆分信息.csv"
    
    # Fields required for creation
    fieldnames = [
        "PatientID", "PatientName", "SeriesInstanceUID", "SeriesDescription", 
        "NewLocation", "SliceThickness", "SeriesNumber", "PatientSex", 
        "PatientAge", "StudyDate", "StudyInstanceUID", "SliceNum", 
        "imageCount", "上传状态"
    ]
    
    # Prepare row data
    row_data = {}
    for k in fieldnames:
        if k == "NewLocation":
            row_data[k] = str(directory_path)
        elif k == "上传状态":
            row_data[k] = status
        else:
            val = series_info.get(k)
            row_data[k] = str(val) if val is not None else ""

    if csv_path.exists():
        try:
            rows = []
            updated = False
            existing_fieldnames = []
            
            with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                existing_fieldnames = reader.fieldnames if reader.fieldnames else []
                
                if "上传状态" not in existing_fieldnames:
                    existing_fieldnames.append("上传状态")
                
                for row in reader:
                    # Match by SeriesInstanceUID
                    if row.get("SeriesInstanceUID") == str(series_info.get("SeriesInstanceUID")):
                        row["上传状态"] = status
                        updated = True
                    rows.append(row)
            
            if not updated:
                # If not found, append. Ensure we respect existing fieldnames
                for f in fieldnames:
                    if f not in existing_fieldnames:
                        existing_fieldnames.append(f)
                
                # Fill missing fields in row_data with empty string if they are in existing_fieldnames
                # And remove fields from row_data that are not in existing_fieldnames (unless we added them)
                final_row = {k: "" for k in existing_fieldnames}
                final_row.update({k: v for k, v in row_data.items() if k in existing_fieldnames})
                rows.append(final_row)

            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=existing_fieldnames)
                writer.writeheader()
                writer.writerows(rows)
                
        except Exception as e:
            log_print(f"Error updating CSV: {e}")
    else:
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(row_data)
        except Exception as e:
            log_print(f"Error creating CSV: {e}")

def upload_for_one_directory(directory_path,DEFAULT_CONFIG,series_type):

    config = DEFAULT_CONFIG

    # Initialize basic parameters

    directory = directory_path
    base_url = config['base_url']
    if config['cookie'].startswith("ls="):
        cookie = config['cookie']
    else:
        cookie = "ls=" + config['cookie']
    # series_type = config['series_type']
    series_type = int(series_type)
    patient_name = config.get('patient_name', None)
    use_series_uid = patient_name is None  # 如果 patient_name 未设置，则使用 series UID
    if patient_name is None:
        patient_name = 'default'  # 默认值，会被 series UID 覆盖
    api_url = f"{base_url}/api/v2/getSeriesByStudyInstanceUID"

    # Create upload configuration
    upload_config = create_upload_config(config)

    # Initialize DICOM directory
    log_print(f"扫描 DICOM 目录: {directory}")
    dicom_directory = DICOMDirectory(directory)

    # Get all series
    all_series = list(dicom_directory.get_dicom_series())
    total_series = len(all_series)
    log_print(f"发现 {total_series} 个序列\n")

    # Process each series
    successful_uploads = 0
    skipped_series = 0
    failed_series = 0
    patient_num = []
    error_messages = []  # 收集错误信息
    if len(all_series)>1:
        for series_count, series in enumerate(all_series, start=1):
            series_info = get_series_info(series)
            patient_num.append(series_info["PatientID"])
        dit={"message":f"当前文件夹包含{len(all_series)}个序列，建议将文件夹拆分成为多个文件夹，上传单个文件夹"}
        return {
            "content": [
                {
                "type": "text",
                "text": json.dumps(dit, ensure_ascii=False, indent=2)
                }
            ]
        }
    else:
        series_count=1
        series=all_series[0]

        series_info = get_series_info(series)
        patient_num.append(series_info)
        status = "失败"
        try:
            success = process_single_series(
                    series=series,
                    series_count=series_count,
                    patient_name=patient_name,
                    series_type=series_type,
                    base_url=base_url,
                    cookie=cookie,
                    upload_config=upload_config,
                    api_url=api_url,
                    use_series_uid=use_series_uid
            )
            if success:
                successful_uploads += 1
                status = "成功"
            else:
                skipped_series += 1
                status = "失败"
        except Exception as e:
            error_msg = f"序列 {series_count} ({series_info.get('SeriesDescription', 'Unknown')}): {str(e)}"
            log_print(f"\n[错误] 处理序列 {series_count} 时出错: {e}\n")
            error_messages.append(error_msg)
            failed_series += 1
            status = "失败"
        
        # Update CSV status
        update_csv_status(directory, series_info, status)

    series_info = get_series_info(series)
    study_uid = series_info["StudyInstanceUID"]
    SeriesInstanceUID = series_info["SeriesInstanceUID"]

    # 构建返回结果
    dic = {
        "successful_uploads": successful_uploads,
        "totalPatients": 1,
        "patients": f"{patient_num[0]}",
        "view_url": f"{config['base_url']}/study/studylist",
        "directory_path":directory,
        "study_uid":study_uid,
        "SeriesInstanceUID":SeriesInstanceUID,
        "type":series_type
    }
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(dic, ensure_ascii=False, indent=2)
            }
        ]
    }

