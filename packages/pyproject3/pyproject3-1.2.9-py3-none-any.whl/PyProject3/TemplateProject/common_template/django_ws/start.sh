#!/bin/bash
source /opt/py_virtualenvs/xmov/bin/activate

echo '-------run migrate start------------'
python manage.py migrate
echo '-------run migrate done------------'

echo '-------run collectstatic start------------'
python manage.py collectstatic --noinput
echo '-------run collectstatic done------------'

supervisord -c ./supervisord.conf

while true; do sleep 3600; done