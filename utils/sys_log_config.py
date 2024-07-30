# coding=utf-8

"""

File: sys_log_config.py.py

Author: weikaiqiang

Explanation: 日志配置

Date: 2024/7/30 17:35

"""

import logging
import logging.handlers


# 自定义过滤器
class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,  # 是否要禁用任何现有的非根日志记录器
    'incremental': False,  # 配置是否要被解读为在现有配置上新增 如果 incremental 为 True 则该省会被忽略
    'formatters': {
        'error': {
            'format': '{asctime} {levelname} {message} {pathname} {lineno} {process} {thread}',
            'style': '{',  # 可选 {和$ 格式化中的引用格式
            'validate': True  # 配置日志记录器时是否对验证格式化器进行验证
        },
        'warning': {
            'format': '{asctime} {levelname} {message} {lineno} {process} {thread}',
            'style': '{',
            'validate': True
        },
        'info': {
            'format': '{asctime} {levelname} {message} {process}',
            'style': '{',
            'validate': True
        }
    },
    'filters': {
        'error': {
            '()': ErrorFilter
        },
        'warning': {
            '()': WarningFilter
        },
        'info': {
            '()': InfoFilter
        }
    },
    'handlers': {
        'error': {
            'class': 'logging.handlers.SocketHandler',  # 日志处理类
            'formatter': 'error',  # 对应的日志格式
            'filters': ['error'],  # 过滤器
            # 其他的参数都会以关键字传参的形式传递给日志处理类
            'host': 'localhost',  # 传递给日志处理类的关键字参数
            'port': logging.handlers.DEFAULT_TCP_LOGGING_PORT
        },
        'warning': {
            'class': 'logging.handlers.SocketHandler',
            'formatter': 'warning',
            'filters': ['warning'],
            'host': 'localhost',
            'port': logging.handlers.DEFAULT_TCP_LOGGING_PORT
        },
        'info': {
            'class': 'logging.handlers.SocketHandler',
            'formatter': 'info',
            'filters': ['info'],
            'host': 'localhost',
            'port': logging.handlers.DEFAULT_TCP_LOGGING_PORT
        }
    },
    'loggers': {
        'logger': {
            'propagate': False,
            'handlers': ['info', 'warning', 'error'],
            'level': logging.INFO
        }
    }
}
