# coding=utf-8

"""

File: __init__.py.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:44

"""

from .main import ChatClientTyPlus, ChatClientTyTurbo
from sys_config import CONFIG

chat_client_ty_plus = ChatClientTyPlus(model=CONFIG.MODEL_NAME_PLUS)
chat_client_ty_turbo = ChatClientTyTurbo(model=CONFIG.MODEL_NAME_TURBO)
