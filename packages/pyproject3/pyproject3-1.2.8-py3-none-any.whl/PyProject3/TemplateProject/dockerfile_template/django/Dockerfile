FROM python:3.12-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROJECT_DIR=/opt/projects/xmov \
    LOG_DIR=/opt/logs/xmov \
    EXTRA_INDEX=https://mirrors.aliyun.com/pypi/simple\
    DJANGO_SETTINGS_MODULE=core.settings

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    supervisor \
    vim \
    curl\
    iputils-ping \
    procps \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 创建项目环境：项目目录、日志目录、Python 虚拟环境目录
RUN mkdir -p /setup && \
    mkdir -p ${PROJECT_DIR} && \
    mkdir -p ${LOG_DIR} && \
    mkdir -p /opt/py_virtualenvs && \
    mkdir -p ${PROJECT_DIR}/static && \
    mkdir -p ${PROJECT_DIR}/media

RUN chmod 777 ${LOG_DIR}

WORKDIR ${PROJECT_DIR}
    
# 复制项目文件
COPY requirements.txt /setup/requirements.txt
RUN pip install -r /setup/requirements.txt

COPY . .
COPY deploy/start.sh .
COPY deploy/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY deploy/nginx/django.conf /etc/nginx/conf.d/default.conf

# 删除默认的nginx配置
RUN rm -f /etc/nginx/sites-enabled/default

# 暴露端口
EXPOSE 8000 80

# 启动命令
CMD ["bash", "start.sh"]