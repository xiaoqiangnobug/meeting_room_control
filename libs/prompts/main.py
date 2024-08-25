# coding=utf-8

"""

File: main.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 22:00

"""

import datetime
from jinja2 import Template
from sys_config import CONFIG

# 控制命令生成Prompt

data = {
    'DEVICE_LIST': CONFIG.DEVICE_LIST,
    'IOT_INTENT': CONFIG.IOT_INTENT,
    'MEETING_INTENT': CONFIG.MEETING_INTENT,
    'OPEN_DOMAIN': CONFIG.OPEN_DOMAIN,
    'DATATIME': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
}
""" (动作：{{command.command}}, 槽位信息：({% for slot in command.slots %}[字段key: {{slot.key}},槽位含义：{{slot.desc}}, 槽位可选值: [{%for value in slot.values%}{%endfor%}]]{%endfor%})){%endfor%}"""
CONTROL_COMMAND = """
    我需要你协助我根据聊天内容提取成标准的JSON数据,提取规则如下：
    规则一：将对文本的控制垂域分类一共有三个垂域：
        IOT垂域：实现对 {% for iot in data.DEVICE_LIST %}{{iot.key}}、{% endfor %}的设备的操作 
        会议控制垂域：预定会议、查看当前用户预约的会议、取消当前用户预定的某个会议
        闲聊垂域：大模型开放域问答
    JSON字段名称：domain
    例如：
        文本是：打开xxx设备，控制IOT设备相关 domain字段的值是：iot-domain  文本是：预订明天的会议室，会议控制相关 domain字段的值是：meeting-domain  不是控制IOT和会议相关的就属于闲聊垂域 domain字段的值是：chitchat-domain
    规则二：根据规则一的判别结果进行意图字段提取，如果没有表明是那个设备可以通过规则的设置支持的动作来推测设备：
        IOT垂域的意图有: {% for obj in data.IOT_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
        会议控制垂域意图有：{% for obj in data.MEETING_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
        闲聊垂域意图有：{% for obj in data.OPEN_DOMAIN %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
    JSON字段的名称: action
    例如：
        IOT垂域下,打开xxx设备 action的值则是IOT垂域意图中打开动过的意图值
    规则三：基于规则一和规则二的结果对需要进行的动作进行槽位提取，每个领域的槽位提取说明如下：
    IOT设备控制(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {% for obj in data.DEVICE_LIST %}
        (设备名称：{{obj.key}} 
        {%for command in obj.actions %}动作名称: {{command.command}}, 槽位：[{%for slot in command.slots%}{{slot}}){%endfor%}]{%endfor%}){%endfor%}
    会议控制(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {%for obj in data.MEETING_INTENT%}
        (会议操作动作: {{obj.name}}) [{% for slot in obj.slots %}{{slot}}{%endfor%}]{%endfor%}
    JSON字段的名称：slotMap，将提取都得对应槽位数据赋值给slotMap字段
    注意区分延迟打开关闭和定时打开关闭的区别,槽位提取注意多选值和单选值，没有表明多选值的都是单选值，注意多选值的大小写数字,注意会议控制时的日期提取
    开放域问答垂域(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {%for obj in data.OPEN_DOMAIN%}
        (槽位: {{obj.slots}}){%endfor%}
    完整输出举例：
    文本：帮我禁用蜂鸣模式 输出: {"domain": "iot-domain", "action": "update_device_status", "slotMap": {"deviceName": "环境检测", "deviceStatus": "蜂鸣模式设置", "status": "禁用"}}
    现在的时间是：{{data.DATATIME}},按照规则，直接输出可以使用的JSON原本数据不需要其它任何格式
"""


# prompt = Template(source=CONTROL_COMMAND).render(data=data).strip()


class Prompt:
    # Prompt模板统一管理

    @property
    def control(self):
        data = {
            'DEVICE_LIST': CONFIG.DEVICE_LIST,
            'IOT_INTENT': CONFIG.IOT_INTENT,
            'MEETING_INTENT': CONFIG.MEETING_INTENT,
            'OPEN_DOMAIN': CONFIG.OPEN_DOMAIN,
            'DATATIME': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        }

        return Template(source=CONTROL_COMMAND).render(data=data).strip()


PROMPT = Prompt()


class BasePrompt:

    @property
    def prompt(self):
        return self._prompt()

    def _prompt(self):
        raise Exception('子类实现')
