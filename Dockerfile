FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server.py .
RUN python -m pip install --no-cache-dir pyinstaller
RUN pyinstaller --onefile --name http-server server.py

FROM debian:stable-slim
RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /app/dist/http-server /app/server
RUN chmod +x /app/server && chown appuser:appuser /app/server
USER appuser
ENTRYPOINT ["/app/server"]
