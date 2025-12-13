# syntax=docker/dockerfile:1.10
FROM python:3.12

LABEL MAINTAINER="shimachao@xmov.ai"

# 设置时区
RUN unlink /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 将构建时的 shell 设为 bash
SHELL [ "/bin/bash", "-l", "-c" ]

# 创建项目环境：项目目录、日志目录、Python 虚拟环境目录
ENV PROJECT_DIR=/opt/projects/xmov
ENV LOG_DIR=/opt/logs/xmov
ENV VIRTUAL_ENV=/opt/py_virtualenvs/xmov
ENV UV_CACHE_DIR=/root/.cache/uv
ENV UV_HTTP_TIMEOUT=4000
ENV UV_PYTHON_DOWNLOADS=never

RUN mkdir -p ${PROJECT_DIR} && mkdir -p ${LOG_DIR} mkdir -p ${VIRTUAL_ENV} \
    && touch ${LOG_DIR}/supervisord.log && touch /tmp/supervisord.pid

WORKDIR ${PROJECT_DIR}

# 设置 pypi 源、安装必要的 pip 包、创建 Python 虚拟环境
ARG xmov_host=pypi.local.xmov.ai
ARG xmov_url=http://pypi.local.xmov.ai/xmov/release/+simple/
ARG third_index_url=https://mirrors.huaweicloud.com/repository/pypi/simple

RUN --mount=type=cache,target=/root/.cache/pip \
    pip config set global.trusted-host ${xmov_host} \
    && pip config set global.index-url ${xmov_url} \
    && pip config set global.extra-index-url ${third_index_url} \
    && pip config set global.timeout 60 \
    && pip install -U supervisor uv \
    && uv venv --default-index ${third_index_url} --index ${xmov_url} \
    ${VIRTUAL_ENV}

ENV UV_PROJECT_ENVIRONMENT=${VIRTUAL_ENV}

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    vim \
    curl\
    procps \
    && rm -rf /var/lib/apt/lists/*

# 安装项目依赖
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# 最后添加项目
ADD . ${PROJECT_DIR}/

# 同步项目
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# 增加python快捷方式
RUN echo "alias python='/opt/py_virtualenvs/xmov/bin/python'" >> /root/.bashrc

CMD ["bash", "start.sh"]
