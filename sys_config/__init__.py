# coding=utf-8

"""

File: __init__.py.py

Author: weikaiqiang

Explanation: 

Date: 2024/5/31 14:29

"""
from sys_config.config import config_dict


class Config:
    pass


CONFIG = Config()
for key, value in config_dict.items():
    setattr(CONFIG, key, value)
