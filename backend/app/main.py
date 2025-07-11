from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models import LogEntry, LogEntryCreate, LogEntryInDB
from datetime import datetime, timezone
from opensearch_client import get_logs_stats, index_log, search_logs

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # En prod on doit remplacer par VITE_API_BASE_URL
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/logs")
async def websocket_logs_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/logs", response_model=LogEntryInDB)
async def ingest_log(log: LogEntryCreate) -> LogEntryInDB:
    """
    Ingest a new log entry and index it into OpenSearch.

    Args:
        log (LogEntryCreate): The log data submitted in the request body.

    Returns:
        LogEntryInDB: The indexed log entry, including the generated ID.
    """
    log_data: LogEntry = LogEntry(
        **log.model_dump(), timestamp=datetime.now(timezone.utc)
    )
    result = index_log(log_data=log_data.model_dump())
    await manager.broadcast(jsonable_encoder(log_data.model_dump()))
    return LogEntryInDB(id=result["_id"], **log_data.model_dump())


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
        page (int): Page number for pagination (default: 1).
        size (int): Number of results per page (default: 20, max: 100).
        start_date (Optional[datetime]): Filter logs starting from this date.
        end_date (Optional[datetime]): Filter logs up to this date.

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


@app.get("/logs/stats")
def stats() -> dict:
    """
    Retrieve aggregated statistics of log levels for today's logs.

    Returns:
        dict: A dictionary mapping log levels (e.g., INFO, ERROR) to their counts.
    """
    results = get_logs_stats()
    return results
