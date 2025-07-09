from fastapi import FastAPI, Query
from typing import Optional, List, Dict, Any
from models import LogEntry
from opensearch_client import index_log, search_logs

app: FastAPI = FastAPI()


@app.post("/logs")
def ingest_log(log: LogEntry) -> Dict[str, Any]:
    result = index_log(log.dict())
    return {"id": result["_id"], **log.dict()}


@app.get("/logs/search")
def search(
    q: Optional[str] = Query(default=None),
    level: Optional[str] = Query(default=None),
    service: Optional[str] = Query(default=None),
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = search_logs(
        q=q, level=level, service=service)
    return [r["_source"] for r in results]
