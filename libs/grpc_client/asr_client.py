# coding=utf-8

"""

File: asr_client.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/2 0:41

"""

import grpc
import os
import pickle
import io
from proto.asr_backend.main_pb2_grpc import AsrBackendStub
from proto.asr_backend.main_pb2 import Request
from sys_config import CONFIG


async def audio_to_text(audio: io.BytesIO):
    grpc_addr = f'{os.environ.get("ASR_HOST", CONFIG.ASR_SERVER["host"])}:{os.environ.get("ASR_PROT", CONFIG.ASR_SERVER["prot"])}'
    async with grpc.aio.insecure_channel(grpc_addr) as channel:
        stub = AsrBackendStub(channel)
        req_data = {
            'audio': audio,
            'language': 'zh'
        }
        res = await stub.AudioToText(Request(data=pickle.dumps(req_data)))
        return pickle.loads(res.data)
