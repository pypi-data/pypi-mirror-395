FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /build

RUN apk add --no-cache git

COPY .git .git
COPY pyproject.toml README.md ./
COPY src/ src/

RUN uv build --wheel

FROM python:3.14-alpine AS runtime

LABEL description="Code-Reminder aggregation tool"

WORKDIR /work

COPY --from=builder /build/dist/*.whl .

RUN pip install --no-cache-dir *.whl && \
    rm -rf *.whl

ENTRYPOINT ["reminder-aggregator"]
