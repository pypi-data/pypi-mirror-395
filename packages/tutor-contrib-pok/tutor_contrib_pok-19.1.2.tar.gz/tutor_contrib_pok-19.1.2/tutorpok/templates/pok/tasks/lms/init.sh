dockerize -wait tcp://{{ MYSQL_HOST }}:{{ MYSQL_PORT }} -timeout 20s

echo "Loading settings $DJANGO_SETTINGS_MODULE"

./manage.py lms migrate openedx_pok
