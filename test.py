# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import ChatClient
from libs.prompts.main import prompt

messages = [
    {'role': 'system', 'content': prompt.strip()},
    {'role': 'user', 'content': '帮我设置导播合成模式为两合成二等分'}]

start_time = time.time()
print(ChatClient()._chat(messages=messages))
print(time.time() - start_time)

