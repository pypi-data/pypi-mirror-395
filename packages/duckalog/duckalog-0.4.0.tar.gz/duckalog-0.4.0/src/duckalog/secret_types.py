"""Secret type configurations for DuckDB."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class S3SecretConfig(BaseModel):
    """S3 secret configuration."""

    key_id: Optional[str] = None
    secret: str
    region: Optional[str] = None
    endpoint: Optional[str] = None


class AzureSecretConfig(BaseModel):
    """Azure secret configuration."""

    connection_string: Optional[str] = None
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: str
    account_name: Optional[str] = None


class GCSSecretConfig(BaseModel):
    """GCS secret configuration."""

    service_account_key: str
    json_key: Optional[str] = None


class HTTPSecretConfig(BaseModel):
    """HTTP secret configuration."""

    bearer_token: str
    header: Optional[str] = None


class PostgresSecretConfig(BaseModel):
    """PostgreSQL secret configuration."""

    connection_string: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: str


class MySQLSecretConfig(BaseModel):
    """MySQL secret configuration."""

    connection_string: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: str
