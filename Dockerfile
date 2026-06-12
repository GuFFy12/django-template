ARG VERSION="unknown"

FROM python:3.14.6-slim-trixie@sha256:c79315c9ba2403aecb221fb9090486be9af43cdc2372959ca7ccf6b17ebe9912 AS builder
COPY --from=astral/uv:0.11.14@sha256:1025398289b62de8269e70c45b91ffa37c373f38118d7da036fb8bb8efc85d97 /uv /uvx /usr/local/bin
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_SYNC=1
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-editable --no-install-project
COPY . .
RUN uv run python manage.py collectstatic --noinput

# Проект иммутабельный, вы не можете никуда писать (кроме media).

FROM python:3.14.6-slim-trixie@sha256:c79315c9ba2403aecb221fb9090486be9af43cdc2372959ca7ccf6b17ebe9912
WORKDIR /app
RUN adduser --system --group app
ARG VERSION
ENV VERSION=${VERSION}
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=builder /opt/venv /opt/venv
# --chown=app:app если вам НУЖНО писать.
COPY --from=builder /app /app
# При s3 убрать.
RUN chown -R app:app /app/media
USER app
