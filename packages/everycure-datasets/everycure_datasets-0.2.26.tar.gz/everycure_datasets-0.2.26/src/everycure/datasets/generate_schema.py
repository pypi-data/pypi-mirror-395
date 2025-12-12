"""Generate JSON schema from Pydantic models."""

import json
from pathlib import Path

from everycure.datasets.models.v1 import DatasetMetadataV1
from everycure.datasets.models.v2 import DatasetMetadataV2


def generate_schema(model_class, output_path: Path, schema_id: str) -> None:
    """
    Generate JSON schema from a Pydantic model.

    Args:
        model_class: The Pydantic model class to generate schema from
        output_path: Path where the JSON schema should be written
        schema_id: The $id for the schema (FQDN)
    """
    # Get the JSON schema from the Pydantic model
    schema = model_class.model_json_schema(
        mode="serialization",
        by_alias=True,
    )

    # Update the $id to use the provided FQDN
    schema["$id"] = schema_id

    # Remove fields with defaults from required list
    # but keep them in properties so they're documented
    fields_with_defaults = ["schema_version", "status", "created_at"]
    if "required" in schema:
        for field in fields_with_defaults:
            if field in schema["required"]:
                schema["required"].remove(field)

    # Write to file with proper formatting
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)
        f.write("\n")  # Add trailing newline

    print(f"Generated JSON schema at {output_path}")


def generate_all_schemas(schema_dir: Path) -> None:
    """Generate all schema versions."""
    schema_dir.mkdir(parents=True, exist_ok=True)

    # Generate v1 schema
    v1_path = schema_dir / "dataset.v1.schema.json"
    generate_schema(
        DatasetMetadataV1,
        v1_path,
        "https://everycure.org/schemas/dataset.v1.schema.json",
    )

    # Generate v2 schema
    v2_path = schema_dir / "dataset.v2.schema.json"
    generate_schema(
        DatasetMetadataV2,
        v2_path,
        "https://everycure.org/schemas/dataset.v2.schema.json",
    )
