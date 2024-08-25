# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import ChatClient
from libs.prompts import DivideDomainPrompt, PROMPT, MeetingControlPrompt

messages = [
    {'role': 'system', 'content': MeetingControlPrompt().prompt},
    {'role': 'user', 'content': "帮我约个7点到8点的会"},
    {'role': 'system', 'content': '好的，帮你越好了'},
    {'role': 'user', 'content': '时间不合适帮我取消吧'}
]
s = [{'role': 'system',
      'content': '\n        我需要你协助我根据聊天内容提取成标准的JSON数据,提取规则如下：\n        一共有三个垂域：\n            IOT垂域：实现对摄像头、空间人数传感器、智能控制面板、窗帘、TCP插座、GW插座(电源插座)、GW开关(灯开关)、电源时序器、环境检测、空调控制器、录播主机、的设备的操作 \n            会议控制垂域：预定会议、查看当前用户预约的会议、取消当前用户预定的某个会议\n            闲聊垂域：大模型开放域问答\n            JSON字段名称：domain\n            例如：\n            文本是：打开xxx设备，控制IOT设备相关domain字段的值是：iot-domain  文本是：预订明天的会议室，会议控制相关 domain字段的值是：meeting-domain  不是控制IOT和会议相关的就属于闲聊垂域 domain字段的值是：chitchat-domain\n            用户最后一次的的输入，直接输出可以使用的JSON原本数据不需要其它任何格式\n            '},
     {'role': 'user', 'content': '帮我约个下午三点的会'}, {'role': 'system', 'content': '好的，预约好了'},
     {'role': 'user', 'content': '取消吧'}, {'role': 'system', 'content': '好的已取消'},
     {'role': 'user', 'content': '查询下午两点的会议信息'}]

start_time = time.time()
print(ChatClient()._json_chat(messages=s))
print(time.time() - start_time)
