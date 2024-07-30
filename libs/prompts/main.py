# coding=utf-8

"""

File: main.py

Author: weikaiqiang

Explanation: 

Date: 2024/7/30 22:00

"""

from jinja2 import Template
from sys_config import CONFIG

# 控制命令生成Prompt

CONTROL_COMMAND = """
    我需要你协助我将文本内容提取成标准的JSON数据,提取规则如下：
    规则一：将对文本的控制垂域分类一共有三个垂域：
        IOT垂域：主要实现对电灯、空调、音箱、摄像头等智能设备的控制，如开关操作，调整方向操作等 
        会议室控制垂域：主要包括预定、查看、取消会议信息
        闲聊垂域：大模型开放域问答
    JSON字段名称：domain
    例如：
        打开xxx设备，控制IOT设备相关
        domain字段的值是：IOT垂域
        预订明天的会议室，会议控制相关
        domain字段的值是：会议控制
        不是控制IOT和会议相关的就属于,闲聊垂域
        domain字段的值是：闲聊垂域
    按照规则，只需要输出标准的JSON数据即可
"""

prompt = Template(source=CONTROL_COMMAND).render(data={}).strip()
