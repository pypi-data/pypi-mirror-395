"""HTTP Library"""

import json
from typing import Any

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import utils


def download(
    payload: dict,
    file: dict,
    chunks: bool = False,
    iter_content: dict | None = None,
    info: str | None = None,
) -> bool:
    """下载文件"""

    if utils.isTrue(payload, dict):
        request_arguments = {"method": "GET", "stream": True, **payload}
    else:
        return False

    if utils.isTrue(file, dict):
        file_arguments = {"mode": "wb", **file}
    else:
        return False

    if iter_content is not None and utils.isTrue(iter_content, dict):
        iter_content_arguments = {"chunk_size": 1024, **iter_content}
    else:
        iter_content_arguments = {"chunk_size": 1024}

    info_prefix: str = "Download"
    if utils.isTrue(info, str):
        info_prefix = f"Download {info}"

    try:

        logger.info(f"{info_prefix} ......")

        response = requests.request(**request_arguments)

        # # pylint: disable=W1514
        with open(**file_arguments) as _file:  # type: ignore

            if utils.isTrue(chunks, bool):
                for _chunk in response.iter_content(**iter_content_arguments):  # type: ignore
                    _file.write(_chunk)
            else:
                _file.write(response.content)

        logger.success(f"{info_prefix} [success]")

        return True

    except Exception as e:

        logger.error(f"{info_prefix} [failed]")
        logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def response_json(data: Any = None, **kwargs) -> str | None:
    """解决字符编码问题: ensure_ascii=False"""
    try:
        return json.dumps(data, default=str, ensure_ascii=False, sort_keys=True, **kwargs)
    except Exception as e:
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


class APIClient:
    """API Client"""

    def __init__(self, base_url: str, timeout: tuple = (3, 10)):

        self.session = requests.Session()

        self.base_url = base_url

        self.timeout = timeout

        # self.session.headers.update(
        #     {
        #         "User-Agent": "MyApp/1.0",
        #     }
        # )

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

        info: str = f"Request [GET]: {url}"

        logger.info(f"{info} | Start")

        try:
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            logger.success(f"{info} | Success")
            return response
        except requests.Timeout:
            # 请求超时
            logger.error(f"{info} | Timeout")
            return None
        except requests.ConnectionError:
            # 网络连接失败
            logger.error(f"{info} | Connection Error")
            return None
        except requests.HTTPError as e:
            # HTTP 错误
            logger.error(f"{info} | HTTP Error")
            logger.error(e)
            return None
        except requests.RequestException as e:
            # 请求失败
            logger.error(f"{info} | Request Exception")
            logger.error(e)
            return None
        except Exception as e:
            # 未知错误
            logger.error(f"{info} | Unknown Error")
            logger.error(e)
            return None

    def post(self, end: str, **kwargs) -> requests.Response | None:
        """POST"""

        # return self.session.post(self.base_url + end, timeout=self.timeout, **kwargs)

        url: str = f"{self.base_url}{end}"

        info: str = f"Request [POST]: {url}"

        logger.info(f"{info} | Start")

        try:
            response = self.session.post(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.Timeout:
            # 请求超时
            logger.error(f"{info} | Timeout")
            return None
        except requests.ConnectionError:
            # 网络连接失败
            logger.error(f"{info} | Connection Error")
            return None
        except requests.HTTPError as e:
            # HTTP 错误
            logger.error(f"{info} | HTTP Error")
            logger.error(e)
            return None
        except requests.RequestException as e:
            # 请求失败
            logger.error(f"{info} | Request Exception")
            logger.error(e)
            return None
        except Exception as e:
            # 未知错误
            logger.error(f"{info} | Unknown Error")
            logger.error(e)
            return None
