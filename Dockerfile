FROM python:3.10-slim

ENV POETRY_VERSION=1.4.0 \
    POETRY_HOME="/poetry"
ENV PATH="$PATH:$POETRY_HOME/bin"

ARG POETRY_SCRIPT="https://install.python-poetry.org"

RUN  apt-get update \
     && apt-get install -y wget \
     && rm -rf /var/lib/apt/lists/* \

WORKDIR /install
RUN wget ${POETRY_SCRIPT} -O ./install_poetry.py && python3 ./install_poetry.py


WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./src/ /code/src

RUN useradd -ms /bin/bash user
USER user

EXPOSE 80
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
