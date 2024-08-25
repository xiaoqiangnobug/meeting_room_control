# coding=utf-8

"""

File: sys_db_connect.py

Author: xiaoqiang

Explanation: 

Date: 2024/6/3 11:22

"""
import aioredis
from fastapi import FastAPI

from sys_config import CONFIG

app_redis = aioredis.Redis(**CONFIG.REDIS_CONFIG)


def init_redis_async(app: FastAPI):
    @app.on_event('startup')
    async def init_redis_client():
        # 创建redis连接池并绑定属性给app
        await app_redis

    @app.on_event('shutdown')
    async def redis_close():
        # 服务关闭时关闭redis连接池
        await app_redis.close()
        await app_redis.connection_pool.disconnect()
