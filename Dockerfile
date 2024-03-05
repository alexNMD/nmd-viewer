# syntax=docker/dockerfile:1

FROM python:3.9.5

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

ARG PROJECTS_PATH
ENV PROJECTS_PATH="."

COPY . .

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "app:app"]
