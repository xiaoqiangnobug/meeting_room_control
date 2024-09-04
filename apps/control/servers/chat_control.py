# coding=utf-8

"""

File: chat_control.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/25 22:23

"""
import json
import logging

from libs.llm_chat import chat_client_ty_turbo, chat_client_ty_plus
from libs.prompts import DivideDomainPrompt, MeetingControlPrompt, IotControlPrompt, ChatControlPrompt
from utils.sys_db_connect import app_redis
from utils.sys_error import CustomError
from utils.sys_consts import SysResCode

logger = logging.getLogger('logger')


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
        self.domain = ''
        self.previous_domain = ''
        self.chat_messages = []  # 聊天信息
        self.chat_state = 'PROCESSING'

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
            chat_json = json.loads(chat_info)
            self.chat_messages = chat_json['messages']
            self.turns = chat_json['turns']
            self.previous_domain = chat_json['domain']

        extra_paras = {'msgs': self.chat_messages}
        msgs = [
            {'role': 'system', 'content': DivideDomainPrompt(extra_paras=extra_paras).prompt},
            {'role': 'user', 'content': self.query}
        ]
        ans = await chat_client_ty_turbo.json_chat(messages=msgs)
        logger.info(msg=f'推理域: {ans["domain"]}  上一次: {self.previous_domain}')
        if ans['domain'] != self.previous_domain or ans['domain'] == 'chitchat-domain':
            # 切换域或者闲聊域时-聊天记录清空对话轮数重置
            self.turns = 1
            self.chat_messages = []
        else:
            # 切换域聊天记录清空，对话轮数重置
            self.turns += 1
        self.domain = ans['domain']

    async def _chat_info_save(self):
        if self.domain != 'chitchat-domain':
            self.chat_messages.append({
                'role': 'user',
                'content': self.query
            })
        data = {
            'messages': self.chat_messages[-20:],
            'domain': self.domain,
            'turns': self.turns
        }
        await app_redis.set(name=self.chat_id, value=json.dumps(data, ensure_ascii=False), ex=3600)

    async def answer(self):
        # 第一步判断域和会话轮数

        await self._vertical_domain_division()
        extra_paras = {'msgs': self.chat_messages}
        if self.domain == 'iot-domain':
            msgs = [
                {'role': 'system', 'content': IotControlPrompt(extra_paras=extra_paras).prompt},
                {'role': 'user', 'content': self.query}
            ]
            ans = await chat_client_ty_plus.json_chat(messages=msgs)
        elif self.domain == 'meeting-domain':
            msgs = [
                {'role': 'system', 'content': MeetingControlPrompt(extra_paras=extra_paras).prompt},
                {'role': 'user', 'content': self.query}
            ]
            ans = await chat_client_ty_plus.json_chat(messages=msgs)
        elif self.domain == 'chitchat-domain':
            msgs = [
                {'role': 'system', 'content': ChatControlPrompt(extra_paras=extra_paras).prompt},
                {'role': 'user', 'content': self.query}
            ]
            ans = await chat_client_ty_plus.json_chat(messages=msgs)
            self.chat_state = 'FINISH'
        else:
            raise CustomError(msg='暂不支持的垂域', code=SysResCode.DATA_STATE_ERROR)

        # 会话保存
        await self._chat_info_save()
        return {
            'query': self.query,
            'domain': self.domain,
            'action': ans['action'],
            'slot_map': ans.get('slotMap', {}),
            'dialog_status': {'status': self.chat_state, 'turns': self.turns}
        }
