# coding=utf-8

"""

File: sys_consts.py.py

Author: weikaiqiang

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

    VIDEO_DOES_NOT_EXIST = 10404  # video不存在,

    VIDEO_FACE_DOES_NOT_EXIST = 20404  # video_face不存在

    PROJECT_FACE_DOES_NOT_EXIST = 30404  # project_face不存在

    UPLOAD_FILE_PROCESS = 201000  # 视频文件上传中

    VIDEO_PREVIEW_INDEX_ERROR = 10405  # 精细化索引超出超出范围

    PROJECT_NAME_EXISTING = 10405  # 项目名称已存在

