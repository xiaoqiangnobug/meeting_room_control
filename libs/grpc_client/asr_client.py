# coding=utf-8

"""

File: asr_client.py

Author: xiaoqiang

Explanation: 

Date: 2024/8/2 0:41

"""

import grpc
import pickle
import io
from proto.asr_backend.main_pb2_grpc import AsrBackendStub
from proto.asr_backend.main_pb2 import Request


async def audio_to_text(audio: io.BytesIO):
    async with grpc.aio.insecure_channel(f"localhost:9001") as channel:
        stub = AsrBackendStub(channel)
        req_data = {
            'audio': audio,
            'language': 'zh'
        }
        res = await stub.AudioToText(Request(data=pickle.dumps(req_data)))
        return pickle.loads(res.data)
