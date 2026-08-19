# Python version is controlled by .python-version
ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim

# GHCR package back to the source repository
LABEL org.opencontainers.image.source="https://github.com/pymisc/k8s-network-monitor"

RUN python -m pip install --no-cache-dir --upgrade \
    pip \
    "setuptools>=82.0.0" \
    "wheel>=0.46.2"

WORKDIR /app
COPY requirements.txt .

# Copy the shared project icon into Flask's static directory.
# The source remains under miscellaneous/ so the same icon can
# also be reused by Helm and other project components.
COPY miscellaneous/k8s-network-monitor-icon.png \
     ./app/static/k8s-network-monitor-icon.png

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends iputils-ping && \
    rm -rf /var/lib/apt/lists/*

COPY app ./app

EXPOSE 8080

CMD ["python", "-m", "app.app"]
