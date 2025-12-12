import json
import shutil
import csv
from pathlib import Path

from ..cookie.getcookie import logger
from ..models import DICOMDirectory
from ..core.series_processor import get_series_info


def copy_dicom(src_path: str, dest_dir: str) -> Path:
    src = Path(src_path)
    dest_folder = Path(dest_dir)
    if not src.exists():
        raise FileNotFoundError(f"源文件不存在: {src}")
    dest_folder.mkdir(parents=True, exist_ok=True)

    dest = dest_folder / src.name
    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        i = 1
        while True:
            candidate = dest_folder / f"{stem}_copy{i}{suffix}"
            if not candidate.exists():
                dest = candidate
                break
            i += 1

    shutil.copy2(src, dest)
    return dest

def separate_series_by_patient(directory_path):
    base_path = Path(directory_path)
    csv_file = base_path / "文件拆分信息.csv"
    
    if csv_file.exists():
        message = f"检测到 {csv_file.name} 已存在，已经进行文件拆分"
        logger.info(message)
        dic = {
            "message": message,
        }
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(dic, ensure_ascii=False)
                }
            ]
        }

    dicom_directory = DICOMDirectory(directory_path)
    all_series = list(dicom_directory.get_dicom_series())

    # 按患者分组
    patient_series_map = {}
    for series in all_series:
        info = get_series_info(series)
        pid = info["PatientID"]
        patient_series_map.setdefault(pid, []).append(series)

    # 为每个患者和序列创建目录并复制文件
    base_path = Path(directory_path)
    sucess_num=0
    main_dir=[]
    series_records = []

    for pid, series_list in patient_series_map.items():
        p_dir = base_path / pid
        p_dir.mkdir(parents=True, exist_ok=True)
        main_dir.append(p_dir)
        for series in series_list:
            info = get_series_info(series)
            series_uid = info.get("SeriesInstanceUID", "unknown_series")
            s_dir = p_dir / series_uid
            s_dir.mkdir(parents=True, exist_ok=True)

            # 记录序列信息
            record = {k: str(v) if v is not None else "" for k, v in info.items()}
            record["NewLocation"] = str(s_dir)
            series_records.append(record)

            for instance in getattr(series, "instances", []):
                # 支持常见的实例路径属性名
                src = (
                    getattr(instance, "filepath", None)
                    or getattr(instance, "file_path", None)
                    or getattr(instance, "path", None)
                )
                if not src:
                    logger.warning(f"实例缺少路径: patient={pid}, series={series_uid}")
                    continue

                try:
                    if copy_dicom(src, s_dir):
                        sucess_num += 1
                except Exception as e:
                    logger.exception(f"复制失败: {src} -> {s_dir}: {e}")

    # 创建excel文件夹并保存信息
    if series_records:
        csv_file = base_path / "文件拆分信息.csv"

        # 只写入指定的字段
        priority = [
            "PatientID", "PatientName", "SeriesInstanceUID",
            "NewLocation", "PatientAge", "StudyDate", "StudyInstanceUID",
            "imageCount"
        ]

        try:
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=priority, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(series_records)
            logger.info(f"序列信息已保存至: {csv_file}")
        except Exception as e:
            logger.error(f"保存序列信息失败: {e}")

    message=f"已为 {len(patient_series_map)} 位患者分离 {len(all_series)} 个序列，成功复制 {sucess_num} 个文件。"
    dic={
        "totalPatients": len(patient_series_map),
        "totalSeries": len(all_series),
        "totalFilesCopied": sucess_num,
        "message": message,
        "newDirectory": f"{main_dir}"
    }
    return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(dic, ensure_ascii=False)
                }
            ]
    }