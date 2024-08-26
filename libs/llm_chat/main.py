# coding=utf-8

"""

File: main.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:44

"""

import time
import json
import logging
import asyncio
from openai import OpenAI
from sys_config import CONFIG
from utils.sys_error import CustomError
from utils.sys_consts import SysSpecialResCode

logger = logging.getLogger('logger')


class BaseChatTyClient:

    def __init__(self, model: str, api_key: str = CONFIG.TONGYI_API_KEY, base_url: str = CONFIG.TONGYI_BASE_URL):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def _chat(self, messages: list):
        # 模型推理功能
        try:
            start_time = time.time()
            res = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0
            )
            logger.info(msg=f'推理耗时: {time.time() - start_time}')
            print(res)
            return self._format_msg(msg=res.choices[0].message.content)
        except Exception as e:
            logger.error(msg=f'输入信息 {json.dumps(messages, ensure_ascii=False)} 推理失败', exc_info=e)
            raise CustomError(code=SysSpecialResCode.LLM_ERROR, msg='LLM模型推理失败，请检查API-KEY是否可用')

    @staticmethod
    def _format_msg(msg: str):
        # 格式化模型返回数据
        return msg

    def _json_chat(self, messages: list):
        # 模型JSON数据提取
        ans = self._chat(messages=messages)
        try:
            return json.loads(ans)
        except Exception as e:
            logger.warning(msg='首次提取异常,重新尝试', exc_info=e)
            messages.extend([
                {'role': 'system', 'content': ans},
                {'role': 'user', 'content': '请严格按照规则来进行提取，只输出JSON数据即可'}
            ])
            ans = self._chat(messages=messages)
            try:
                return json.loads(ans)
            except Exception as e:
                logger.error(msg=f'输入 {messages} 推理失败', exc_info=e)
                raise CustomError(code=SysSpecialResCode.LLM_JSON_ERROR, msg=SysSpecialResCode.LLM_JSON_ERROR)

    async def chat(self, messages: list):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._chat, messages)

    async def json_chat(self, messages: list):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._json_chat, messages)


class ChatClientTyPlus(BaseChatTyClient):
    # plus模型
    pass


class ChatClientTyTurbo(BaseChatTyClient):
    # turbo模型响应特殊处理

    @staticmethod
    def _format_msg(msg: str):
        if msg.startswith('```'):
            return msg[7:-3]
        return msg
