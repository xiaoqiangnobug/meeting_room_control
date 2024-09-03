# coding=utf-8

"""

File: test.py

Author: xiaoqiang

Explanation: 

Date: 2024/7/30 21:55

"""

import time
from libs.llm_chat import chat_client_ty_plus
from libs.prompts import DivideDomainPrompt, MeetingControlPrompt, IotControlPrompt

extra_paras = {'msgs': [
    {
        "role": "user",
        "content": "预订会议"
    },
    {
        "role": "system",
        "content": "好的，帮您预约了2024-09-04 17:32:39开始，2024-09-04 18:02:39结束的会议"}

]}

messages = [
    {'role': 'user', 'content': MeetingControlPrompt(extra_paras=extra_paras).prompt},
    {'role': 'user', 'content': "查看会议信息"}
]

ddd = [{'role': 'system',
        'content': '我需要你协助我根据聊天内容提取成标准的控制IOT设备的JSON数据\n        提取规则如下：\n        规则一: 会议控制垂域意图有：(意图解释: 预定会议, 意图值: book_a_meeting)、(意图解释: 查看会议信息, 意图值: check_meeting_schedule)、(意图解释: 取消当前用户预定的某个会议, 意图值: cancel_a_meeting)、(意图解释: 会议时间填充 (对话中未指明确定的 会议时间，使用的是默认时间时), 意图值: feed_meeting_time)、(意图解释: 修改会议主题, 意图值: feed_meeting_theme)、(意图解释: 会议时间修改 (对话中明确指定了时间之后继续修改时间), 意图值: update_meeting_time)、\n        JSON字段的名称: action\n        例如：修改会议 主题的action的值则是feed_meeting_theme\n        规则二：基于规则一结果对需要进行的动作进行槽位提取，每个领域的槽位提取说明如下：\n        会议控制(槽位信息中key是对应JSON的输出字段，desc是槽位解释，values是取值范围，如果取值范围空则需要根据文本提取): \n            (会议操作动作: 预定会议) [{\'desc\': \'会议开始时间,如果没有明确日期时间默认使用当前时间为开始时间\', \'key\': \'startTime\'}{\'desc\': \'会议结束时间，（如果没有给定具体时间，结束时间就是开始时间半个小时之后）\', \'key\': \'endTime\', \'values\': []}{\'key\': \'meetingTheme\', \'desc\': \'会议名称（从对话信息中提取，默认值（默认会议））\', \'values\': []}]\n            (会议操作动作: 查看会 议信息) [{\'desc\': \'会议预约人\', \'key\': \'owner\', \'values\': []}{\'key\': \'startTime\', \'desc\': \'刚刚预订的的会议开始时间，默认时间使用当前时间\', \'values\': []}{\'desc\': \'刚刚预订的会议结束时间，默认时间使用开始时间30分钟后\', \'key\': \'endTime\', \'values\': []}]\n            (会议操作动作: 取消当前用户预定的某个会议) [{\'key\': \'startTime\', \'desc\': \'会议开始时间,默认开始时间当前时间\', \'values\': []}{\'desc\': \'会议结束时间\', \'key\': \'endTime\', \'values\': []}]\n            (会议操作动作: 会议 时间填充 (对话中未指明确定的会议时间，使用的是默认时间时)) [{\'key\': \'startTime\', \'desc\': \'会议开始时间,默认开始时间当前时间\', \'values\': []}{\'desc\': \'会议结束时间\', \'key\': \'endTime\', \'values\': []}]\n            (会议操作动作: 修改会议主题) [{\'key\': \'meetingTheme\', \'desc\': \'需要修改的会议主题\', \'values\': []}]\n            (会议操作动作: 会议时间修改 (对话中明确指定 了时间之后继续修改时间)) [{\'key\': \'startTime\', \'desc\': \'会议开始时间,默认开始时间当前时间\', \'values\': []}{\'desc\': \'会议结束时间\', \'key\': \'endTime\', \'values\': []}]\n        JSON字段的名称：slotMap，将提取都得对应槽位数据赋值给slotMap字段\n        注意开始时间和节数时间的隐藏规则：\n            因为时间是不可逆的比如当前时间是 14:00 用户需要要求预约13:00的开始的会议则这个时间条件不存在，需要往后推算寻找匹配的时间明天13:00的事件还存在则判定的时间应该是明天的13:00\n        时间信息使用 %Y-%m-%d %H:%M:%S 格 式来表示\n         聊天内容: \n         聊天内容可能为空\n        完整输出举例：\n        聊天内容：\n            user: 预订会议 \n            system: 好的已经帮您预约了，2024-08-28 16:00:00开始2024-08-28 18:00:00结束会议 \n            文本：查看我的会议信息\n            输出：{"action": "check_meeting_schedule", "slotMap": {"startTime": "2024-08-28 16:00:00", "endTime": "2024-08-28 18:00:00"}}\n        注意：查看会议信息意图时，开始和结束时间首先从聊天记录中寻找，没有明确时间时再使用默认时间\n        现在的时间是：2024-09-03 23:31:51 结合聊天记录推测目前用户要进行的操作按按照规则直接输出可以使用的JSON原本数据不需任何格式'},
       {'role': 'user', 'content': '查看会议信息'}]

print(ddd[0]['content'])
print(MeetingControlPrompt(extra_paras=extra_paras).prompt)
for _ in range(2):
    start_time = time.time()
    print(chat_client_ty_plus._chat(messages=ddd))
    print(chat_client_ty_plus._chat(messages=messages))
    print(time.time() - start_time)
