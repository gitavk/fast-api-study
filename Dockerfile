FROM python:3.9 as builder

COPY ./pyproject.toml ./poetry.lock /

ENV PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.11

# System deps:
RUN pip install "poetry==$POETRY_VERSION" \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-dev --no-interaction --no-ansi

FROM python:3.9-slim

COPY --from=builder /.venv /venv

COPY . .

CMD ["/venv/bin/python", "/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
