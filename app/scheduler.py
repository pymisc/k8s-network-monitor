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
from .metrics import internet_download_mbps


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

    download_speed = get_download_speed()

    internet_download_mbps.set(download_speed)


def scheduler_loop():
    """
    Main scheduler loop.

    Runs indefinitely until the application exits.
    """

    while True:

        collect_metrics()

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