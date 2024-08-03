# coding=utf-8

"""

File: req_data.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/3 12:30

"""

from pydantic import BaseModel, Field


class ChatReqData(BaseModel):
    # 控制聊天接口入参

    class _ChatMessage(BaseModel):
        role: str
        content: str = Field(default='', alias='rawContent', description='消息内容')

    init_inputs: dict = Field(default=None, alias='initInputs', description='会话动态变量值')
    chat_messages: list[_ChatMessage] = Field(alias='chatMessages', description='对话消息列表')
