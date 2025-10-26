# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install .

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "nmd_viewer:app"]
