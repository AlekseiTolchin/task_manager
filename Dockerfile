FROM python:3.11-slim

WORKDIR /app

ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN pip install pipx
RUN PIPX_BIN_DIR=/usr/local/bin pipx install poetry==1.8.4

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-ansi

COPY ./src /app/src
COPY .env /app/
COPY alembic.ini /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
