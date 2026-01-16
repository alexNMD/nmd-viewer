FROM python:3.11-slim

RUN pip install --no-cache-dir "uv[rust]==0.7.19"

WORKDIR /nmdviewer

ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

CMD ["gunicorn", "nmdviewer:app"]
