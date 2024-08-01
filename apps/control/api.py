# coding=utf-8

"""

File: api.py

Author: weikaiqiang

Explanation: 

Date: 2024/7/30 22:56

"""

import logging
from fastapi import APIRouter
from utils.sys_format_res import async_normal_response
from .req_data import ControlChatReqData
from libs.llm_chat import ChatClient
from libs.prompts import prompt

router = APIRouter()

logger = logging.getLogger('logger')


@router.post('/controlChat')
@async_normal_response
async def control_chat(req_data: ControlChatReqData):
    # 聊天控制接口
    messages = req_data.chat_messages
    messages.insert(0, {'role': 'system', 'content': prompt})
    ans = await ChatClient().chat(messages=req_data.chat_messages)
    logger.info(msg=f'文本: {req_data.chat_messages[0]["content"]}  拆封结果: {ans}')

    return ans
