FROM python:3.8.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# VOLUME /app
#
# EXPOSE 8080

CMD python web_service/manage.py makemigrations \
    && python web_service/manage.py migrate \
    && python web_service/manage.py runserver 0.0.0.0:8000



# FROM python:3.8.8
#
# ENV PYTHONUNBUFFERED 1
#
# RUN mkdir -p /app
# RUN git clone https://github.com/idemintsev/api_service.git /app
#
# WORKDIR /app
#
# RUN ls .
#
# RUN pip install -r requirements.txt
#
# VOLUME /app
#
# EXPOSE 8080
#
# CMD python web_service/manage.py makemigrations && python web_service/manage.py migrate && python web_service/manage.py runserver
