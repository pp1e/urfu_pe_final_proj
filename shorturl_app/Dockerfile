FROM python:3.12-slim

RUN mkdir data

WORKDIR /app

COPY pyproject.toml poetry.lock shorturl_app ./
RUN pip install poetry
RUN poetry install --no-root --only main

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
