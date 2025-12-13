#!/bin/bash
source /opt/py_virtualenvs/xmov/bin/activate

# 创建静态文件目录
mkdir -p /opt/projects/xmov/static
mkdir -p /opt/projects/xmov/media

# 收集静态文件
python manage.py collectstatic --noinput

# 迁移数据库
python manage.py migrate

# 启动nginx
service nginx start

# 启动supervisor
supervisord -c /etc/supervisor/supervisord.conf

# 保持容器运行
while true; do sleep 3600; done
