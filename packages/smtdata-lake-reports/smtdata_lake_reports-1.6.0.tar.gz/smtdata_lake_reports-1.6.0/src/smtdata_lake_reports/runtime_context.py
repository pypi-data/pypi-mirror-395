from __future__ import annotations
from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Simple S3 URL check (bucket + key)
S3Url = Annotated[str, Field(pattern=r"^s3://[^/]+/.+")]

class InboxSettings(BaseModel):
    queue_url: str = Field("", description="The URL of the Inbox Queue to which status messages should be sent.")

class ReportSettings(BaseModel):
    spec_id: str = Field(..., description="ID of the report specification being executed")
    exec_id: str = Field(..., description="ID of the current execution")

class AthenaSettings(BaseModel):
    workgroup_name: str = Field(..., description="Athena workgroup to use")
    database_name: Optional[str] = Field(
        ...,
        description="Athena database. "
    )
    userspace_database_name: str = Field(..., description="Athena userspace database name")
    s3_output: S3Url = Field(..., description="s3://... location for Athena query results")
    log_sql_statements: bool = Field(False, description="Enable capturing of Athena SQL queries before executing")

    @field_validator("s3_output")
    @classmethod
    def _s3_output_must_be_s3(cls, v: str) -> str:
        # The regex already checks s3://, but keep the message explicit.
        if not v.startswith("s3://"):
            raise ValueError("ATHENA.s3_output must start with s3://")
        return v

class ContextSettings(BaseSettings):
    # Nested blocks map to your __ sections
    report: ReportSettings
    athena: AthenaSettings
    inbox: InboxSettings = InboxSettings()

    tenant_id: str = Field(..., description="Tenant identifier")
    aws_region: str = Field(..., description="The AWS region currently executing in")

    s3_bucket_name: str = Field(
        ...,
        description="Primary bucket used by the report"
    )

    # Global settings config: prefix + nested delimiter
    model_config = SettingsConfigDict(
        env_prefix="LAKE_REPORTS__CONTEXT__",
        env_nested_delimiter="__",
        extra="ignore",
        env_file=".env",  # optional
    )

    @model_validator(mode="after")
    def _default_athena_db_from_tenant(self) -> "ContextSettings":
        # If database_name is missing, derive from tenant_id: itbi<tenant_id>_raw
        if not self.athena.database_name:
            object.__setattr__(
                self.athena, "database_name", f"itbi{self.tenant_id}_raw"
            )
        return self

# Convenience accessor you can import elsewhere
def get_context() -> ContextSettings:
    # Reads from env (and .env if configured), applies validation & defaults
    return ContextSettings()