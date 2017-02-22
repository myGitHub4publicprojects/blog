web: gunicorn blog.wsgi
worker: celery -A blog worker -B --loglevel=info