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
    {
        "role": "user",
        "content": "预订会议"
    },
    {
        "role": "system",
        "content": "好的，帮您预约了2024-09-04 17:32:39开始，2024-09-04 18:02:39结束的会议"
    }
]}

messages = [
    {'role': 'user', 'content': MeetingControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "查看会议信息"}
]

print(MeetingControlPrompt(extra_paras=extra_paras).prompt)
for _ in range(10):
    start_time = time.time()
    print(chat_client_ty_plus._chat(messages=messages))
    print(time.time() - start_time)
