# coding=utf-8

"""

File: ali_token.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/29 22:57

"""

import logging
import base64
import hashlib
import hmac
import httpx
import time
import uuid
from urllib import parse
from utils.sys_error_handler import CustomError
from utils.sys_consts import SysSpecialResCode
from sys_config import CONFIG

logger = logging.getLogger('logger')


class AccessToken:
    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

    @staticmethod
    async def create_token(access_key_id=CONFIG.ALIYUN_TOKEN['access_key_id'],
                           access_key_secret=CONFIG.ALIYUN_TOKEN['access_key_secret']):
        parameters = {'AccessKeyId': access_key_id,
                      'Action': 'CreateToken',
                      'Format': 'JSON',
                      'RegionId': 'cn-shanghai',
                      'SignatureMethod': 'HMAC-SHA1',
                      'SignatureNonce': str(uuid.uuid1()),
                      'SignatureVersion': '1.0',
                      'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      'Version': '2019-02-28'}
        # 构造规范化的请求字符串
        query_string = AccessToken._encode_dict(parameters)
        # print('规范化的请求字符串: %s' % query_string)
        # 构造待签名字符串
        string_to_sign = 'GET' + '&' + AccessToken._encode_text('/') + '&' + AccessToken._encode_text(query_string)
        # print('待签名的字符串: %s' % string_to_sign)
        # 计算签名
        secreted_string = hmac.new(bytes(access_key_secret + '&', encoding='utf-8'),
                                   bytes(string_to_sign, encoding='utf-8'),
                                   hashlib.sha1).digest()
        signature = base64.b64encode(secreted_string)
        # print('签名: %s' % signature)
        # 进行URL编码
        signature = AccessToken._encode_text(signature)
        # print('URL编码后的签名: %s' % signature)
        # 调用服务
        full_url = 'http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s' % (signature, query_string)
        # print('url: %s' % full_url)
        # 提交HTTP GET请求
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=full_url)
                root_obj = response.json()
                token = root_obj['Token']['Id']
                expire_time = root_obj['Token']['ExpireTime']
                logger.info(msg=f'获取了阿里云的token 过期时间{expire_time}')
                return token
            except Exception as e:
                logger.error(msg=f'获取阿里云token失败', exc_info=e)
                raise CustomError(msg=f'服务异常获取阿里云token失败', code=SysSpecialResCode.ALIYUN_TOKEN_ERROR)
