FROM python:3.11.6
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV SECRET_KEY ll
ENV DEBUG True
WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /opt/app/django_static/ \
     && mkdir -p /opt/app/django_media/ \
     && python -m pip install --upgrade pip \
     #&& pip install -r requirements.txt \
     && python manage.py collectstatic
CMD ["uwsgi", "--ini", "uwsgi/uwsgi.ini"]
