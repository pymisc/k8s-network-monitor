"""
Network bandwidth measurement utilities.

This module is responsible for collecting
internet speed measurements.

Current implementation:
- Uses speedtest-cli
- Returns download bandwidth in Mbps

Future:
- Upload speed
- Latency
- Jitter
- Packet loss
"""


import speedtest


def get_download_speed():
    """
    Measure current internet download speed.

    Returns:
        float:
            Download bandwidth in Mbps.
    """

    test = speedtest.Speedtest()

    test.get_best_server()

    test.download()

    download_bps = test.results.download

    # Convert bits per second to megabits per second
    download_mbps = download_bps / 1_000_000

    return round(download_mbps, 2)