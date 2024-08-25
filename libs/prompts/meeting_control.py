# coding=utf-8

"""

File: meeting_control.py

Author: xiaoqiang

Explanation: 会议控制领域

Date: 2024/8/25 23:31

"""

import datetime
from sys_config import CONFIG
from libs.prompts.main import BasePrompt
from jinja2 import Template


class MeetingControlPrompt(BasePrompt):
    template_content = """
    我需要你协助我根据聊天内容提取成标准的JSON数据,提取规则如下：
    规则一:
        会议控制垂域意图有：{% for obj in data.MEETING_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
    JSON字段的名称: action
    例如：
        预订会议 action的值则是book_a_meeting
    规则二：基于规则一结果对需要进行的动作进行槽位提取，每个领域的槽位提取说明如下：
    会议控制(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {%for obj in data.MEETING_INTENT%}
        (会议操作动作: {{obj.name}}) [{% for slot in obj.slots %}{{slot}}{%endfor%}]{%endfor%}
    JSON字段的名称：slotMap，将提取都得对应槽位数据赋值给slotMap字段
    槽位提取注意没有表明多选值的都是单选值,注意会议控制时的日期提取,
    时间信息使用 %Y-%m-%d %H:%M:%S 格式来表示
    严格按照规则来进行识别
    完整输出举例：
    文本：帮我预约明天的会议 输出: {"action": "book_a_meeting", "slotMap": {"deviceName": "环境检测", "deviceStatus": "蜂鸣模式设置", "status": "禁用"}}
    现在的时间是：{{data.DATATIME}} 直接输出可以使用的JSON原本数据不需要其它任何格式
            """

    def _prompt(self):

        data = {
            'MEETING_INTENT': CONFIG.MEETING_INTENT,
            'DATATIME': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        }
        return Template(source=self.template_content).render(data=data)
