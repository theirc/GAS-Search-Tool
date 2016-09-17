bower install; \
sass ui/static/scss/main.scss > ui/static/scss/main.css; \
python manage.py collectstatic --noinput; \
gunicorn app.wsgi --log-file -