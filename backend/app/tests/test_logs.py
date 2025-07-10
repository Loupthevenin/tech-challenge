import pytest
from unittest.mock import patch


@patch("main.index_log", return_value={"_id": "fake-id-123"})
def test_create_log(mock_index_log, client):
    payload = {
        "level": "WARNING",
        "message": "Log test",
        "service": "test-service",
    }

    response = client.post("/logs", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["level"] == "WARNING"
    assert data["message"] == "Log test"
    assert data["service"] == "test-service"
    assert "timestamp" in data

    mock_index_log.assert_called_once()


def test_missing_level(client):
    payload = {
        "message": "Log sans level",
        "service": "test-service",
    }

    response = client.post("/logs", json=payload)
    assert response.status_code == 422


def test_invalid_level(client):
    payload = {
        "level": "SUPERCRITICAL",
        "message": "Niveau invalide",
        "service": "test-service",
    }

    response = client.post("/logs", json=payload)
    assert response.status_code == 422


def test_empty_message(client):
    payload = {
        "level": "INFO",
        "message": "",
        "service": "",
    }

    response = client.post("/logs", json=payload)
    assert response.status_code == 422


@patch("main.index_log", return_value={"_id": "fake-id-123"})
def test_long_service_name(mock_index_log, client):
    payload = {
        "level": "ERROR",
        "message": "Service long test",
        "service": "a" * 300,
    }

    response = client.post("/logs", json=payload)
    assert response.status_code == 200

    mock_index_log.assert_called_once()


@patch("main.index_log", return_value={"_id": "fake-id-123"})
def test_timestamp_is_auto_generated(mock_index_log, client):
    payload = {
        "level": "INFO",
        "message": "Auto-timestamp test",
        "service": "test-service",
    }

    response = client.post("/logs", json=payload)
    data = response.json()
    assert "timestamp" in data

    from datetime import datetime

    datetime.fromisoformat(data["timestamp"])

    mock_index_log.assert_called_once()
