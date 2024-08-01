# coding=utf-8

"""

File: sys_format_res.py.py

Author: xiaoqiang

Explanation: 接口响应格式化

Date: 2024/5/31 17:27

"""
import time
from functools import wraps
from fastapi.responses import JSONResponse
from utils.sys_consts import SysResCode


# 全局统一格式化响应装饰器
def normal_response(func):
    """
    :param func: 被包装函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        data = {'code': str(SysResCode.SUCCESS) * 6, 'data': result, 'message': '成功', 'success': True,
                'time': int(time.time())}
        return JSONResponse(content=data)

    return wrapper


def async_normal_response(func):
    """
    :param func: 被包装函数
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        data = {'code': str(SysResCode.SUCCESS) * 6, 'data': result, 'message': '成功', 'success': True,
                'time': int(time.time())}
        return JSONResponse(content=data)

    return wrapper
