release: python manage.py collectstatic --no-input && python manage.py migrate --run-syncdb
web: gunicorn galavant.wsgi --log-file -