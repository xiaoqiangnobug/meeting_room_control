# coding=utf-8

"""

File: api.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/3 12:30

"""

import logging
from fastapi import APIRouter
from utils.sys_format_res import async_normal_response
from .req_data import ChatReqData
from libs.llm_chat.main import ChatClient

logger = logging.getLogger('logger')
router = APIRouter()


@router.post(path='/chat')
@async_normal_response
async def chat(req_data: ChatReqData):
    # 闲聊接口
    messages = req_data.chat_messages
    ans = await ChatClient().chat(messages=messages)
    return ans
