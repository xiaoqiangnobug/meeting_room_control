# coding=utf-8

"""

File: sys_error_handler.py

Author: xiaoqiang

Explanation: 

Date: 2024/6/3 13:55

"""

import time
import logging
from fastapi.exceptions import RequestValidationError
from utils.sys_error import CustomError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from utils.sys_consts import SysResCode

logger = logging.getLogger('logger')


def sys_error_handler(req: Request, error: Exception):
    # 全局未知异常处理
    req_data = {}
    if req.query_params:
        req_data['query_params'] = req.query_params
    if req.path_params:
        req_data['path_params'] = req.path_params
    logger.error(msg=f'系统未知异常 {str(error)} headers: {req.headers} req_data: {req_data}', exc_info=error)
    data = {'code': str(SysResCode.UNKNOWN_ERROR), 'data': None, 'message': f'{str(error)}', 'success': False,
            'time': int(time.time())}
    return JSONResponse(content=data)


def param_error_handler(req: Request, error: RequestValidationError):
    # 参数校验异常处理
    msg = '参数错误 '
    for obj in error.errors():
        msg += f'{obj["loc"]} 参数校验异常 error: {obj["msg"]}'
        break
    logger.info(msg=f'参数校验异常 {error}')
    data = {'code': str(SysResCode.PARAM_FORMAT_ERROR), 'data': None, 'message': f'{msg}', 'success': False,
            'time': int(time.time())}
    return JSONResponse(content=data)


def custom_error_handler(req: Request, error: CustomError):
    # 自定义异常处理
    data = {'code': str(error.code), 'data': None, 'message': error.msg, 'success': False,
            'time': int(time.time())}
    logger.warning(msg=f'自定义异常触发: {error.msg} code: {error.code}')
    return JSONResponse(content=data)
