FROM python:3.8.8
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

WORKDIR /app

# RUN git clone https://github.com/idemintsev/api_service.git /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN ls .

COPY . .

# VOLUME /app

EXPOSE 8000

CMD python web_service/manage.py makemigrations \
    && python web_service/manage.py migrate \
    && python web_service/manage.py runserver 0.0.0.0:8000
