from models import LogEntry, LogEntryInDB
from opensearchpy import OpenSearch
from typing import List, Optional
from datetime import datetime, timezone
import os

client: OpenSearch = OpenSearch(
    hosts=[
        {
            "host": os.getenv("OPENSEARCH_HOST", "opensearch-node"),
            "port": int(os.getenv("OPENSEARCH_PORT", "9200")),
        }
    ],
    http_compress=True,
)


def index_log(log_data: LogEntry) -> dict:
    """
    Index a single log entry into OpenSearch.

    Args:
        log_data (LogEntry): The validated log data to be indexed.

    Returns:
        dict: The OpenSearch indexing response.
    """
    today: str = datetime.now(timezone.utc).strftime("%Y.%m.%d")
    index_name: str = f"logs-{today}"
    response: dict = client.index(index=index_name, body=log_data)
    return response


def search_logs(
    q: Optional[str] = None, level: Optional[str] = None, service: Optional[str] = None
) -> List[LogEntryInDB]:
    """
    Search log entries in OpenSearch based on optional filters.

    Args:
        q (Optional[str]): Full-text search on the message field.
        level (Optional[str]): Filter by log level (e.g., INFO, ERROR).
        service (Optional[str]): Filter by service name.

    Returns:
        List[LogEntryInDB]: A list of matching log entries.
    """
    today: str = datetime.now(timezone.utc).strftime("%Y.%m.%d")
    index_name: str = f"logs-{today}"

    must = []

    if q:
        must.append({"match": {"message": q}})
    if level:
        must.append({"term": {"level.keyword": level}})
    if service:
        must.append({"term": {"service.keyword": service}})

    if not must:
        query = {"match_all": {}}
    else:
        query = {"bool": {"must": must}}

    query_body = {
        "query": query,
        "sort": [{"timestamp": {"order": "desc"}}],
        "size": 20,
    }

    response = client.search(index=index_name, body=query_body)
    return [
        LogEntryInDB(**hit["_source"], id=hit["_id"])
        for hit in response["hits"]["hits"]
    ]
