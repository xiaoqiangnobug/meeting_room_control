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

    @property
    def _template_content(self):
        return """结合上下文内容根据输入提取JSON数据
        上下文: {% for obj in data.msgs %} {{obj.role}}: {{obj.content}} 
        {% endfor %}
        提取规则如下：
        规则一: 会议控制垂域意图有：{% for obj in data.MEETING_INTENT %}(意图解释: {{obj.name}}, 意图值: {{obj.key}})、{% endfor %}
        JSON字段的名称: action
        例如：修改会议主题的action的值则是feed_meeting_theme
        规则二：基于规则一结果对需要进行的动作进行槽位提取，每个领域的槽位提取说明如下：
        会议控制(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): {%for obj in data.MEETING_INTENT%}
            (会议操作动作: {{obj.name}}) [{% for slot in obj.slots %}{{slot}}{%endfor%}]{%endfor%}
        JSON字段的名称：slotMap，将提取都得对应槽位数据赋值给slotMap字段
        注意开始时间和节数时间的隐藏规则：
            因为时间是不可逆的比如当前时间是 14:00 用户需要要求预约13:00的开始的会议则这个时间条件不存在，需要往后推算寻找匹配的时间明天13:00的事件还存在则判定的时间应该是明天的13:00
        时间信息使用 %Y-%m-%d %H:%M:%S 格式来表示
        严格按照规则来进行识别
        完整输出举例：文本：帮我预约明天的会议 输出: {"action": "book_a_meeting", "slotMap": {"startTime": "2021-08-27 08:00:00", "endTime": "2021-08-27 08:30:00", "meetingTheme": "默认会议"}}
        现在的时间是：{{data.DATATIME}} 直接输出可以使用的JSON原本数据不需要其它任何格式"""

    def _prompt(self):
        data = {
            'MEETING_INTENT': CONFIG.MEETING_INTENT,
            'DATATIME': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        }
        if self.extra_paras is not None:
            data.update(self.extra_paras)
        return Template(source=self._template_content).render(data=data)
