FROM python:3.13.12-trixie@sha256:1cd859c53cde85de47ef35a154e05925d80ff4d133033ef6e2937ed290f27b2e
COPY --from=astral/uv:0.11.14@sha256:1025398289b62de8269e70c45b91ffa37c373f38118d7da036fb8bb8efc85d97 /uv /uvx /usr/local/bin
COPY --exclude=docker-entrypoint.sh --from=node:24.15.0-bookworm-slim@sha256:4e6b70dd6cbfc88c8157ba19aa3d9f9cce6ba4703576d55459e45efcbc9c5f5d /usr/local/bin /usr/local/bin
COPY --from=node:24.15.0-bookworm-slim@sha256:4e6b70dd6cbfc88c8157ba19aa3d9f9cce6ba4703576d55459e45efcbc9c5f5d /opt /opt
COPY --from=node:24.15.0-bookworm-slim@sha256:4e6b70dd6cbfc88c8157ba19aa3d9f9cce6ba4703576d55459e45efcbc9c5f5d /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN apt-get update && apt-get install -y --no-install-recommends \
    git-lfs \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install --system
