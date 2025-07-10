from models import LogEntry, LogEntryInDB
from opensearchpy import OpenSearch
from typing import List, Optional
from datetime import datetime, timezone
from opensearchpy.exceptions import NotFoundError
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
    q: Optional[str] = None,
    level: Optional[str] = None,
    service: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
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
    from_ = (page - 1) * size
    today: str = datetime.now(timezone.utc).strftime("%Y.%m.%d")
    index_name: str = f"logs-{today}"

    must = []

    if q:
        must.append({"match": {"message": q}})
    if level:
        must.append({"term": {"level.keyword": level}})
    if service:
        must.append({"term": {"service.keyword": service}})

    if start_date or end_date:
        date_range = {}
        if start_date:
            date_range["gte"] = start_date.isoformat()
        if end_date:
            date_range["lte"] = end_date.isoformat()
        must.append({"range": {"timestamp": date_range}})

    if not must:
        query = {"match_all": {}}
    else:
        query = {"bool": {"must": must}}

    query_body = {
        "query": query,
        "sort": [{"timestamp": {"order": "desc"}}],
        "from": from_,
        "size": size,
    }

    try:
        response = client.search(index=index_name, body=query_body)
        return [
            LogEntryInDB(**hit["_source"], id=hit["_id"])
            for hit in response["hits"]["hits"]
        ]
    except NotFoundError:
        # L'index du jour n'existe pas (aucun log écrit)
        return []
