# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import ChatClient
from libs.prompts.main import PROMPT
print(PROMPT.control)
messages = [
    {'role': 'system', 'content': PROMPT.control},
    {'role': 'user', 'content': '帮我约个7点到8点的会，会叫aaa'}]

start_time = time.time()
print(ChatClient()._chat(messages=messages))
print(time.time() - start_time)

