"""
Ping measurement utilities.

This module measures network round-trip latency
using the operating system ping command.

The target is controlled by the PING_TARGET
environment variable.

Default:
    1.1.1.1
"""

import os
import platform
import re
import subprocess


PING_TARGET = os.getenv("PING_TARGET", "1.1.1.1")


def get_ping_latency():
    """
    Measure round-trip latency to the configured ping target.

    Returns:
        float:
            Average ping latency in milliseconds.

    Raises:
        RuntimeError:
            If the ping command fails or latency cannot be parsed.
    """

    system = platform.system().lower()

    if system == "windows":
        command = [
            "ping",
            "-n",
            "1",
            PING_TARGET,
        ]
    else:
        command = [
            "ping",
            "-c",
            "1",
            PING_TARGET,
        ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Ping failed for target {PING_TARGET}"
        )

    output = result.stdout

    match = re.search(
        r"time[=<]([\d.]+)\s*ms",
        output,
        re.IGNORECASE,
    )

    if not match:
        raise RuntimeError(
            f"Unable to parse ping latency for target {PING_TARGET}"
        )

    return round(float(match.group(1)), 2)