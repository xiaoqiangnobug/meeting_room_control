# coding=utf-8

"""

File: test.py

Author: weikaiqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import ChatClient
from libs.prompts.main import prompt, data

messages = [
    {'role': 'system', 'content': prompt.strip()},
    {'role': 'user', 'content': '帮我调整送风模式为高'}]

start_time = time.time()
# print(prompt)
print(ChatClient()._chat(messages=messages))
print(time.time() - start_time)

