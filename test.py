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
        "content": "预约会议"
    },
    {
        "role": "system",
        "content": "好的，帮您预约了2024-09-04 16:46:59开始，2024-09-04 17:16:59结束的会议"
    }
]}

messages = [
    {'role': 'user', 'content': MeetingControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "查看会议"}
]

print(MeetingControlPrompt(extra_paras=extra_paras).prompt)
for _ in range(1):
    start_time = time.time()
    print(chat_client_ty_plus._chat(messages=messages))
    print(time.time() - start_time)
