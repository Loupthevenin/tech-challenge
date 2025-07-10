from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from models import LogEntry, LogEntryCreate, LogEntryInDB
from datetime import datetime, timezone
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
def ingest_log(log: LogEntryCreate) -> LogEntryInDB:
    """
    Ingest a new log entry and index it into OpenSearch.

    Args:
        log (LogEntryCreate): The log data submitted in the request body.

    Returns:
        LogEntryInDB: The indexed log entry, including the generated ID.
    """
    log_data: LogEntry = LogEntry(**log.dict(), timestamp=datetime.now(timezone.utc))
    result = index_log(log_data=log_data.dict())
    return LogEntryInDB(id=result["_id"], **log_data.dict())


@app.get("/logs/search", response_model=List[LogEntry])
def search(
    q: Optional[str] = Query(default=None),
    level: Optional[str] = Query(default=None),
    service: Optional[str] = Query(default=None),
    page: int = Query(
        1,
        ge=1,
    ),
    size: int = Query(20, ge=1, le=100),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
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
    results: List[LogEntryInDB] = search_logs(
        q=q,
        level=level,
        service=service,
        page=page,
        size=size,
        start_date=start_date,
        end_date=end_date,
    )
    return [LogEntry(**r.model_dump(exclude={"id"})) for r in results]
