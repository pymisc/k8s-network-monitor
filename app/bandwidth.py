"""
Bandwidth measurement utilities.

This module is responsible for collecting
internet bandwidth measurements.

The Speedtest execution timeout is controlled through the
SPEEDTEST_TIMEOUT_SECONDS environment variable.

Default:
    60 seconds

Current implementation:
- Download bandwidth

Future:
- Upload bandwidth
"""

import json
import os
import subprocess


SPEEDTEST_TIMEOUT_SECONDS = int(
    os.getenv("SPEEDTEST_TIMEOUT_SECONDS", "60")
)


def get_download_speed():
    """
    Measure current internet download speed.

    Returns:
        float:
            Download bandwidth in Mbps.

    Raises:
        RuntimeError:
            If speedtest-cli fails or returns invalid output.
        subprocess.TimeoutExpired:
            If the speed test exceeds the configured timeout.
    """

    result = subprocess.run(
        ["speedtest-cli", "--json"],
        capture_output=True,
        text=True,
        timeout=SPEEDTEST_TIMEOUT_SECONDS,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Speedtest failed: {result.stderr.strip()}"
        )

    try:
        data = json.loads(result.stdout)
        download_bps = data["download"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise RuntimeError(
            "Unable to parse speedtest-cli output"
        ) from exc

    # Convert bits per second to megabits per second.
    download_mbps = download_bps / 1_000_000

    return round(download_mbps, 2)