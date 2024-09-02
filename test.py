# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import chat_client_ty_plus
from libs.prompts import DivideDomainPrompt, MeetingControlPrompt, IotControlPrompt

extra_paras = {'msgs': [
    # {'role': 'user', 'content': '打开空调'},
    # {'role': 'system', 'content': '您需要打开打几个空调'},
]}

messages = [
    {'role': 'user', 'content': IotControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "打开空调"}
]

print(IotControlPrompt(extra_paras=extra_paras).prompt)
for _ in range(2):
    start_time = time.time()
    print(chat_client_ty_plus._chat(messages=messages))
    print(time.time() - start_time)
