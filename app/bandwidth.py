"""
Network measurement utilities.

This module is responsible for collecting
internet performance measurements.

Current implementation:
- Download bandwidth
- Ping latency

Future:
- Upload speed
- Jitter
- Packet loss
"""


import speedtest


def get_network_metrics():
    """
    Measure current internet download speed and ping latency.

    Returns:
        tuple:
            download_mbps (float)
            ping_latency_ms (float)
    """


    test = speedtest.Speedtest()

    test.get_best_server()

    ping_latency_ms = test.results.ping

    test.download()

    download_bps = test.results.download
    # Convert bits per second to megabits per second
    download_mbps = download_bps / 1_000_000

    return (
        round(download_mbps, 2), 
        round(ping_latency_ms, 2),
    )