# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import asyncio
import time
from libs.llm_chat import chat_client_ty_plus, chat_client_ty_turbo
from libs.prompts import DivideDomainPrompt, MeetingControlPrompt, IotControlPrompt

extra_paras = {'msgs': []}

messages = [
    {'role': 'user', 'content': DivideDomainPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "远端合成模式设置为四合成四等分"}
]
print(DivideDomainPrompt(extra_paras=extra_paras).prompt)
for _ in range(1):
    # print(chat_client_ty_turbo._json_chat(messages=messages))
    print(asyncio.run(chat_client_ty_plus.json_chat(messages=messages)))
