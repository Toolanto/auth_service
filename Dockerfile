FROM python:3.9

WORKDIR /code

#
COPY ./pyproject.toml ./pyproject.toml
COPY ./.env ./.env
COPY src/ ./src
COPY README.md README.md

#
RUN pip install poetry==1.2.2
RUN poetry install --no-cache --without test

#
CMD ["poetry", "run", "uvicorn", "main:web", "--host", "0.0.0.0", "--port", "8000"]
