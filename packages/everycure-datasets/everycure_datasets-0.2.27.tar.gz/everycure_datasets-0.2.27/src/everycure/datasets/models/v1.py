"""Dataset Metadata v1 - Initial version matching the JSON schema."""

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import AnyUrl, BaseModel, Field, HttpUrl, field_validator


class StorageType(str, Enum):
    """Storage type for dataset location."""

    GCS = "gcs"
    S3 = "s3"
    LOCAL = "local"
    BIGQUERY = "bigquery"
    POSTGRES = "postgres"


class FileFormat(str, Enum):
    """File format for dataset."""

    TSV = "tsv"
    CSV = "csv"
    PARQUET = "parquet"
    JSON = "json"
    JSONL = "jsonl"
    AVRO = "avro"
    ORC = "orc"


class DatasetStatus(str, Enum):
    """Dataset status."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class Location(BaseModel):
    """Dataset location information."""

    type: StorageType = Field(..., description="Storage type")
    uri: AnyUrl = Field(..., description="Full URI to the dataset")
    format: FileFormat = Field(..., description="File format")

    model_config = {"extra": "forbid"}


class Owner(BaseModel):
    """Dataset owner information."""

    name: str = Field(..., min_length=1, description="Owner name")
    email: Optional[str] = Field(None, description="Owner email address")

    model_config = {"extra": "forbid"}


class Origin(BaseModel):
    """Dataset origin information."""

    system: str = Field(..., description="Pipeline or system name")
    url: HttpUrl = Field(..., description="GitHub URL to source code")
    commit: Optional[str] = Field(
        None,
        pattern=r"^[a-f0-9]{7,40}$",
        description="Git commit hash (7-40 hex characters)",
    )
    tag: Optional[str] = Field(None, description="Git tag")

    model_config = {"extra": "forbid"}


class ColumnSchema(BaseModel):
    """Schema definition for a single column."""

    name: str = Field(..., description="Column name")
    type: str = Field(..., description="Column data type")
    description: Optional[str] = Field(None, description="Column description")

    model_config = {"extra": "forbid"}


class DatasetSchema(BaseModel):
    """Dataset schema information."""

    row_count: Optional[int] = Field(None, ge=0, description="Number of rows")
    columns: Optional[list[ColumnSchema]] = Field(
        None, description="List of column definitions"
    )

    model_config = {"extra": "forbid"}


class DatasetMetadataV1(BaseModel):
    """
    Dataset Metadata v1.

    This model represents the metadata for a dataset in the registry.
    It matches the structure defined in dataset.schema.json.
    """

    # Schema version - tracks the version of this metadata definition itself
    schema_version: str = Field(
        default="1.0.0",
        description="Version of the dataset metadata schema definition",
    )
    name: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Dataset name in snake_case",
    )
    version: str = Field(
        ...,
        pattern=r"^\d+\.\d+\.\d+$",
        description="Semantic version (e.g., 0.2.0)",
    )
    description: Optional[str] = Field(
        None, min_length=10, description="Brief description of the dataset"
    )
    message: Optional[str] = Field(
        None, description="Optional message about this dataset version"
    )
    location: Location = Field(..., description="Dataset location")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="ISO 8601 timestamp",
    )
    owner: Owner = Field(..., description="Dataset owner")
    origin: Origin = Field(..., description="Dataset origin")
    status: DatasetStatus = Field(
        default=DatasetStatus.ACTIVE, description="Dataset status"
    )
    lineage: Optional[dict[str, Any]] = Field(
        default=None, description="Placeholder for future lineage tracking"
    )
    # Use model_field to avoid shadowing BaseModel.schema
    dataset_schema: Optional[DatasetSchema] = Field(
        default=None,
        alias="schema",
        description="Dataset schema information",
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Additional metadata dictionary"
    )
    tags: Optional[list[str]] = Field(
        default=None,
        description="Tags for discoverability (lowercase with hyphens)",
    )
    related_docs: Optional[HttpUrl] = Field(
        default=None, description="Link to documentation"
    )
    deprecated_by: Optional[str] = Field(
        default=None, description="Version that replaces this dataset"
    )
    deprecation_date: Optional[datetime] = Field(
        default=None, description="Date when dataset was deprecated"
    )

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate description length if provided."""
        if v is not None and len(v) < 10:
            raise ValueError("Description must be at least 10 characters long")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Validate tag format."""
        if v is None:
            return v
        for tag in v:
            if not tag or not tag.replace("-", "").replace("_", "").isalnum():
                raise ValueError(
                    f"Tag '{tag}' must contain only lowercase alphanumeric characters and hyphens"
                )
            if tag != tag.lower():
                raise ValueError(f"Tag '{tag}' must be lowercase")
        # Ensure unique tags
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")
        return v

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/2020-12/schema#",
            "$id": "https://everycure.org/schemas/dataset.v1.schema.json",
            "title": "Dataset Metadata v1",
            "description": "Schema for dataset registry metadata files (v1)",
        },
    }
