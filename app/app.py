"""
Main Flask application for k8s-network-monitor.

This module exposes HTTP endpoints used for:
- Application availability checks
- Kubernetes health probes
- Future Prometheus metrics integration
"""

from flask import Flask
from .scheduler import start_scheduler
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Create Flask application instance.
# This object is imported by:
# - Gunicorn (future production deployment)
# - pytest (automated testing)
# - Kubernetes container runtime
app = Flask(__name__)


# Start background metric collection scheduler.
start_scheduler()

@app.route("/")
def root():
    """
    Root endpoint.

    Provides a simple response confirming that the
    application container is running successfully.
    """
    return "k8s-network-monitor is running!"


@app.route("/health")
def health():
    """
    Health check endpoint.

    Kubernetes can use this endpoint for:
    - livenessProbe
    - readinessProbe

    A successful response indicates that the
    application process is healthy.
    """
    return {"status": "ok"}

@app.route("/metrics")
def metrics():
    """
    Prometheus metrics endpoint.

    Prometheus scrapes this endpoint periodically
    to collect application metrics.
    """
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

# Allow the application to be started directly:
#
#     python app.py
#
# In Kubernetes, this will normally be replaced by
# a production WSGI server such as Gunicorn.
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
