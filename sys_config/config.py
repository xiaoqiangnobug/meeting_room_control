# coding=utf-8

"""

File: config.py

Author: xiaoqiang

Explanation: 

Date: 2024/5/31 17:16

"""

import yaml

with open(file='sys_config/config.yaml', mode='r', encoding='utf8') as f:
    config_dict = yaml.safe_load(f)
