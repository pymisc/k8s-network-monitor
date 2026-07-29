# k8s-network-monitor

> Cloud-native network monitoring solution deployed on Kubernetes with Prometheus metrics, Grafana dashboards, and automated health checks.

![Kubernetes](https://img.shields.io/badge/Kubernetes-native-blue)
![Prometheus](https://img.shields.io/badge/Metrics-Prometheus-orange)
![Grafana](https://img.shields.io/badge/Dashboard-Grafana-yellow)
![Helm](https://img.shields.io/badge/Deployment-Helm-0f1689)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://github.com/pymisc/k8s-network-monitor/actions/workflows/publish-image.yml/badge.svg)
![Security Scan](https://github.com/pymisc/k8s-network-monitor/actions/workflows/security.yml/badge.svg)
![Docker Image](https://img.shields.io/badge/Image-GHCR-blue)
![Helm Chart](https://img.shields.io/badge/Chart-Helm-0F1689)
![Security](https://img.shields.io/badge/Security-Trivy-success)
---

## Overview

**k8s-network-monitor** is a lightweight Kubernetes-native observability agent designed to monitor network connectivity, bandwidth, latency, and overall internet health.

The solution runs as a single container deployment inside Kubernetes and continuously collects network performance metrics that can be consumed by **Prometheus** and visualized through **Grafana dashboards**.

The initial implementation focuses on monitoring internet connection quality (such as ISP bandwidth and latency), while the architecture is designed to support additional network health probes in the future.

---

# Architecture

```text
                         Kubernetes Cluster

                              |
                              |
                    +---------------------+
                    | k8s-network-monitor |
                    |---------------------|
                    | Network Probe       |
                    | Metrics Exporter    |
                    | Health Checks       |
                    +----------+----------+
                               |
                               |
                         /metrics endpoint
                               |
                               |
                  +------------+-------------+
                  |                          |
             Prometheus                 Grafana Alloy
                  |                          |
                  +------------+-------------+
                               |
                               |
                         Grafana Dashboard
```

---

# Features

## Current Features

✅ Kubernetes-native deployment  
✅ Lightweight single-container architecture  
✅ Automated network health checks  
✅ Internet bandwidth monitoring  
✅ Prometheus-compatible metrics endpoint  
✅ Grafana dashboard visualization  
✅ Configurable monitoring interval  
✅ Helm-based deployment  

---

# Metrics

The application exposes Prometheus metrics including:

| Metric | Description |
|---|---|
| `internet_download_mbps` | Current download bandwidth |
| `internet_upload_mbps` | Current upload bandwidth |
| `internet_ping_ms` | Network latency |
| `internet_jitter_ms` | Latency variation |
| `internet_packet_loss_percent` | Packet loss percentage |
| `internet_last_success_timestamp` | Last successful health check |
| `internet_test_duration_seconds` | Monitoring test duration |

Example:

```text
# HELP internet_download_mbps Download bandwidth in Mbps
# TYPE internet_download_mbps gauge

internet_download_mbps 932.15


# HELP internet_ping_ms Network latency
# TYPE internet_ping_ms gauge

internet_ping_ms 12.4
```

---

# Grafana Dashboard

The project provides Grafana dashboards for:

## Bandwidth Monitoring

- Download speed trend
- Upload speed trend
- Bandwidth comparison

## Network Health

- Latency over time
- Jitter analysis
- Packet loss monitoring

## Availability

- Successful health checks
- Failed health checks
- Last successful measurement timestamp

Dashboard layout:

```text
+------------------------------------------------+
| Download Speed       | Upload Speed             |
+------------------------------------------------+
| Latency              | Packet Loss              |
+------------------------------------------------+
| Bandwidth History                               |
+------------------------------------------------+
| Network Availability                            |
+------------------------------------------------+
```

---

# Deployment

## Prerequisites

- Kubernetes cluster
- Helm 3.x
- Prometheus or Grafana Cloud Metrics
- Grafana Dashboard

---

## Install Using Helm

```bash
helm install network-monitor \
  ./helm/k8s-network-monitor \
  --namespace monitoring \
  --create-namespace
```

---

## Verify Deployment

```bash
kubectl get pods -n monitoring
```

Expected:

```text
NAME                                  READY   STATUS
k8s-network-monitor                   1/1     Running
```

---

# Configuration

Configuration is controlled through Helm values.

Example:

```yaml
monitor:
  intervalSeconds: 600

metrics:
  port: 8080

logging:
  level: INFO
```

Default monitoring interval:

```text
10 minutes
```

---

# Prometheus Integration

The application exposes:

```text
http://<pod-ip>:8080/metrics
```

Example scrape configuration:

```yaml
scrape_configs:

- job_name: network-monitor

  static_configs:
    - targets:
      - network-monitor:8080
```

For Kubernetes environments, a `ServiceMonitor` resource can be used with Prometheus Operator.

---

# Grafana Alerts

Example alert rules:

## Low Download Bandwidth

```text
internet_download_mbps < 500
```

---

## High Latency

```text
internet_ping_ms > 50
```

---

## Packet Loss

```text
internet_packet_loss_percent > 2
```

---

## Monitoring Failure

```text
time() - internet_last_success_timestamp > 1800
```

---

# Technology Stack

| Component | Technology |
|-|-|
| Runtime | Python |
| Container | Docker |
| Orchestration | Kubernetes |
| Deployment | Helm |
| Metrics | Prometheus |
| Visualization | Grafana |
| Observability | Grafana Alloy / Prometheus |
| CI/CD | GitHub Actions |

---

# Project Structure

```text
k8s-network-monitor/

├── app/
│   └── monitor.py
│
├── Dockerfile
├── requirements.txt
│
├── helm/
│   └── k8s-network-monitor/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── dashboards/
│   └── network-monitor-dashboard.json
│
├── docs/
│
├── tests/
│
├── README.md
└── LICENSE
```

---

# Roadmap

## Phase 1 - Core Monitoring

- [x] Project initialization
- [ ] Internet bandwidth measurement
- [ ] Prometheus metrics exporter
- [ ] Grafana dashboard
- [ ] Helm deployment

---

## Phase 2 - Network Observability

Planned probes:

- DNS latency monitoring
- HTTP endpoint availability
- ICMP latency checks
- Packet loss monitoring
- Public IP change detection
- SSL certificate monitoring

---

## Phase 3 - Enterprise Features

Future ideas:

- Multi-target monitoring
- Alert integrations
- Slack / Email notifications
- Historical reports
- Multi-architecture container images
- Kubernetes Operator support

---

# Security Considerations

The container follows Kubernetes security best practices:

- Runs as non-root user
- Minimal container image
- Read-only filesystem where possible
- No unnecessary Kubernetes permissions
- Resource limits configured
- Vulnerability scanning in CI/CD

---

# Contributing

Contributions are welcome.

Please open an issue to discuss:

- New monitoring probes
- Dashboard improvements
- Performance enhancements
- Feature requests

---

# License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.

---

# Author

Built as a Kubernetes observability learning project demonstrating:

- Kubernetes deployments
- Prometheus metrics
- Grafana dashboards
- Cloud-native monitoring patterns
- Platform engineering practices
