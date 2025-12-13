#!/bin/bash
source /opt/py_virtualenvs/xmov/bin/activate

# 启动nginx
service nginx start

# 启动supervisor
supervisord -c /etc/supervisor/supervisord.conf

# 保持容器运行
while true; do sleep 3600; done
