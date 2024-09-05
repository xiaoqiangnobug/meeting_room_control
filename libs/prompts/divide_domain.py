# coding=utf-8

"""

File: divide_domain.py

Author: weikaiqiang

Explanation: 垂域划分

Date: 2024/8/15 21:25

"""

from sys_config import CONFIG
from libs.prompts.main import BasePrompt
from jinja2 import Template


class DivideDomainPrompt(BasePrompt):

    @property
    def _template_content(self):
        return """
        我需要你协助我根据聊天内容提取成标准的JSON数据
        提取规则如下：
        一共有三个垂域：
            IOT垂域：实现对{% for iot in data.DEVICE_LIST %}
                {{iot.key}}的：{% for obj in iot.actions %} {{obj.command}}、{% endfor %}的操作{% endfor %}的设备的操作 
            会议控制垂域：预定会议、查看当前用户预约的会议、取消当前用户预定的某个会议
            闲聊垂域：大模型开放域问答
            JSON字段名称：domain
            实例：
            文本是：对xxx设备操作相关，对IOT设备操作相关domain字段的值是: iot-domain 
            文本是：预订明天的会议室，对会议控制相关domain字段的值是: meeting-domain
            不是控制IOT和会议相关的就属于闲聊垂域domain字段的值是: chitchat-domain
            聊天内容: {% for obj in data.msgs %} 
            {{obj.role}}: {{obj.content}} {% endfor %}
            聊天记录肯可能为空 
            推理IOT设备推理时有一点需要注意下，如果用户表达的是 不打开xxx这样的否定词可以归类为关闭xxx设备
            结合聊天记录根据规则提取直接按照要求输出结果不需要其他任何输出
            """

    def _prompt(self):
        data = {'DEVICE_LIST': CONFIG.DEVICE_LIST}
        if self.extra_paras is not None:
            data.update(self.extra_paras)
        return Template(source=self._template_content).render(data=data)
