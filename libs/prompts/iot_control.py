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
    我需要你协助我根据聊天对话内容提取成标准的控制IOT设备的JSON数据
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
            {%for command in obj.actions %}动作名称: {{command.command}}, 
                槽位：[{%for slot in command.slots%}{{slot}}){%endfor%}]
        {%endfor%}){%endfor%}
    JSON字段的名称：slotMap，将提取都得对应槽位数据赋值给slotMap字段
    注意区分延迟打开关闭和定时打开关闭的区别,
    槽位提取注意多选值和单选值，没有表明多选值的都是单选值，注意多选值的大小写数字,注意会议控制时的日期提取
    提取槽位值时需要根据聊天记录从槽位的可选值中提取
    设备名称参考IOT设备列表
    规则三: 
    如果槽位信息中包含deviceIndex字段，如果用户明确的表达了需要操作的设备索引并且设备所以在可选值内则输出索引值，如果无法准确的推断出设备索引则deviceIndex的值为"null"用双引号括起来的
    
    完整输出举例：
    案例一：
        文本：打开第一个控制面板 输出: {"domain": "iot-domain", "action": "open_device", "slotMap": {"deviceName": "智能控制面板", "deviceIndex": 1}}
    案例二：
        聊天内容：
        user: 打开第一台空调
        system: 已为您打开第一台空调 
        user: 将送风模式调整为高 
        system: 已将第一台空调送风模式调整为高  
        user: 关闭空调
        system: 已经关闭第一台空调
        user: 打开第二台空调 
        system: 是否确认打开第二台空调 
        user: 确认打开 
        system: 已为您打开第二台空调 
        user: 将送风模式调整为中 
        system: 已将第二台空调送风模式调整为中
        文本：将送风模式调整为高 输出: {"action": "update_device_status", "slotMap": {"deviceName": "空调控制器", "deviceIndex": 2, "deviceStatus": "送风模式设置", "status": "高"}}
        文本：帮我五秒后开启gw开关 输出：{"action": "open_device_regular", "slotMap": {"deviceName": "GW开关", "deviceIndex": "none", "mode": "LATER", "timeValue": 5, "timeCycle": "s"}
        文本：现在的时间时: 2024-09-10 15:00:00 晚上八点关闭电源开关 输出: {"action": "close_device_regular", "slotMap": {"deviceName": "GW开关", "deviceIndex": "none", "mode": "FIX_TIME", "timeValue": "2024-09-10 20:00:00", "timeCycle": "s"}
    现在的聊天对话内容: {% for obj in data.msgs %} {{obj.role}}: {{obj.content}} 
    {% endfor %}聊天内容可能为空
    注意摄像头的复位操作不是reset_device意图属于update_device_status意图，根据规则所有的槽位在对应的可选值中或者根据说明来提取，根据规则槽位信息必须提取完整
    注意，远端合成模式和合成模式是两个不同的命令
    注意，延迟打开和定时打开的命令中需要提取mode槽位的值
    聊天记录的排列顺序是从到近排序从聊天记录中推理信息时查找信息应该从近到远，比如定位需要对那台设备操作时应该从聊天中选择最近操作的那一台设备
    现在的时间是：{{data.DATATIME}}
    按照规则只需要输出JSON数据，在JSON数据前后不需要任何提示或者说明
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
