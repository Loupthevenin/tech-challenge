from pydantic import BaseModel, Field, constr
from typing import Literal
from datetime import datetime


class LogEntry(BaseModel):
    timestamp: datetime = Field(
        ...,
        description="Timestamp of the log entry in ISO 8601 format",
        json_schema_extra={"example": "2025-07-09T09:11:56Z"},
    )
    level: Literal["INFO", "WARNING", "ERROR", "DEBUG"] = Field(
        ...,
        description="Log level",
        json_schema_extra={"example": "INFO"},
    )
    message: constr(min_length=1) = Field(
        ...,
        description="Log message content",
        json_schema_extra={"example": "User login successful"},
    )
    service: constr(min_length=1) = Field(
        ...,
        description="Service name (ex: api-gateway, user-service)",
        json_schema_extra={"example": "api-gateway"},
    )


class LogEntryCreate(BaseModel):
    level: Literal["INFO", "WARNING", "ERROR", "DEBUG"] = Field(
        ...,
        description="Log level",
        json_schema_extra={"example": "INFO"},
    )
    message: constr(min_length=1) = Field(
        ...,
        description="Log message content",
        json_schema_extra={"example": "User login successful"},
    )
    service: constr(min_length=1) = Field(
        ...,
        description="Service name (ex: api-gateway, user-service)",
        json_schema_extra={"example": "api-gateway"},
    )


class LogEntryInDB(LogEntry):
    id: str = Field(
        ...,
        description="Unique identifier assigned by OpenSearch",
        json_schema_extra={"example": "abc123xyz456"},
    )
