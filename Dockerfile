FROM python:3.8.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/ilia/PycharmProjects/DRF/app
RUN git clone https://github.com/idemintsev/api_service.git /home/ilia/PycharmProjects/DRF/app

WORKDIR /home/ilia/PycharmProjects/DRF/app

RUN ls .

RUN pip install -r requirements.txt

VOLUME /home/ilia/PycharmProjects/DRF/app

EXPOSE 8080

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 127.0.0.1:8000