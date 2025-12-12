"""Utils Library"""

import re
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from functools import lru_cache
from os import environ

import tomllib
from loguru import logger

# --------------------------------------------------------------------------------------------------

DEBUG = environ.get("DEBUG")

# --------------------------------------------------------------------------------------------------


def load_toml_file(file: str) -> dict:
    """Load TOML file"""

    info: str = "load toml file"

    try:

        logger.info(f"{info} [ start ]")

        # 不要加 encoding="utf-8" 参数, 否则会报错:
        # binary mode doesn't take an encoding argument
        with open(file, "rb") as _file:
            config = tomllib.load(_file)

        logger.success(f"{info} [ success ]")

        return config

    except Exception as e:

        logger.error(f"{info} [ error ]")

        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)

        return {}


# --------------------------------------------------------------------------------------------------


def map_filter(iterable: Iterable, func: Callable) -> list:
    """对 iterable 执行 func, 并保留为 True 的返回值"""
    try:
        return [x for x in map(func, iterable) if x]
    except Exception as e:
        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)
        return []


# --------------------------------------------------------------------------------------------------


def check_dict_values_incorrect(
    data: dict[str, object],
    errors: object | Iterable[object] | None = None,
    include_keys: list[str] | None = None,
    exclude_keys: list[str] | None = None,
    regex: str | None = None,
) -> bool:
    """检查字典的值是否存在错误值"""

    # 支持:
    #
    #   target: 单值 或 多值（列表/元组）
    #   regex: 值是否匹配某正则表达式
    #   include_keys / exclude_keys: 指定检查的 key 范围
    #
    # 匹配规则(满足任一条件即可):
    #
    #   value 等于 target 或 在 target 列表里
    #   value 与 regex 匹配
    #
    # 参数:
    #
    #   data            dict[str, object]       待检查的字典
    #   errors          object|Iterable|None    指定匹配值或值列表
    #   include_keys    list[str]|None          只检查这些 key
    #   exclude_keys    list[str]|None          排除指定 key
    #   regex           str|None                正则匹配（自动转换成 re.Pattern）
    #
    # 返回:
    #
    #   bool
    #
    # 所有最终 keys 的值满足任一匹配条件返回 False, 否则 True

    try:

        # -----------------------
        # 处理 include / exclude 逻辑
        # -----------------------
        if include_keys is not None:
            keys = set(include_keys)
        else:
            keys = set(data.keys())

        if exclude_keys is not None:
            keys -= set(exclude_keys)

        # 若没有 key 需要检查 -> 默认 True
        if not keys:
            return False

        # -----------------------
        # 处理 target（单值 or 列表）
        # -----------------------
        if isinstance(errors, Iterable) and not isinstance(errors, (str, bytes)):
            error_set = set(errors)
        else:
            error_set = {errors}

        # -----------------------
        # 处理正则
        # -----------------------
        pattern = re.compile(regex) if regex else None

        # -----------------------
        # 核心检查逻辑
        # -----------------------
        for k in keys:

            value = data.get(k)

            # 匹配 target
            if value in error_set:
                return False

            # 匹配 类型
            # if isinstance(types, list) and types:
            #     if any(isinstance(value, type) for type in types):
            #         return False

            # 匹配正则
            if pattern is not None:
                if isinstance(value, str) and pattern.search(value):
                    return False

        return True

    except Exception as e:

        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)

        return False


# --------------------------------------------------------------------------------------------------


def timestamp_to_datetime(timestamp: int | float, tz: timezone = timezone.utc) -> datetime | None:
    """Unix Timestamp 转换为 Datatime"""
    try:
        if not isinstance(timestamp, (int, float)):
            return None
        return (datetime.fromtimestamp(timestamp, tz=tz)).replace(tzinfo=None)
    except Exception as e:
        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


@lru_cache(maxsize=None)
def compile_patterns(patterns: tuple[str, ...]) -> re.Pattern:
    """把 list 编译为一个超大正则 (带缓存)"""
    combined = "|".join(map(re.escape, patterns))
    return re.compile(combined)
