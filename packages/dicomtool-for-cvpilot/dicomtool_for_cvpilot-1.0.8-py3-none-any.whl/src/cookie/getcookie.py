
import logging
import sys
import requests
# python
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)




api_base_url="http://192.168.1.3:29999"
login_cipher="123#34#117#115#101#114#110#97#109#101#34#58#34#99#118#112#105#108#111#116#34#44#34#112#97#115#115#119#111#114#100#34#58#34#67#118#112#105#108#111#116#48#49#64#34#125#"
#="123#34#117#115#101#114#110#97#109#101#34#58#32#34#122#104#97#110#103#106#105#97#110#99#111#110#103#34#44#32#34#112#97#115#115#119#111#114#100#34#58#32#34#90#106#99#49#50#51#64#34#44#32#34#112#104#111#110#101#78#117#109#98#101#114#34#58#32#34#49#56#51#56#56#49#49#54#53#53#48#34#125#"
cookie_refresh_hours: 24  # Cookie 刷新间隔（小时）

class CookieManager:
    """Cookie 管理器，负责登录和刷新 Cookie"""

    def __init__(self, api_base_url, login_cipher, refresh_hours=24):
        self.api_base_url = api_base_url
        self.login_cipher = login_cipher
        self.refresh_hours = refresh_hours
        self.cookie = None
        self.cookie_time = None

    def get_cookie(self):
        """获取有效的 Cookie，如果过期则自动刷新"""
        if self._is_cookie_valid():
            logger.info("使用缓存的 Cookie")
            return self.cookie

        logger.info("Cookie 已过期或不存在，重新登录获取")
        return self._login()

    def _is_cookie_valid(self):
        """检查 Cookie 是否有效"""
        if not self.cookie or not self.cookie_time:
            return False

        elapsed = datetime.now() - self.cookie_time
        if elapsed.total_seconds() > self.refresh_hours * 3600:
            logger.info(f"Cookie 已过期（{elapsed.total_seconds() / 3600:.1f} 小时）")
            return False

        return True

    def _login(self):
        """登录获取 Cookie"""
        login_url = f"{self.api_base_url}/api/v1/login"
        payload = {"cipher": self.login_cipher}

        try:
            logger.info(f"正在登录到 {login_url}")
            response = requests.post(
                login_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()

            # 从响应头中提取 Cookie
            set_cookie = response.headers.get('Set-Cookie', '')
            if not set_cookie:
                logger.error("登录响应中未找到 Set-Cookie 头")
                return None

            # 提取 ls= 值
            for part in set_cookie.split(';'):
                if part.strip().startswith('ls='):
                    self.cookie = part.strip().split('=', 1)[1]
                    self.cookie_time = datetime.now()
                    logger.info(f"成功获取 Cookie: ls={self.cookie}...")
                    return self.cookie

            logger.error("无法从 Set-Cookie 中提取 ls 值")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"登录失败: {e}")
            return None
if __name__ == "__main__":
    cookie_manager = CookieManager(api_base_url, login_cipher)
    cookie = cookie_manager.get_cookie()
    if cookie:
        logger.info(f"获取到的 Cookie: ls={cookie}...")
    else:
        logger.error("未能获取到有效的 Cookie")