ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
ARG APP_USER=python
ARG PACKAGE_VERSION=''
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    ${APP_USER}

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install clickhouse-table-exporter==${PACKAGE_VERSION}

USER ${APP_USER}

COPY . .

EXPOSE 9001

CMD /usr/local/bin/python3 /usr/local/lib/python3.9/site-packages/exporter.py
