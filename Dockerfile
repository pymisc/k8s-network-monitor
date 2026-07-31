# Python version is controlled by .python-version
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim
#old# FROM python:3.13-slim

# Links the GHCR package back to your source repository
LABEL org.opencontainers.image.source="https://github.com/pymisc/k8s-network-monitor"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8080

CMD ["python", "-m", "app.app"]
