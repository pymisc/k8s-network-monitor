"""
Unit tests for the Flask application.

These tests verify that the application's basic endpoints are functioning
correctly. The tests use Flask's built-in test client, which allows requests
to be made without starting a real web server.
"""

from pathlib import Path
import sys

import pytest

# ---------------------------------------------------------------------------
# Allow importing the application when running pytest from the repository root.
# This adds the project's root directory to Python's module search path.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.app import app as flask_app


# ---------------------------------------------------------------------------
# Pytest Fixture
#
# This fixture creates a reusable Flask test client. Any test that accepts
# "client" as an argument will automatically receive this object.
#
# Benefits:
#   - Avoids repeating flask_app.test_client() in every test.
#   - Makes future tests cleaner and easier to maintain.
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    flask_app.testing = True

    with flask_app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Test: Root Endpoint
#
# Verify that the root endpoint (/) responds successfully and returns the
# expected application status message.
# ---------------------------------------------------------------------------
def test_root_returns_running_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "k8s-network-monitor is running!"


# ---------------------------------------------------------------------------
# Test: Health Endpoint
#
# Verify that the health endpoint returns HTTP 200 along with the expected
# JSON response. This endpoint is commonly used by Kubernetes liveness and
# readiness probes.
# ---------------------------------------------------------------------------
def test_health_returns_ok_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}