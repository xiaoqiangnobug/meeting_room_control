# coding=utf-8

"""

File: chat_control.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/26 15:41

"""

import datetime
from sys_config import CONFIG
from libs.prompts.main import BasePrompt
from jinja2 import Template


class ChatControlPrompt(BasePrompt):

    @property
    def _template_content(self):
        return """
    我需要你协助我根据聊天内容提取成标准的JSON数据
    聊天内容: {% for obj in data.msgs %} {{obj.role}}: {{obj.content}} {% endfor %}
    提取规则如下：
    规则一：根据规则一的判别结果进行意图字段提取，如果没有表明是那个设备可以通过规则的设置支持的动作来推测设备：
        闲聊垂域意图有：{% for obj in data.OPEN_DOMAIN %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
    JSON字段的名称: action
    例如：
        闲聊垂域下,action的值则是chitchat-domain
    规则二：基于规则一的结果对需要进行的动作进行槽位提取，每个领域的槽位提取说明如下：
    开放域问答垂域(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {%for obj in data.OPEN_DOMAIN%}
        (槽位: {{obj.slots}}){%endfor%}
    完整输出举例：
    文本：曹操是谁 输出: {"domain": "chitchat-domain", "action": "llm_chitchat", "slotMap": {"query": "曹操是谁"}}
    现在的时间是：{{data.DATATIME}},按照规则，直接输出可以使用的JSON原本数据不需要其它任何格式
            """

    def _prompt(self):
        data = {
            'OPEN_DOMAIN': CONFIG.OPEN_DOMAIN,
            'DATATIME': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        }
        if self.extra_paras is not None:
            data.update(self.extra_paras)
        return Template(source=self._template_content).render(data=data)
