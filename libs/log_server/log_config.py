# coding=utf-8

"""

File: log_config.py

Author: xiaoqiang

Explanation: 

Date: 2024/5/31 16:22

"""

import logging
import logging.config


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
            # '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '{asctime} {levelname} {message} {pathname} {lineno} {process} {thread}',
            'style': '{',  # 可选 {和$ 格式化中的引用格式
            'validate': True,  # 配置日志记录器时是否对验证格式化器进行验证
            # 'json_ensure_ascii': False
        },
        'warning': {
            # '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '{asctime} {levelname} {message} {lineno} {process} {thread}',
            'style': '{',
            'validate': True,
            # 'json_ensure_ascii': False
        },
        'info': {
            # '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '{asctime} {levelname} {message} {process}',
            'style': '{',
            'validate': True,
            # 'json_ensure_ascii': False
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
            'class': 'logging.handlers.RotatingFileHandler',  # 日志处理类
            'formatter': 'error',  # 对应的日志格式
            'filters': ['error'],  # 过滤器
            # 其他的参数都会以关键字传参的形式传递给日志处理类
            'filename': 'logs/error.log',
            'mode': 'a',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'warning': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'warning',
            'filters': ['warning'],
            'filename': 'logs/waring.log',
            'mode': 'a',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'info',
            'filters': ['info'],
            'filename': 'logs/info.log',
            'mode': 'a',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 20,
            'encoding': 'utf8'
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
