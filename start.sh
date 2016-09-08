bower install; \
python manage.py compress; \
python manage.py collectstatic --noinput; \
gunicorn app.wsgi --log-file -