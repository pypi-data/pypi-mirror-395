ARG BASE_IMAGE=python:3.12-slim-bullseye
ARG UV_VERSION=0.7.2

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM ${BASE_IMAGE} AS base

ARG USERNAME=non-root
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

ENV USERNAME=${USERNAME}

RUN set -eux; \
    apt-get update -qq; \
    apt-get install -y --no-install-recommends bash; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid "${USER_GID}" "${USERNAME}"; \
    useradd --uid "${USER_UID}" --gid "${USER_GID}" -m -s /bin/bash "${USERNAME}"

WORKDIR /workspace

ENV PYTHONPATH=/workspace

RUN chown -R "${USERNAME}:${USERNAME}" /workspace /run || true

USER ${USERNAME}

FROM base AS dev
COPY --from=uv /uv /uvx /bin/

FROM dev AS builder
RUN --mount=type=cache,target=/home/${USERNAME}/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=/workspace/pyproject.toml,ro \
    --mount=type=bind,source=uv.lock,target=/workspace/uv.lock,ro \
    uv sync --locked --no-install-project

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/home/${USERNAME}/.cache/uv \
    uv sync --locked
