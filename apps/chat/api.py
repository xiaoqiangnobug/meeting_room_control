# coding=utf-8

"""

File: api.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/3 12:30

"""
import json
import logging
from fastapi import APIRouter
from utils.sys_format_res import async_normal_response
from .req_data import ChatReqData
from libs.llm_chat import chat_client_ty_plus
from utils.sys_db_connect import app_redis
from sys_config import CONFIG

logger = logging.getLogger('logger')
router = APIRouter()


@router.post(path='/chat')
@async_normal_response
async def chat(req_data: ChatReqData):
    # 闲聊接口

    chat_str = await app_redis.get(name=req_data.chat_id)
    messages = []
    if chat_str:
        chat_obj = json.loads(chat_str)
        messages.extend(chat_obj)
    messages.extend([{'role': obj.role, 'content': obj.content} for obj in req_data.chat_messages])
    ans = await chat_client_ty_plus.chat(messages=messages)
    messages.append({{'role': 'system', 'content': ans}})
    await app_redis.set(name=req_data.chat_id, value=json.dumps(messages, ensure_ascii=False),
                        ex=CONFIG.CONVERSATION['max_history_num'])
    return ans
