FROM python:3.13-slim

# Links the GHCR package back to your source repository
LABEL org.opencontainers.image.source="https://github.com/pymisc/k8s-network-monitor"

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app .

EXPOSE 8080

CMD ["python", "app.py"]