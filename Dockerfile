FROM python:3.9-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /code

COPY pyproject.toml poetry.lock  ./
COPY src/ ./src
RUN touch README.md

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc
RUN pip install poetry==1.2.2 &&\
    poetry install --no-cache --without test

#final stage
FROM python:3.9-slim as runtime
ENV VIRTUAL_ENV=/code/.venv
ENV PATH="/code/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./.env ./.env
COPY src/ ./src
WORKDIR /src


ENTRYPOINT ["uvicorn", "main:web", "--host", "0.0.0.0", "--port", "8000"]
