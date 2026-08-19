"""
Main Flask application for k8s-network-monitor.

This module exposes HTTP endpoints used for:
- Application availability checks
- Kubernetes health probes
- Future Prometheus metrics integration
"""

from flask import Flask, render_template_string
from .scheduler import start_scheduler
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .metrics import (
    internet_download_mbps,
    internet_ping_latency_ms,
)

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
    Human-friendly application status page.

    Displays:
    - Application running status
    - Latest download bandwidth measurement
    - Latest ping latency measurement
    - Links to health and Prometheus metrics endpoints
    """

    download_speed = internet_download_mbps._value.get()
    ping_latency = internet_ping_latency_ms._value.get()

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>k8s-network-monitor</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f5f7fa;
                    color: #1f2937;
                    margin: 0;
                    padding: 40px;
                    text-align: center;
                }

                .card {
                    background: white;
                    max-width: 650px;
                    margin: auto;
                    padding: 35px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.10);
                }

                .logo {
                    width: 170px;
                    margin-bottom: 15px;
                }

                h1 {
                    margin-bottom: 5px;
                }

                .subtitle {
                    color: #6b7280;
                    margin-bottom: 25px;
                }

                .status {
                    display: inline-block;
                    padding: 6px 14px;
                    border-radius: 20px;
                    background: #dcfce7;
                    color: #166534;
                    font-weight: bold;
                    margin-bottom: 30px;
                }

                .metrics {
                    display: flex;
                    gap: 20px;
                    justify-content: center;
                    flex-wrap: wrap;
                }

                .metric {
                    background: #f8fafc;
                    border: 1px solid #e5e7eb;
                    border-radius: 10px;
                    padding: 20px;
                    min-width: 200px;
                }

                .metric-name {
                    color: #6b7280;
                    font-size: 14px;
                }

                .metric-value {
                    font-size: 30px;
                    font-weight: bold;
                    margin-top: 8px;
                }

                .links {
                    margin-top: 30px;
                }

                .links a {
                    margin: 0 12px;
                    text-decoration: none;
                    color: #2563eb;
                    font-weight: bold;
                }
            </style>
        </head>

        <body>

            <div class="card">

                <img
                    class="logo"
                    src="/static/k8s-network-monitor-icon.png"
                    alt="k8s-network-monitor"
                >

                <h1>k8s-network-monitor</h1>

                <div class="subtitle">
                    Kubernetes Network Monitoring
                </div>

                <div class="status">
                    ● Running
                </div>

                <div class="metrics">

                    <div class="metric">
                        <div class="metric-name">
                            Download Speed
                        </div>

                        <div class="metric-value">
                            {{ "%.2f"|format(download_speed) }} Mbps
                        </div>
                    </div>

                    <div class="metric">
                        <div class="metric-name">
                            Ping Latency
                        </div>

                        <div class="metric-value">
                            {{ "%.1f"|format(ping_latency) }} ms
                        </div>
                    </div>

                </div>

                <div class="links">
                    <a href="/health">Health</a>
                    <a href="/metrics">Prometheus Metrics</a>
                </div>

            </div>

        </body>
        </html>
        """,
        download_speed=download_speed,
        ping_latency=ping_latency,
    )

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
