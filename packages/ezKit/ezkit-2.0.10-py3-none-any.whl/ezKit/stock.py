"""股票"""

from copy import deepcopy
from os import environ

from loguru import logger

# --------------------------------------------------------------------------------------------------

DEBUG = environ.get("DEBUG")

# --------------------------------------------------------------------------------------------------


def coderename(target: str | dict, restore: bool = False) -> str | dict | None:
    """代码重命名"""

    # 正向:
    #     coderename('000001') => 'sz000001'
    #     coderename({'code': '000001', 'name': '平安银行'}) => {'code': 'sz000001', 'name': '平安银行'}
    # 反向:
    #     coderename('sz000001', restore=True) => '000001'
    #     coderename({'code': 'sz000001', 'name': '平安银行'}) => {'code': '000001', 'name': '平安银行'}

    try:

        # 初始化

        code_object: dict = {}
        code_name: str = ""

        # 判断 target

        if isinstance(target, str) and target:
            code_name = target
        elif isinstance(target, dict) and target:
            code_object = deepcopy(target)
            code_name = code_object.get("code", "")
        else:
            logger.error("target value or type error")
            return None

        if not code_name:
            logger.error("code name error")
            return None

        # 是否还原

        if restore:

            if len(code_name) != 8 or not code_name.startswith(("sz", "sh")):
                logger.error("code name error")
                return None

            code_name = code_name[-6:]

        else:

            if code_name[0:2] == "00":
                code_name = f"sz{code_name}"
            elif code_name[0:2] == "60":
                code_name = f"sh{code_name}"
            else:
                logger.error("code name error")
                return None

        # 返回结果

        if isinstance(target, str):
            return code_name

        if isinstance(target, dict):
            code_object["code"] = code_name
            return code_object

        return None

    except Exception as e:

        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)

        return None
