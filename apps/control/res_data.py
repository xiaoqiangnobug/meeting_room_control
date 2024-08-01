# coding=utf-8

"""

File: res_data.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/2 0:06

"""

from marshmallow import Schema, fields


class ControlChatResData(Schema):
    # 会议控制接口响应

    class _IntentRes(Schema):
        query = fields.Str()
        domain = fields.Str()
        action = fields.Str()
        dialogStatus = fields.Dict(default={'status': 'FINISH', 'turns': 1})
        slotMap = fields.Dict(attribute='slot_map')

    event = fields.Str(default='INTENT')
    result = fields.Nested(nested=_IntentRes(), many=False)
