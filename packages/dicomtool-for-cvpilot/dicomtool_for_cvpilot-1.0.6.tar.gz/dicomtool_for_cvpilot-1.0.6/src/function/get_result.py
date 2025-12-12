import json
import sys
from  ..cookie.config import get_config

def log_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_result(study_uid):
    config = get_config()
    cookie = "ls=" + config["cookie"]
    api_url = config["base_url"]
    api_url = api_url + '/api/v2/getSeriesByStudyInstanceUID'
    def query_result(study_uid):
        study_uid, series_uid, s_type, status = find_result(
            api_url, study_uid, cookie
        )
        return status,study_uid,series_uid,s_type
        # 查询结果输出

    from src.api.query_api import find_result
    import time
    log_print("查询上传结果...")
    re = False
    for i in range(50):
        status,study_uid,series_uid,s_type= query_result(study_uid)
        log_print(f"查询状态: {status}, StudyInstanceUID: {study_uid}")
        if status is not None:
            if int(status) == 42:
                re = True
                log_print("查询成功")
                break
            elif int(status) == 41:
                time.sleep(1)
            elif int(status) == 44:
                break
            time.sleep(1)
            continue
        else:
            log_print("查询失败")
            break
    dit={}
    if re == True:
        dit["url"] = f"{config['base_url']}/viewer/{study_uid}?seriesInstanceUID={series_uid}&type={s_type}&status=42"
    elif int(status) == 41:
        dit["message"] = "没有执行完分析，再次进行查询get_result_tool工具"
    else:
        dit["message"] = f"查询超时，请确定是否进行上传，或系统中查看结果:{config['base_url']}/study/studylist"
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(dit, ensure_ascii=False, indent=2)
            }
        ]
    }

