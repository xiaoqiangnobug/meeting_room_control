# coding=utf-8

"""

File: api.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 22:56

"""

import base64
import io
import logging
from fastapi import APIRouter
from utils.sys_format_res import async_normal_response
from .req_data import ControlChatReqData
from .res_data import ControlChatResData
from libs.llm_chat import ChatClient
from libs.prompts import prompt
from libs.grpc_client.asr_client import audio_to_text

router = APIRouter()

logger = logging.getLogger('logger')


@router.post('/controlChat')
@async_normal_response
async def control_chat(req_data: ControlChatReqData):
    # 聊天控制接口
    messages = req_data.chat_messages
    messages.insert(0, {'role': 'system', 'content': prompt})
    audio = messages[-1].audio_content
    if audio:
        audio = base64.b64decode(audio)
        messages[-1].content = audio_to_text(audio=io.BytesIO(audio))
        messages[-1].audio_content = ''
    ans = await ChatClient().json_chat(messages=messages)
    result = {
        'query': req_data.chat_messages[-1].content,
        'domain': ans['domain'],
        'action': ans['action'],
        'slot_map': ans.get('slotMap', {})

    }
    logger.info(msg=f'文本: {req_data.chat_messages[1].content}  拆封结果: {ans}')

    return ControlChatResData().dump(obj={'result': result}, many=False)
