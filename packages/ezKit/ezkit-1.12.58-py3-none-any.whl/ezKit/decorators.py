"""
通用装饰器库：适用于 FastAPI + SQLAlchemy + PostgreSQL + Loguru 技术栈
支持同步与异步函数自动识别
"""

import asyncio
import functools
import time
from typing import Callable

from loguru import logger
from sqlalchemy.orm import Session

# ------------------------------------------------------------
# 工具函数：自动判断是不是 async 函数
# ------------------------------------------------------------


def is_coroutine(fn):
    return asyncio.iscoroutinefunction(fn)


# ------------------------------------------------------------
# 1）打印函数调用日志（同步/异步通用）
# ------------------------------------------------------------


def log_call(fn: Callable):
    """打印函数调用日志（自动识别 async）"""

    @functools.wraps(fn)
    async def async_wrapper(*args, **kwargs):
        logger.info(f"[CALL] {fn.__name__} args={args} kwargs={kwargs}")
        result = await fn(*args, **kwargs)
        logger.info(f"[RETURN] {fn.__name__} -> {result}")
        return result

    @functools.wraps(fn)
    def sync_wrapper(*args, **kwargs):
        logger.info(f"[CALL] {fn.__name__} args={args} kwargs={kwargs}")
        result = fn(*args, **kwargs)
        logger.info(f"[RETURN] {fn.__name__} -> {result}")
        return result

    return async_wrapper if is_coroutine(fn) else sync_wrapper


# ------------------------------------------------------------
# 2）函数计时器
# ------------------------------------------------------------


def timer(fn: Callable):
    """计算函数执行耗时"""

    @functools.wraps(fn)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        result = await fn(*args, **kwargs)
        logger.info(f"[TIMER] {fn.__name__} took {time.time() - start:.4f}s")
        return result

    @functools.wraps(fn)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        logger.info(f"[TIMER] {fn.__name__} took {time.time() - start:.4f}s")
        return result

    return async_wrapper if is_coroutine(fn) else sync_wrapper


# ------------------------------------------------------------
# 3）捕获异常，避免函数 crash
# ------------------------------------------------------------


def catch(fn: Callable):
    """捕获异常，并打印日志"""

    @functools.wraps(fn)
    async def async_wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            logger.exception(f"[ERROR] {fn.__name__}: {e}")
            return None

    @functools.wraps(fn)
    def sync_wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.exception(f"[ERROR] {fn.__name__}: {e}")
            return None

    return async_wrapper if is_coroutine(fn) else sync_wrapper


# ------------------------------------------------------------
# 4）重试机制（支持 async）
# ------------------------------------------------------------


# def retry(times: int = 3, delay: float = 1.0):
#     """自动重试装饰器，支持 async"""

#     def decorator(fn: Callable):

#         @functools.wraps(fn)
#         async def async_wrapper(*args, **kwargs):
#             for i in range(times):
#                 try:
#                     return await fn(*args, **kwargs)
#                 except Exception as e:
#                     logger.error(f"[RETRY ASYNC] {fn.__name__} 第 {i + 1}/{times} 次失败: {e}")
#                     await asyncio.sleep(delay)
#             raise

#         @functools.wraps(fn)
#         def sync_wrapper(*args, **kwargs):
#             for i in range(times):
#                 try:
#                     return fn(*args, **kwargs)
#                 except Exception as e:
#                     logger.error(f"[RETRY] {fn.__name__} 第 {i + 1}/{times} 次失败: {e}")
#                     time.sleep(delay)
#             raise

#         return async_wrapper if is_coroutine(fn) else sync_wrapper

#     return decorator


# ------------------------------------------------------------
# 5）数据库事务管理（适用于 SQLAlchemy ORM）
# ------------------------------------------------------------


def db_transaction(fn: Callable):
    """
    SQLAlchemy ORM 事务装饰器：
    函数签名必须为 (db: Session, *args, **kwargs)
    """

    @functools.wraps(fn)
    def wrapper(db: Session, *args, **kwargs):
        try:
            result = fn(db, *args, **kwargs)
            db.commit()
            return result
        except Exception:
            db.rollback()
            logger.exception("[DB] Transaction rolled back")
            raise

    return wrapper


# ------------------------------------------------------------
# 6）参数类型检查（轻量级）
# ------------------------------------------------------------


def type_check(**type_hints):
    """检查入参类型，例如 @type_check(a=int, b=str)"""

    def decorator(fn: Callable):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for name, expected in type_hints.items():
                if name in kwargs and not isinstance(kwargs[name], expected):
                    raise TypeError(f"{name} must be {expected}")
            return fn(*args, **kwargs)

        return wrapper

    return decorator


# ------------------------------------------------------------
# 7）只执行一次（单例初始化）
# ------------------------------------------------------------


def once(fn: Callable):
    """只执行一次，之后总是返回第一次的结果"""

    called = False
    result = None

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal called, result
        if not called:
            result = fn(*args, **kwargs)
            called = True
        return result

    return wrapper


# ------------------------------------------------------------
# 8）缓存（简单 Memoize）
# ------------------------------------------------------------


def cache(fn: Callable):
    memo = {}

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in memo:
            memo[key] = fn(*args, **kwargs)
        return memo[key]

    return wrapper


# ------------------------------------------------------------
# 9）函数节流（间隔执行）
# ------------------------------------------------------------


def throttle(interval: float):
    last = 0.0

    def decorator(fn: Callable):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            nonlocal last
            now = time.time()
            if now - last >= interval:
                last = now
                return fn(*args, **kwargs)

        return wrapper

    return decorator


# ------------------------------------------------------------
# 10）函数防抖（等待静止）
# ------------------------------------------------------------


# def debounce(wait: float):
#     def decorator(fn: Callable):

#         @functools.wraps(fn)
#         def wrapper(*args, **kwargs):
#             wrapper._last = time.time()
#             time.sleep(wait)
#             if time.time() - wrapper._last >= wait:
#                 return fn(*args, **kwargs)

#         return wrapper

#     return decorator


# ------------------------------------------------------------
# 11）函数返回值类型强制
# ------------------------------------------------------------


def ensure(return_type: type):
    """确保返回值为指定类型"""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return return_type(fn(*args, **kwargs))

        return wrapper

    return decorator


# ------------------------------------------------------------
# 12）自动注入 Redis 连接（示例）
# ------------------------------------------------------------


def inject_redis(redis_client):
    """自动注入 Redis 客户端"""

    def decorator(fn):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, redis=redis_client, **kwargs)

        return wrapper

    return decorator


# ------------------------------------------------------------
# 13）函数入口输出 + 返回结果输出（最强日志）
# ------------------------------------------------------------


def trace(fn: Callable):

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info(f"[TRACE] {fn.__name__} 入参: {args} {kwargs}")
        result = fn(*args, **kwargs)
        logger.info(f"[TRACE] {fn.__name__} 返回: {result}")
        return result

    return wrapper


# ------------------------------------------------------------
# 14）允许跳过执行（用于调试）
# ------------------------------------------------------------

DEBUG_SKIP = False


def skip_when_debug(fn):

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if DEBUG_SKIP:
            logger.info(f"[SKIP] {fn.__name__} 因 DEBUG_SKIP 被跳过")
            return None
        return fn(*args, **kwargs)

    return wrapper


# ------------------------------------------------------------
# 15）强制函数必须登录 / 有权限（常用于后端）
# ------------------------------------------------------------


def require_login(fn):

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user")
        if not user:
            raise PermissionError("用户未登录")
        return fn(*args, **kwargs)

    return wrapper
