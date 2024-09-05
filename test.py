# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import chat_client_ty_plus, chat_client_ty_turbo
from libs.prompts import DivideDomainPrompt, MeetingControlPrompt, IotControlPrompt

extra_paras = {'msgs': []}

messages = [
    {'role': 'user', 'content': DivideDomainPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "停止录制"}
]

print(DivideDomainPrompt(extra_paras=extra_paras).prompt)
print(messages[1])
for _ in range(10):
    start_time = time.time()
    print(chat_client_ty_turbo._json_chat(messages=messages))
    print(time.time() - start_time)
