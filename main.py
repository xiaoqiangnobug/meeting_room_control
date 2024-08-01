# coding=utf-8

"""

File: main.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:11

"""

import time
import logging.config

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils.sys_log_config import LOG_CONFIG
from utils.sys_consts import SysResCode
from utils.sys_error import CustomError
from utils.sys_error_handler import param_error_handler, custom_error_handler, sys_error_handler

from apps.control import router as control_router

# 加载日志配置
logging.config.dictConfig(LOG_CONFIG)
app = FastAPI()


# 注册全局入参校验异常处理模块
@app.exception_handler(RequestValidationError)
async def param_error_intercept(request, exc):
    return param_error_handler(req=request, error=exc)


@app.exception_handler(405)
async def error_405_intercept(request, exc):
    data = {'code': str(SysResCode.METHOD_NOT_ALLOWED), 'data': '405 Method Not Allowed', 'message': '失败',
            'success': False, 'time': int(time.time())}
    return JSONResponse(data, status_code=405)


@app.exception_handler(404)
async def error_404_intercept(request, exc):
    data = {'code': str(SysResCode.PATH_NOT_FOUND), 'data': '404 Not Found', 'message': '失败', 'success': False,
            'time': int(time.time())}
    return JSONResponse(data, status_code=404)


# 注册全局自定义异常处理模块
@app.exception_handler(CustomError)
async def custom_error_intercept(request, exc):
    return custom_error_handler(req=request, error=exc)


# 注册全局未知异常处理模块
@app.exception_handler(Exception)
async def sys_error_intercept(request, exc):
    return sys_error_handler(req=request, error=exc)


# CORS跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

# 注册子模块路由
app.include_router(prefix='/api', router=control_router)
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
