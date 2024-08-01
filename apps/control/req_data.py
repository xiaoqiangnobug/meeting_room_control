# coding=utf-8

"""

File: req_data.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 22:58

"""

from pydantic import BaseModel, Field


class ControlChatReqData(BaseModel):
    # 控制聊天接口入参

    class _ChatMessage(BaseModel):
        chatMessage_id: str = Field(alias='chatMessageId', max_length=32, description='消息Id')
        role: str
        content: str = Field(default='', alias='rawContent', description='消息内容')
        audio_content: str = Field(default='', alias='audioContent', description='音频内容')

    class _InitOpening(BaseModel):
        language: str = 'Ch'

    chat_id: str = Field(max_length=32, alias='chatId', description='会话ID')
    owner_id: str = Field(max_length=32, alias='ownerId', description='所属者ID')
    device_id: str = Field(alias='deviceId', description='设备ID')
    chat_name: str = Field(alias='chatName', description='会话名称')
    init_inputs: dict = Field(default=None, alias='initInputs', description='会话动态变量值')
    init_opening: _InitOpening = Field(default=None, alias='initOpening', description='开场白')
    chat_messages: list[_ChatMessage] = Field(alias='chatMessages', description='对话消息列表')
