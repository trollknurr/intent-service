FROM python:3.11-slim-bookworm

RUN apt-get update -qq \
    &&  DEBIAN_FRONTEND=noninteractive \
    apt-get install -y -qq --no-install-recommends \
        build-essential \
        ca-certificates \
    && apt-get clean all \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /app

# Create non-root user
ENV USER=appuser
ENV UID=10001
RUN adduser --disabled-password --gecos "" --shell "/sbin/nologin" --uid "${UID}" "${USER}" && \
    chown -R ${USER}:${USER} /app

USER ${UID}

COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/home/appuser/.cache/uv,uid=${UID} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --locked

ADD --chown=${USER}:${USER} . /app

RUN --mount=type=cache,target=/home/appuser/.cache/uv,uid=${UID} \
    uv sync --locked

CMD ["uv", "run", "fastapi", "run", "src/intent_service/__main__.py"]