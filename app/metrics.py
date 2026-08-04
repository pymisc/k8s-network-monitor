"""
Prometheus metrics used by k8s-network-monitor.
"""

from prometheus_client import Gauge

internet_download_mbps = Gauge(
    "internet_download_mbps",
    "Current internet download bandwidth in Mbps"
)

internet_ping_latency_ms = Gauge(
    "internet_ping_latency_ms",
    "Current internet ping latency in milliseconds",
)