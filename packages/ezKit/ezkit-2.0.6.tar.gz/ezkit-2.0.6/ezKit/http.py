"""HTTP Library"""

from os import environ

import requests

from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --------------------------------------------------------------------------------------------------

DEBUG = environ.get("DEBUG")

# --------------------------------------------------------------------------------------------------


class HTTPClient:
    """API Client"""

    def __init__(self, base_url: str, timeout: tuple = (3, 10)):

        self.session = requests.Session()

        self.base_url = base_url

        self.timeout = timeout

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            }
        )

        # token: str | None = None
        # if token:
        #     self.session.headers["Authorization"] = f"Bearer {token}"

        # 重试
        retry = Retry(total=3, backoff_factor=0.3, allowed_methods=["GET", "POST"])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, end: str, **kwargs) -> requests.Response | None:
        """GET"""

        # return self.session.get(self.base_url + end, timeout=timeout, **kwargs)

        url: str = f"{self.base_url}{end}"

        info: str = f"request get {url}"

        logger.info(f"{info} [ start ]")

        try:
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            logger.success(f"{info} [ success ]")
            return response
        except requests.Timeout:
            # 请求超时
            logger.error(f"{info} [ timeout ]")
            return None
        except requests.ConnectionError:
            # 网络连接失败
            logger.error(f"{info} [ connection error ]")
            return None
        except requests.HTTPError as e:
            # HTTP 错误
            logger.error(f"{info} [ http error ]")
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None
        except requests.RequestException as e:
            # 请求失败
            logger.error(f"{info} [ request exception ]")
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None
        except Exception as e:
            # 未知错误
            logger.error(f"{info} [ unknown error ]")
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    def post(self, end: str, **kwargs) -> requests.Response | None:
        """POST"""

        # return self.session.post(self.base_url + end, timeout=self.timeout, **kwargs)

        url: str = f"{self.base_url}{end}"

        info: str = f"request post {url}"

        logger.info(f"{info} [ start ]")

        try:
            response = self.session.post(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.Timeout:
            # 请求超时
            logger.error(f"{info} [ timeout ]")
            return None
        except requests.ConnectionError:
            # 网络连接失败
            logger.error(f"{info} [ connection error ]")
            return None
        except requests.HTTPError as e:
            # HTTP 错误
            logger.error(f"{info} [ http error ]")
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None
        except requests.RequestException as e:
            # 请求失败
            logger.error(f"{info} [ request exception ]")
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None
        except Exception as e:
            # 未知错误
            logger.error(f"{info} [ unknown error ]")
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None
