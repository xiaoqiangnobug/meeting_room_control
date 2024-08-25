# coding=utf-8

"""

File: chat_control.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/25 22:23

"""
import json

from libs.llm_chat import ChatClient
from libs.prompts import DivideDomainPrompt, MeetingControlPrompt
from utils.sys_db_connect import app_redis
from utils.sys_error import CustomError
from utils.sys_consts import SysResCode


class ChatControl:

    # 多轮控制

    def __init__(self, query: str, chat_id: str):
        """
        :param query: 会话id
        :param chat_id: 会话ID
        """
        self.query = query
        self.chat_id = chat_id
        self.turns = 0
        self.domain = None
        self.chat_messages = []  # 聊天信息

    @staticmethod
    async def _get_redis_obj(name: str):
        """
        :param name: 字段名称
        :return:
        """
        return await app_redis.get(name=name)

    async def _vertical_domain_division(self):
        # 垂域划分&聊天轮数判断
        chat_info = await self._get_redis_obj(name=self.chat_id)
        if chat_info:
            chat_info = json.loads(chat_info)
            self.chat_messages = chat_info['messages']
        self.chat_messages.append({'role': 'user', 'content': self.query})
        msgs = [{'role': 'system', 'content': DivideDomainPrompt().prompt}]
        msgs.extend(self.chat_messages)
        ans = await ChatClient().json_chat(messages=msgs)
        res_data = {
            'domain': ans['domain'],
            'turns': 1
        }
        if chat_info:
            if ans['domain'] == chat_info['domain']:
                res_data['turns'] = chat_info['turns'] + 1

        self.turns = res_data['turns']
        self.domain = res_data['domain']
        return res_data

    async def _chat_info_save(self):
        data = {
            'messages': self.chat_messages[-20:],
            'domain': self.domain,
            'turns': self.turns
        }
        await app_redis.set(name=self.chat_id, value=json.dumps(data, ensure_ascii=False), ex=3600)

    async def answer(self):
        # 第一步判断域和会话轮数

        await self._vertical_domain_division()
        if self.domain == 'iot-domain':
            # todo
            ans = {}
        elif self.domain == 'meeting-domain':
            msgs = [{'role': 'system', 'content': MeetingControlPrompt().prompt}]
            msgs.extend(self.chat_messages)
            ans = await ChatClient().json_chat(messages=msgs)

        elif self.domain == 'chitchat-domain':
            # todo
            ans = {}
        else:
            raise CustomError(msg='暂不支持的垂域', code=SysResCode.DATA_STATE_ERROR)

        # 会话保存
        await self._chat_info_save()
        return {
            'query': self.query,
            'domain': self.domain,
            'action': ans['action'],
            'slot_map': ans.get('slotMap', {}),
            'dialog_status': {'status': 'PROCESSING', 'turns': self.turns}
        }
