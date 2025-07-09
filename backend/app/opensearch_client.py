from opensearchpy import OpenSearch
from typing import List, Dict, Any
from datetime import datetime
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


def index_log(log_data: Dict[str, Any]) -> Dict[str, Any]:
    today: str = datetime.utcnow().strftime("%Y.%m.%d")
    index_name: str = f"logs-{today}"
    response: Dict[str, Any] = client.index(index=index_name, body=log_data)
    return response


def search_logs(
    q: str = None, level: str = None, service: str = None
) -> List[Dict[str, Any]]:
    today: str = datetime.utcnow().strftime("%Y.%m.%d")
    index_name: str = f"logs-{today}"

    must_clauses: List[Dict[str, Any]] = []

    if q:
        must_clauses.append({"match": {"message": q}})
    if level:
        must_clauses.append({"term": {"level": level}})
    if service:
        must_clauses.append({"term": {"service": service}})

    if not must_clauses:
        must_clauses = [{"match_all": {}}]

    query_body: Dict[str, Any] = {
        "query": {
            "bool": {"must": must_clauses}
            if must_clauses
            else {"must": [{"match_all": []}]}
        },
        "sort": [{"timestamp": {"order": "desc"}}],
    }

    response: Dict[str, Any] = client.search(index=index_name, body=query_body)
    return response["hits"]["hits"]
