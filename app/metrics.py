"""
Prometheus metrics used by k8s-network-monitor.
"""

from prometheus_client import Gauge

internet_download_mbps = Gauge(
    "internet_download_mbps",
    "Current internet download bandwidth in Mbps"
)