"""
Background scheduler for k8s-network-monitor.

This module periodically performs network measurements and updates
Prometheus metrics.

The monitoring interval is controlled through the
MONITOR_INTERVAL_SECONDS environment variable.

Default:
    600 seconds (10 minutes)
"""

import os
import threading
import time

from .bandwidth import get_download_speed
from .ping import get_ping_latency
from .metrics import (
    internet_download_mbps,
    internet_ping_latency_ms,
)

# Default to running every 10 minutes.
MONITOR_INTERVAL_SECONDS = int(
    os.getenv(
        "MONITOR_INTERVAL_SECONDS", 
        "600"
    )
)


def collect_metrics():
    """
    Perform one monitoring cycle.

    Retrieves the current internet download bandwidth and updates the
    corresponding Prometheus metric.
    """

    try:
        download_speed = get_download_speed()
        internet_download_mbps.set(download_speed)
    except Exception as exc:
        print(f"Failed to collect download speed: {exc}")

    try:
        ping_latency = get_ping_latency()
        internet_ping_latency_ms.set(ping_latency)
    except Exception as exc:
        print(f"Failed to collect ping latency: {exc}")


def scheduler_loop():
    """
    Main scheduler loop.

    Runs indefinitely until the application exits.
    """

    while True:
        try:
            collect_metrics()
        except Exception as exc:
            print(f"Metric collection failed: {exc}")

        time.sleep(MONITOR_INTERVAL_SECONDS)


def start_scheduler():
    """
    Start the background scheduler thread.

    The thread is marked as daemon=True so it exits automatically when
    the Flask application stops.
    """
    print(
        f"Starting network monitor scheduler "
        f"(interval={MONITOR_INTERVAL_SECONDS}s)"
    )

    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True,
        name="network-monitor-scheduler",
    )

    thread.start()

    return thread