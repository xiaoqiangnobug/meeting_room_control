# coding=utf-8

"""

File: main.py

Author: xiaoqiang

Explanation: 

Date: 2024/5/31 16:24

"""

import os
import sys

# 解决非目录，导包问题

sys.path.insert(0, os.getcwd())

import pickle
import logging
import logging.handlers
import socketserver
import struct
import select
import logging.config
import logging.handlers
from libs.log_server.log_config import LOG_CONFIG

# 加载日志配置
logging.config.dictConfig(LOG_CONFIG)


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """
    日志数监听并处理
    """

    def handle(self):
        """
        数据监听并还原为LogRecord对象
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = pickle.loads(chunk)
            record = logging.makeLogRecord(obj)
            self.handle_log_record(record)

    @staticmethod
    def handle_log_record(record: logging.LogRecord):
        # 监听进程的logger配置应该和推送端保持一致
        name = record.name
        logger = logging.getLogger(name)
        logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    创建socketserver服务并检测服务状态直到结束
    """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1

    def serve_until_stopped(self):
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


if __name__ == '__main__':
    LogRecordSocketReceiver().serve_until_stopped()
