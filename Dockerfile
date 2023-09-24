FROM python:3.11.5-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOMEBREW_INSTALL_FROM_API 1

RUN apt update -y && apt install -y build-essential libpq-dev wget procps curl file git default-jdk mlocate

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./.env.example /usr/src/app/.env

RUN pip install -r requirements.txt

COPY . /usr/src/app/

RUN chmod -R 777 /usr/src/app/

EXPOSE 8000

CMD ["python", "manage.py", "flush", "--no-input"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
