FROM python:3.8.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

WORKDIR /app

# RUN git clone https://github.com/idemintsev/api_service.git /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN ls .

COPY . .

# VOLUME /app

EXPOSE 8080

CMD python web_service/manage.py makemigrations \
    && python web_service/manage.py migrate \
    && python web_service/manage.py runserver 0.0.0.0:8080
