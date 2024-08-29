# coding=utf-8

"""

File: main.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/28 15:45

"""

import logging
import time

import httpx
from .ali_token import AccessToken
from sys_config import CONFIG
from utils.sys_error import CustomError
from utils.sys_consts import SysResCode

logger = logging.getLogger('logger')


async def audio_to_text(audio: bytes):
    # 语音文件识别
    params = {
        'appkey': CONFIG.ALIYUN_AUDIO['app_key'],
        'format': CONFIG.ALIYUN_AUDIO['format'],
        'sample_rate': CONFIG.ALIYUN_AUDIO['sample_rate'],
        'enable_voice_detection': CONFIG.ALIYUN_AUDIO['enable_voice_detection'],
        'disfluency': CONFIG.ALIYUN_AUDIO['disfluency']
    }
    headers = {
        'X-NLS-Token': f'{await AccessToken().create_token()}',
        'Content-type': 'application/octet-stream',
        'Content-Length': str(len(audio)),
        'Host': 'nls-gateway-cn-beijing.aliyuncs.com'
    }
    print(headers)

    async with httpx.AsyncClient() as client:
        try:
            start_time = time.time()
            res = await client.post(url=CONFIG.ALIYUN_AUDIO['asr_url'], params=params, content=audio, headers=headers)
            result = res.json()['result']
            logger.info(msg=f'语音识别耗时：{time.time() - start_time}，识别结果: {result}')
            return result
        except Exception as e:
            logger.error(msg=f'阿里云语音识别服务出错', exc_info=e)
            raise CustomError(msg='语音识别服务异常，请联系管理员排查', code=SysResCode.UNKNOWN_ERROR)
