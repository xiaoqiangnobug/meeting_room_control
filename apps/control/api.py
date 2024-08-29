# coding=utf-8

"""

File: api.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 22:56

"""

import base64
import json
import logging
from fastapi import APIRouter
from utils.sys_format_res import async_normal_response
from .req_data import ControlChatReqData, AddChatHistory
from .res_data import ControlChatResData
from apps.control.servers import ChatControl
from libs.asr_client import audio_to_text
from utils.sys_db_connect import app_redis
from utils.sys_error import CustomError
from utils.sys_consts import SysSpecialResCode

router = APIRouter()

logger = logging.getLogger('logger')


@router.post('/controlChat')
@async_normal_response
async def control_chat(req_data: ControlChatReqData):
    # 聊天控制接口
    messages = req_data.chat_messages
    audio = messages[-1].audio_content
    if audio:
        audio = base64.b64decode(audio)
        messages[-1].content = await audio_to_text(audio=audio)
        messages[-1].audio_content = ''

    result = await ChatControl(chat_id=req_data.chat_id, query=messages[-1].content).answer()

    return ControlChatResData().dump(obj={'result': result}, many=False)


@router.post('/addChatHistory')
@async_normal_response
async def add_chat_history(req_data: AddChatHistory):
    # 指令消息转文本保证完整的聊天信息（上下文）

    chat_str = await app_redis.get(name=req_data.chat_id)
    if not chat_str:
        raise CustomError(msg='未找到有效的对话信息', code=SysSpecialResCode.CHAT_LOG_WARNING)
    chat_obj = json.loads(chat_str)
    messages = chat_obj['messages']
    for obj in req_data.chat_messages:
        messages.append({
            'role': obj.role,
            'content': obj.content
        })
    await app_redis.set(name=req_data.chat_id, value=json.dumps(chat_obj, ensure_ascii=False))

    return True
