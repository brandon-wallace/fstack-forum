FROM python:3.7.10-slim-buster

WORKDIR /usr/src/application

COPY Pipfile ./

COPY Pipfile.lock ./

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install --no-cache-dir pipenv

RUN pipenv install --system --deploy

EXPOSE 5000

COPY . .

CMD [ "python", "./wsgi.py" ]
