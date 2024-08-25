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
    template_content = """
        我需要你协助我根据聊天内容提取成标准的JSON数据,提取规则如下：
        一共有三个垂域：
            IOT垂域：实现对{% for iot in data.DEVICE_LIST %}{{iot.key}}、{% endfor %}的设备的操作 
            会议控制垂域：预定会议、查看当前用户预约的会议、取消当前用户预定的某个会议
            闲聊垂域：大模型开放域问答
            JSON字段名称：domain
            例如：
            文本是：打开xxx设备，控制IOT设备相关domain字段的值是：iot-domain  文本是：预订明天的会议室，会议控制相关 domain字段的值是：meeting-domain  不是控制IOT和会议相关的就属于闲聊垂域 domain字段的值是：chitchat-domain
            用户最后一次的的输入，直接输出可以使用的JSON原本数据不需要其它任何格式
            """

    def _prompt(self):
        data = {'DEVICE_LIST': CONFIG.DEVICE_LIST}
        return Template(source=self.template_content).render(data=data)
