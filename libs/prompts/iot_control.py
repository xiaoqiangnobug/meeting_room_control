# coding=utf-8

"""

File: iot_control.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/26 15:37

"""

import datetime
from sys_config import CONFIG
from libs.prompts.main import BasePrompt
from jinja2 import Template


class IotControlPrompt(BasePrompt):

    @property
    def _template_content(self):
        return """
    我需要你协助我根据聊天内容提取成标准的控制IOT设备的JSON数据
    提取规则如下：
    IOT垂域：实现对 {% for iot in data.DEVICE_LIST %}{{iot.key}}、{% endfor %}的设备的操作 
    规则一：意图字段提取，如果没有表明是那个设备可以通过规则的设置支持的动作来推测设备：
        IOT垂域的意图有: {% for obj in data.IOT_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
    JSON字段的名称: action
    例如：
        IOT垂域下,打开xxx设备 action的值则是IOT垂域意图中打开动作的意图值
    规则二：基于规则一的结果对需要进行的动作进行槽位提取，每个领域的槽位提取说明如下：
    IOT设备控制(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {% for obj in data.DEVICE_LIST %}
        (设备名称：{{obj.key}} 
        {%for command in obj.actions %}动作名称: {{command.command}}, 槽位：[{%for slot in command.slots%}{{slot}}){%endfor%}]{%endfor%}){%endfor%}
    JSON字段的名称：slotMap，将提取都得对应槽位数据赋值给slotMap字段
    注意区分延迟打开关闭和定时打开关闭的区别,
    槽位提取注意多选值和单选值，没有表明多选值的都是单选值，注意多选值的大小写数字,注意会议控制时的日期提取
    提取槽位值时需要根据聊天记录从槽位的可选值中提取
    设备名称参考IOT设备列表
    规则三: 
    如果槽位信息中包含deviceIndex字段，如果用户明确的表达了需要操作的设备索引并且设备所以在可选值内则输出索引值，如果无法准确的推断出设备索引则deviceIndex的值为None
    
    聊天内容: {% for obj in data.msgs %} {{obj.role}}: {{obj.content}} 
    {% endfor %}聊天内容可能为空
    完整输出举例：
    文本：帮我禁用蜂鸣模式 输出: {"domain": "iot-domain", "action": "update_device_status", "slotMap": {"deviceName": "环境检测", "deviceStatus": "蜂鸣模式设置", "status": "禁用"}}
    现在的时间是：{{data.DATATIME}},结合上下文推测目前用户要进行的操作按按照规则直接输出可以使用的JSON原本数据不需要其它任何格式
            """

    def _prompt(self, **kwargs):
        data = {
            'IOT_INTENT': CONFIG.IOT_INTENT,
            'DEVICE_LIST': CONFIG.DEVICE_LIST,
            'DATATIME': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        }
        if self.extra_paras is not None:
            data.update(self.extra_paras)
        return Template(source=self._template_content).render(data=data)
