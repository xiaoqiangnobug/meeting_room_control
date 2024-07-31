# coding=utf-8

"""

File: main.py

Author: weikaiqiang

Explanation: 

Date: 2024/7/30 22:00

"""

import datetime
from jinja2 import Template
from sys_config import CONFIG

# 控制命令生成Prompt

data = {
    'iot_device': [obj['key'] for obj in CONFIG.DEVICE_LIST],
    'IOT_INTENT': CONFIG.IOT_INTENT,
    'MEETING_INTENT': CONFIG.MEETING_INTENT,
    'OPEN_DOMAIN': CONFIG.OPEN_DOMAIN,
    'datatime': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
}

CONTROL_COMMAND = """
    我需要你协助我将文本内容提取成标准的JSON数据,提取规则如下：
    规则一：将对文本的控制垂域分类一共有三个垂域：
        IOT垂域：实现对 {% for iot in data.iot_device %}{{iot}}、{% endfor %}的设备的操作 
        会议控制垂域：预定会议、查看当前用户预约的会议、取消当前用户预定的某个会议
        闲聊垂域：大模型开放域问答
    JSON字段名称：domain
    例如：
        文本是：打开xxx设备，控制IOT设备相关 domain字段的值是：iot-domain
        文本是：预订明天的会议室，会议控制相关 domain字段的值是：meeting-domain
        不是控制IOT和会议相关的就属于闲聊垂域 domain字段的值是：chitchat-domain
    规则二：根据规则一的判别结果进行意图字段提取：
        IOT垂域的意图有: {% for obj in data.IOT_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}}，需要提取的槽位: [{%for slot in obj.slots%}(槽位JSON字段值:{{slot.key}}, 槽位解释: {{slot.name}}){%endfor%}])、{% endfor %}
        会议控制垂域意图有：{% for obj in data.MEETING_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
        闲聊垂域意图有：{% for obj in data.OPEN_DOMAIN %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
    JSON字段的名称: action
    例如：
        IOT垂域下,打开xxx设备 action的值则是IOT垂域意图中打开动过的意图值
    规则三：基于规则一和规则二的结果进行数据槽位提取，
        槽位数据参考规则二中的槽位说明，所有的槽位信息提取成一个完成的JSON
        时间值的：时间格式为: %Y-%m-%d %H:%M:%S， 现在的时间是 {{data.datatime}}
        时间单位：时: h 分：m 秒: s
        设备名称参考规则一中的设备名称
    JSON字段的名称：slotMap
    按照规则，直接输出可以使用的JSON原本数据不需要其它任何格式
"""

prompt = Template(source=CONTROL_COMMAND).render(data=data).strip()
