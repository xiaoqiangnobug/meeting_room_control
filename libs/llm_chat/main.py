# coding=utf-8

"""

File: main.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:44

"""

import json
import logging
import asyncio
from openai import OpenAI
from sys_config import CONFIG

logger = logging.getLogger('logger')


class ChatClient:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.client = OpenAI(api_key=CONFIG.TONGYI_API_KEY, base_url=CONFIG.TONGYI_BASE_URL)

    def _chat(self, messages: list):
        # 模型推理功能
        res = self.client.chat.completions.create(
            model=CONFIG.MODEL_NAME,
            messages=messages
        )
        return json.loads(res.choices[0].message.content)

    async def chat(self, messages: list):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._chat, messages)
