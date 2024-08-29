# coding=utf-8

"""

File: sys_consts.py.py

Author: xiaoqiang

Explanation: 系统常量

Date: 2024/7/30 17:30

"""


class SysResCode:
    # 系统自定义接口code码

    # 成功Code码
    SUCCESS = 000000
    # 参数校验异常
    PARAM_FORMAT_ERROR = 401000
    # 正常的请求系统允许的操作失败
    # 比如查询id=1的用户信息，但是该用户已经被管理员删除了
    # 比如数据库唯一索引限制
    PARAM_DATA_ERROR = 402000
    # 请求方法不允许
    METHOD_NOT_ALLOWED = 403000
    # 请求路径不存在
    PATH_NOT_FOUND = 404000
    # 数据状态异常拒绝执行
    DATA_STATE_ERROR = 405000
    # 无效的登录信息
    NOT_LOGGED_IN = 406000
    # 未知异常
    UNKNOWN_ERROR = 500000


class SysSpecialResCode:
    # 系统特殊异常码，需要前端接口进行特殊响应时使用的Code码，根据业务定义唯一的

    LLM_ERROR = 10404  # LLM模型推理失败，请检查API-KEY有效性
    LLM_JSON_ERROR = 10405  # LLM提取槽位数据失败，请联系开发人员查看或者提供标准文本
    CHAT_LOG_WARNING = 10406  # 对话信息不存在，可能有效期已过
    ALIYUN_TOKEN_ERROR = 10407  # 阿里云token获取失败

