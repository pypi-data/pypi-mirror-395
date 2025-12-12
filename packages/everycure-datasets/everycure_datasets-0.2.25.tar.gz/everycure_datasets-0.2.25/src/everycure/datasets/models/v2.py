"""Dataset Metadata v2 - Refined version (placeholder for future improvements)."""

from everycure.datasets.models.v1 import DatasetMetadataV1


class DatasetMetadataV2(DatasetMetadataV1):
    """
    Dataset Metadata v2.

    This is a placeholder for a future refined version of the dataset metadata model.
    When v2 is implemented, it will include improvements and refinements over v1.

    For now, this class inherits from v1 to maintain compatibility.
    """

    # TODO: Add v2-specific fields and improvements here
    # Examples of potential improvements:
    # - Better validation
    # - Additional metadata fields
    # - Improved lineage tracking
    # - Enhanced schema definitions

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/2020-12/schema#",
            "$id": "https://everycure.org/schemas/dataset.v2.schema.json",
            "title": "Dataset Metadata v2",
            "description": "Schema for dataset registry metadata files (v2)",
        },
    }
