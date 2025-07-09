from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class LogEntry(BaseModel):
    timestamp: datetime
    level: Literal["INFO", "WARNING", "ERROR", "DEBUG"]
    message: str
    service: str
