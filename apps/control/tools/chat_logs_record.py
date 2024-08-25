# coding=utf-8

"""

File: chat_logs_record.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/21 16:42

"""

from utils.sys_db_connect import app_redis


class ChatLogsRecord:
    # 会话记录管理

    def __init__(self, chat_id: str, intention: str):
        """
        :param chat_id: 会话ID
        :param intention: 本轮会话意图领域
        """
        self.chat_id = chat_id
        self.chat_rounds = 0
        self.intention = intention

    @staticmethod
    async def _get_redis_obj(name: str):
        """
        :param name: 字段名称
        :return:
        """
        return await app_redis.hgetall(name=name)

    @staticmethod
    async def _insert_redis_obj(name: str, data: dict):
        """
        :param name: 字段名称
        :return:
        """

        await app_redis.hmset(name=name, **data)

    async def message(self):
        obj = await self._get_redis_obj(name=self.chat_id)
        if obj:
            return obj['message']
        return ''

    async def insert_message(self, msg: str):
        """
        :param msg: 消息内容
        :return: {'message': [{role: 角色, msg: 消息内容}], chat_rounds: 对话轮数}
        """

        data = await self._get_redis_obj(name=self.chat_id)
        if not data:
            data = {
                'message': [msg],
                'chat_rounds': 1
            }
        data['message'].append(msg)
        data['chat_rounds'] += 1
        await self._insert_redis_obj(name=self.chat_id, data=data)

        return data

    @staticmethod
    async def _delete_redis_obj(name: str):
        """
        :param name: 字段名称
        :return:
        """
        await app_redis.delete(name)

    async def clear(self):
        await self._delete_redis_obj(name=self.chat_id)
