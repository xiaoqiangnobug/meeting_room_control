FROM arm64v8/ubuntu:22.04

# 镜像元信息
LABEL MAINTAINER=weikaiqiang
# 环境设置
ENV LANG=C.UTF-8
ENV TZ=Asia/Shanghai

# 安装必要的依赖包
RUN mkdir -p /opt/project /opt/log /opt/py_virtualenvs /opt/setup && \
        chmod 1777 /tmp/ && \
        apt update && \
        apt install --no-install-recommends ca-certificates --reinstall -y

WORKDIR /opt/project/
# 替换镜像源
ADD deployment/files/sources.list /etc/apt/sources.list

RUN DEBIAN_FRONTEND=noninteractive && \
        apt update && \
        apt install --no-install-recommends -y build-essential && \
        apt install --no-install-recommends -y python3.10-dev && \
        apt install --no-install-recommends -y vim && \
        apt install --no-install-recommends -y python3.10 && \
        apt install --no-install-recommends -y python3-virtualenv && \
        apt install --no-install-recommends -y supervisor && \
        apt clean && \
        rm -rf /var/lib/apt/lists/*

# 项目导入
ADD ./ /opt/project/

# supervisor 配置
ADD ./deployment/files/supervisor.conf /etc/supervisor/conf.d/server_supervisor.conf

# 虚拟环境创建&依赖包安装
RUN cd /opt/py_virtualenvs && \
    python3 -m virtualenv -p python3 py && \
    /opt/py_virtualenvs/py/bin/pip install --no-cache-dir -r /opt/project/requirements.txt -i https://mirrors.aliyun.com/pypi/simple && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*


# 设置启动脚本
ADD deployment/files/start.sh /opt/project/start.sh
RUN chmod 777 /opt/project/start.sh


ENTRYPOINT ["/bin/bash", "-c", "/opt/project/start.sh"]