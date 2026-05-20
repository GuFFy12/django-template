ARG VERSION="unknown"

FROM node:24.14-slim@sha256:b506e7321f176aae77317f99d67a24b272c1f09f1d10f1761f2773447d8da26c AS node-builder
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm/,sharing=locked \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=bind,source=package.json,target=package.json \
    npm ci --omit=dev

FROM python:3.13.12-slim-trixie@sha256:f1927c75e81efd1e091dbd64b6c0ecaa5630b38635a3d1c04034ac636e1f94c8 AS builder
COPY --from=astral/uv:0.11.14@sha256:1025398289b62de8269e70c45b91ffa37c373f38118d7da036fb8bb8efc85d97 /uv /uvx /usr/local/bin
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-editable --no-install-project
COPY . .
COPY --from=node-builder /app/node_modules ./node_modules
RUN uv run python manage.py collectstatic --noinput \
    && uv run python manage.py compress --force \
    && rm -r ./static \
    && rm -r ./node_modules

FROM python:3.13.12-slim-trixie@sha256:f1927c75e81efd1e091dbd64b6c0ecaa5630b38635a3d1c04034ac636e1f94c8
RUN addgroup --system appuser && adduser --system --group appuser
WORKDIR /app
ARG VERSION
ENV VERSION=${VERSION}
ENV DEBUG=False
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder --chown=appuser:appuser /app /app
USER appuser
CMD ["sh", "-c", "exec granian --interface wsgi --host 0.0.0.0 --port 8000 --workers ${GRANIAN_WORKERS:-$((2 * $(nproc) + 1))} config.wsgi:application"]
