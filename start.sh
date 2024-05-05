python3 manage.py makemigrations user spot msg
python3 manage.py migrate

# Run with uWSGI
uwsgi --module=hiddenCanton.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=hiddenCanton.settings \
    --master \
    --http=0.0.0.0:80 \
    --processes=5 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum