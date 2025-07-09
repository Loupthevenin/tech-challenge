from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from models import LogEntry, LogEntryInDB
from opensearch_client import index_log, search_logs

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # En prod on doit remplacer par VITE_API_BASE_URL
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/logs", response_model=LogEntryInDB)
def ingest_log(log: LogEntry) -> LogEntryInDB:
    """
    Ingest a new log entry and index it into OpenSearch.

    Args:
        log (LogEntry): The log data submitted in the request body.

    Returns:
        LogEntryInDB: The indexed log entry, including the generated ID.
    """
    result = index_log(log.dict())
    return LogEntryInDB(id=result["_id"], **log.model_dump())


@app.get("/logs/search", response_model=List[LogEntry])
def search(
    q: Optional[str] = Query(default=None),
    level: Optional[str] = Query(default=None),
    service: Optional[str] = Query(default=None),
) -> List[LogEntry]:
    """
    Search logs in OpenSearch using optional filters.

    Args:
        q (Optional[str]): Full-text search on the message field.
        level (Optional[str]): Filter by log level (INFO, ERROR, etc.).
        service (Optional[str]): Filter by service name.

    Returns:
        List[LogEntry]: List of matching logs without OpenSearch metadata.
    """
    results: List[LogEntryInDB] = search_logs(q=q, level=level, service=service)
    return [LogEntry(**r.model_dump(exclude={"id"})) for r in results]
