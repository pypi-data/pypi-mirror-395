import json
import sys
from typing import Dict, Any

try:
    from .getcookie import CookieManager
    from .getcrpit import encrypt
except ImportError:
    # 直接运行时使用绝对导入
    from src.cookie.getcookie import CookieManager
    from src.cookie.getcrpit import encrypt


def get_config():
    """输入用户名和密码修改config.json"""
    DEFAULT_CONFIG: Dict[str, Any] = {
        "max_workers": 10,
        "max_retries": 3,
        "DEFAULT_CONNECT_TIMEOUT": 3,
        "DEFAULT_READ_TIMEOUT": 5,
        "DEFAULT_RETRY_DELAY": 5,
        "DEFAULT_BATCH_SIZE": 6
    }

    import os
    from dotenv import load_dotenv
    load_dotenv()
    name=os.getenv("name")
    password=os.getenv("password")
    tel=os.getenv("tel")
    base_url=os.getenv("base_url")

    payload = {"username": name, "password": password, "phoneNumber": tel}
    plain = json.dumps(payload, ensure_ascii=False)
    cipher = encrypt(plain)
    cookie_manager = CookieManager(base_url, cipher)
    cookie = cookie_manager.get_cookie()
    if cookie:
        DEFAULT_CONFIG["cookie"]=cookie
        DEFAULT_CONFIG["base_url"]=base_url
        print(f":配置详情{DEFAULT_CONFIG}", file=sys.stderr)

    return DEFAULT_CONFIG