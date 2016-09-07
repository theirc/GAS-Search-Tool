bower install; \
python manage.py collectstatic --noinput; \
gunicorn app.wsgi --log-file -