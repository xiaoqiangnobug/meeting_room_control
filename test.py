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
    {'role': 'user', 'content': '预订明天的会议'},
    {'role': 'system', 'content': '好的，成功预订了2024-09-02 08:00:00的会议'},
]}

messages = [
    {'role': 'user', 'content': MeetingControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "取消吧"}
]

print(IotControlPrompt(extra_paras=extra_paras).prompt)
for _ in range(100):
    start_time = time.time()
    print(chat_client_ty_plus._chat(messages=messages))
    print(time.time() - start_time)
