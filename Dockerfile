FROM python:3.9

ENV DEPLOY 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python3 manage.py makemigrations", "python3 manage.py migrate",
    "uwsgi --module=DjangoHW.wsgi:application \
        --env DJANGO_SETTINGS_MODULE=DjangoHW.settings \
        --master \
        --http=0.0.0.0:80 \
        --processes=5 \
        --harakiri=20 \
        --max-requests=5000 \
        --vacuum"]