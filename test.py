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
    {'role': 'user', 'content': '预订会议'},
    {'role': 'system', 'content': '好的预订了'},
    # {'role': 'user', 'content': '预订早上十点的'},
    # {'role': 'system', 'content': '好的修改好了'},
    # {'role': 'user', 'content': ''},
    # {'role': 'system', 'content': '好的改成制热了'}
]}

messages = [
    {'role': 'system', 'content': MeetingControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "主题是AI方案讨论"}
]

print(MeetingControlPrompt(extra_paras=extra_paras).prompt)

start_time = time.time()
print(chat_client_ty_plus._json_chat(messages=messages))
print(time.time() - start_time)
