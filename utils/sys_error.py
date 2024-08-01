# coding=utf-8

"""

File: sys_error.py

Author: xiaoqiang

Explanation: 

Date: 2024/6/3 13:51

"""


class CustomError(Exception):
    def __init__(self, code: int, msg: str):
        """
        :param code: API接口响应状态码,参照全局Code码设计
        :param msg: 提示信息
        """

        self.code = code
        self.msg = msg
