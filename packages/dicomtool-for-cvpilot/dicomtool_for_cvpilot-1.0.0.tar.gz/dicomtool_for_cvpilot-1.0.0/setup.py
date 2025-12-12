from src.function.upload import upload_for_one_directory
from src.cookie.config import get_config
from src.function.get_result import get_result
from src.function.seprate import separate_series_by_patient

#文件上传功能测试
# print(upload_for_one_directory(r"C:\Users\13167\Desktop\data\shuzhangqi\dcm",get_config(),"1"))

# #文件拆分：

# print(separate_series_by_patient(r"C:\Users\13167\Desktop\data"))
#
# #结果查询
# #"study_uid": "1.2.826.0.1.3680043.2.109.5.20220519102622656.1699758078.1",\n  "SeriesInstanceUID": "1.3.12.2.1107.5.1.4.73336.30000022051900071431600051249"

# print(get_result("1.2.826.0.1.3680043.2.109.5.20220519102622656.1699758078.1"))

#
async def Analysis_dicom_directory_tool(directory_path: str, series_type: str):
    return upload_for_one_directory(directory_path, get_config(), series_type)

async def separate_series_by_patient_tool(directory_path: str):
    return separate_series_by_patient(directory_path)

async def get_result_tool(study_uid: str):
    return get_result(study_uid)
       #, separate_series_by_patient_tool, get_result_tool)