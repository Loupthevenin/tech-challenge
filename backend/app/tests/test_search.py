import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from models import LogEntry


def test_search_logs(client):
    response = client.get("/logs/search")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


@patch("main.search_logs")
def test_search_with_level_filter(mock_search_logs, client):
    mock_search_logs.return_value = [
        LogEntry(
            level="ERROR",
            message="Erreur critique",
            service="core",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    ]

    response = client.get("/logs/search?level=ERROR")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["level"] == "ERROR"

    mock_search_logs.assert_called_once_with(
        q=None,
        level="ERROR",
        service=None,
        page=1,
        size=20,
        start_date=None,
        end_date=None,
    )


@patch("main.search_logs")
def test_search_with_pagination(mock_search_logs, client):
    mock_search_logs.return_value = []

    response = client.get("/logs/search?page=2&size=10")
    assert response.status_code == 200
    assert response.json() == []

    mock_search_logs.assert_called_once_with(
        q=None,
        level=None,
        service=None,
        page=2,
        size=10,
        start_date=None,
        end_date=None,
    )


@patch("main.search_logs")
def test_search_with_date_range(mock_search_logs, client):
    start = datetime(2024, 1, 1, tzinfo=timezone.utc).isoformat()
    end = datetime(2024, 1, 31, tzinfo=timezone.utc).isoformat()

    mock_search_logs.return_value = []

    response = client.get(
        "/logs/search",
        params={
            "start_date": start,
            "end_date": end,
        },
    )
    assert response.status_code == 200

    mock_search_logs.assert_called_once()
    kwargs = mock_search_logs.call_args.kwargs
    assert kwargs["start_date"].isoformat() == start
    assert kwargs["end_date"].isoformat() == end


@patch("main.search_logs")
def test_search_with_service(mock_search_logs, client):
    mock_search_logs.return_value = [
        LogEntry(
            level="INFO",
            message="Log du service A",
            service="service-A",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    ]

    response = client.get("/logs/search?service=service-A")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["service"] == "service-A"

    mock_search_logs.assert_called_once_with(
        q=None,
        level=None,
        service="service-A",
        page=1,
        size=20,
        start_date=None,
        end_date=None,
    )


def test_search_invalid_page(client):
    response = client.get("/logs/search?page=0")
    assert response.status_code == 422


def test_search_invalid_size(client):
    response = client.get("/logs/search?size=101")
    assert response.status_code == 422


def test_search_size_too_small(client):
    response = client.get("/logs/search?size=0")
    assert response.status_code == 422


def test_search_invalid_start_date_format(client):
    response = client.get("/logs/search?start_date=not-a-date")
    assert response.status_code == 422


def test_search_invalid_end_date_format(client):
    response = client.get("/logs/search?end_date=31-01-2024")
    assert response.status_code == 422
