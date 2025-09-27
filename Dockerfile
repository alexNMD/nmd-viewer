# syntax=docker/dockerfile:1

FROM python:3.9.5

WORKDIR /nmd-viewer

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "app:app"]
