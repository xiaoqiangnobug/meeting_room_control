#!/bin/bash

service supervisor stop
service nginx start

cd /opt/project

# 可以在服务启动前随意增加自定义功能

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf

# 可以在服务启动后随意增加自定义功能
while true; do sleep 1d; done