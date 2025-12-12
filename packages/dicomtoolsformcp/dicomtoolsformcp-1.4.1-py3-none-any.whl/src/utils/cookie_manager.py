import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

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
