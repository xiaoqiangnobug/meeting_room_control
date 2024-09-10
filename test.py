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

extra_paras = {'msgs': [
    {
        "role": "user",
        "content": "打开空调"
    },
    {
        "role": "system",
        "content": "室内有两台空调，您想打开第几台"
    },
    {
        "role": "user",
        "content": "打开第一台"
    },
    {
        "role": "system",
        "content": "是否确认打开第一台空调"
    },
    {
        "role": "user",
        "content": "确认打开"
    },
    {
        "role": "system",
        "content": "好的已经打开了"
    },
    {
        "role": "user",
        "content": "打开第二台空调"
    },
    {
        "role": "system",
        "content": "好的打开了"
    }
]
}

messages = [
    {'role': 'user', 'content': IotControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "调整为制冷模式"}
]

print(IotControlPrompt(extra_paras=extra_paras).prompt)
print(messages[1])
for _ in range(5):
    # print(chat_client_ty_turbo._json_chat(messages=messages))
    print(asyncio.run(chat_client_ty_plus.json_chat(messages=messages)))
