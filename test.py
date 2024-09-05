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

extra_paras = {'msgs': [
    {
        "role": "system",
        "content": "好的，已左移摄像头"
    },
    {
        "role": "user",
        "content": "帮我下移摄像头"
    },
    {
        "role": "system",
        "content": "好的，已下移摄像头"
    },
    {
        "role": "user",
        "content": "帮我右移摄像头"
    },
    {
        "role": "system",
        "content": "好的，已右移摄像头"
    },
    {
        "role": "user",
        "content": "帮我非右移摄像头"
    },
    {
        "role": "system",
        "content": "好的，已左移摄像头"
    },
    {
        "role": "user",
        "content": "帮我复位摄像头"
    },
    {
        "role": "user",
        "content": "帮我打开空间人数传感器"
    },
    {
        "role": "system",
        "content": "好的，已打开空间人数传感器"
    },
    {
        "role": "user",
        "content": "帮我关闭空间人数传感器"
    },
    {
        "role": "system",
        "content": "好的，已关闭空间人数传感器"
    },
    {
        "role": "user",
        "content": "帮我重启空间人数传感器"
    },
    {
        "role": "system",
        "content": "好的，已重启空间人数传感器"
    },
    {
        "role": "user",
        "content": "空间人数传感器打开了吗"
    },
    {
        "role": "user",
        "content": "将第二个窗帘打开三分之一"
    },
    {
        "role": "system",
        "content": "好的，将第二个窗帘打开了三分之一"
    },
    {
        "role": "user",
        "content": "将第一个窗帘关闭三分之二"
    },
    {
        "role": "system",
        "content": "好的，将第一个窗帘关闭了三分之二"
    },
    {
        "role": "user",
        "content": "将第二个窗帘打开至一半"
    }
]}

messages = [
    {'role': 'user', 'content': IotControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "将窗帘打开到三分之二"}
]

print(IotControlPrompt(extra_paras=extra_paras).prompt)
for _ in range(10):
    start_time = time.time()
    print(chat_client_ty_plus._chat(messages=messages))
    print(time.time() - start_time)
