import logging
from pathlib import Path
from typing import Any

import typer
import yaml
from kedro.io.core import AbstractDataset, DatasetError
from kedro_datasets import pandas, spark
from semantic_version import NpmSpec, Version

from everycure.datasets.kedro.storage import GitStorageService, is_uri
from everycure.datasets.models.v1 import (
    ColumnSchema,
    DatasetMetadataV1,
    DatasetSchema,
)

logger = logging.getLogger(__name__)

app = typer.Typer()


class DataCatalogDataset(AbstractDataset):
    """Custom dataset to load and read resources

    Examples:

        ```yaml
            catalog_diseases:
                type: everycure.datasets.kedro.catalog_dataset.DataCatalogDataset
                dataset: disease_list
                engine: spark

                load_args:
                    version: ~0.2.0

                # Arguments for the underlying Kedro engine (e.g., spark.SparkDataset)
                save_args:
                    mode: overwrite

                    # Arguments for the DatasetMetadataV1 model
                    catalog_args:
                        description: "Dataset description"
                        message: "Optional message"
                        owner:
                            name: "John Doe"
                            email: "john@example.com"
                        location:
                            uri: "gs://path/to/{version}/data.parquet"
                            format: "parquet"
                        # ...etc

        ```
    """

    def __init__(
        self,
        *,
        dataset: str | dict[str, Any],
        engine: str,
        save_args: dict[str, Any] = None,
        load_args: dict[str, Any] = None,
        **kwargs,
    ):
        self._dataset = dataset
        self._engine = engine
        self._storage_service = GitStorageService.get_instance()
        self._save_args = save_args or {}
        self._catalog_args = self._save_args.pop("catalog_args", None)
        self._load_args = load_args or {}

    @property
    def filepath(self) -> str:
        semver_pattern = self._load_args.get("version")
        version, _ = self.best_match(self.versions, semver_pattern)
        content = self._storage_service.get(
            Path(f"datasets/{self._dataset}/{version}/dataset.yaml")
        )
        if content is None:
            raise DatasetError(
                f"Dataset metadata file not found for '{self._dataset}' version '{version}'"
            )
        dataset = DatasetMetadataV1.model_validate(yaml.safe_load(content))

        return str(dataset.location.uri)

    def load(self) -> Any:
        """Dataset loading

        Dataset loads the best matching version of the requested
        dataset using the pattern.
        """
        # Make a copy to avoid modifying the original dict
        engine_load_args = self._load_args.copy()
        semver_pattern = engine_load_args.pop("version", None)
        assert_latest = engine_load_args.pop("assert_latest", False)

        version, is_latest = self.best_match(self.versions, semver_pattern)

        if version is None:
            raise DatasetError(
                f"No version matched for dataset '{self._dataset}', available versions: {','.join(self.versions)}"
            )

        if assert_latest and not is_latest:
            raise DatasetError(
                f"Newer version for dataset '{self._dataset}' available!"
            )

        logger.info(f"Using version {version} for dataset '{self._dataset}'")
        try:
            content = self._storage_service.get(
                Path(f"datasets/{self._dataset}/{version}/dataset.yaml")
            )
            if content is None:
                raise DatasetError(
                    f"Dataset metadata file not found for '{self._dataset}' version '{version}'"
                )
            dataset = DatasetMetadataV1.model_validate(yaml.safe_load(content))

            return self.get_dataset(
                dataset.location.format.value,
                str(dataset.location.uri),
                engine_load_args,
                {},  # save_args are not used in load
            ).load()
        except Exception as e:
            raise DatasetError(
                f"Failed to load version for dataset '{self._dataset}': {e}"
            ) from e

    @staticmethod
    def _uri_to_path(uri: str) -> str:
        """Convert file:// URLs to file paths for local file access.

        kedro_datasets expects file paths, not file:// URLs.
        Other URI schemes (http, https, gs, s3, etc.) are passed through unchanged.
        """
        if uri.startswith("file://"):
            from urllib.parse import unquote, urlparse

            parsed = urlparse(uri)
            return unquote(parsed.path)
        return uri

    def get_dataset(
        self,
        format_: str,
        file_path: str,
        load_args: dict[str, Any],
        save_args: dict[str, Any],
    ) -> AbstractDataset:
        # Convert file:// URLs to paths for local file access
        file_path = self._uri_to_path(file_path)

        if self._engine == "spark":
            if format_ == "tsv":
                return spark.SparkDataset(
                    filepath=file_path,
                    file_format="csv",
                    load_args={
                        **load_args,
                        "sep": "\t",
                        "header": True,
                        "index": False,
                    },
                    save_args=save_args,
                )

            return spark.SparkDataset(
                filepath=file_path,
                file_format=format_,
                load_args={**load_args, "header": True, "index": False},
                save_args=save_args,
            )

        if self._engine == "pandas":
            if format_ == "csv":
                return pandas.CSVDataset(
                    filepath=file_path,
                    load_args=load_args,
                    save_args=save_args,
                )

            if format_ == "parquet":
                return pandas.ParquetDataset(
                    filepath=file_path, load_args=load_args, save_args=save_args
                )

        raise ValueError(f"Unsupported engine: {self._engine} and format {format}")

    def get_schema(self, data) -> DatasetSchema:
        """Get dataset schema as DatasetSchema model."""
        columns = None
        row_count = None

        if self._engine == "pandas":
            type_map = {
                "int64": "int",
                "Int64": "int",
                "float64": "float",
                "object": "string",
                "bool": "bool",
                "datetime64[ns]": "datetime",
            }
            columns = [
                ColumnSchema(name=col, type=type_map.get(str(dtype), "unknown"))
                for col, dtype in data.dtypes.items()
            ]
            row_count = len(data)

        elif self._engine == "spark":
            spark_map = {
                "IntegerType()": "int",
                "LongType()": "int",
                "DoubleType()": "float",
                "FloatType()": "float",
                "StringType()": "string",
                "BooleanType()": "bool",
                "TimestampType()": "datetime",
                "DateType()": "date",
            }
            columns = [
                ColumnSchema(
                    name=field.name,
                    type=spark_map.get(str(field.dataType), "unknown"),
                )
                for field in data.schema.fields
            ]
            row_count = data.count()

        else:
            raise ValueError(f"Unsupported engine: {self._engine}")

        return DatasetSchema(columns=columns, row_count=row_count)

    def save(self, data: Any) -> None:
        """Dataset saving

        Dataset is saved using the next relevant semversion based
        on the catalog arguments.
        """
        if not self._catalog_args:
            raise DatasetError("Required 'catalog_args' missing in save_args.")

        # 1. Calculate dynamic properties from _catalog_args
        save_version = self._catalog_args.get("version")
        message = self._catalog_args.get("message")
        if not save_version:
            save_version = self.prompt_version_bump()
            if not save_version:  # User cancelled prompt
                logger.warning("Save cancelled by user.")
                return

        if not message:
            message = (
                typer.prompt("Optional message", default="", show_default=False) or None
            )

        # 2. Prepare the dictionary of dynamic/runtime arguments
        dynamic_args = {
            "name": self._dataset,
            "version": save_version,
            # is aliased in original, hence writing to schema, not dataset_schema
            "schema": self.get_schema(data).model_dump(exclude_none=True),
        }
        if message:
            dynamic_args["message"] = message

        metadata_dict = {**self._catalog_args, **dynamic_args}

        # 4. Post-merge processing: Handle the version placeholder in the URI
        location = metadata_dict.get("location", {})
        if "uri" in location:
            # Format the template string first, then convert to URI if needed
            formatted_filesystem_path_str = location["uri"].format(
                version=metadata_dict["version"]
            )
            if not is_uri(formatted_filesystem_path_str):
                path_obj = Path(formatted_filesystem_path_str)
                if not path_obj.is_absolute():
                    path_obj = path_obj.resolve()
                location["uri"] = path_obj.as_uri()
            else:
                location["uri"] = formatted_filesystem_path_str
        else:
            raise DatasetError("Required 'location.uri' missing in catalog_args.")

        # 5. Validate the final dictionary and create the Pydantic object
        try:
            dataset_metadata = DatasetMetadataV1.model_validate(metadata_dict)
        except Exception as e:  # Catches Pydantic's ValidationError
            raise DatasetError(f"Invalid dataset metadata configuration: {e}") from e

        # 6. Save the dataset file using the correct engine and self._save_args
        self.get_dataset(
            dataset_metadata.location.format.value,
            str(dataset_metadata.location.uri),
            {},  # load_args not used in save path
            self._save_args,  # Pass engine-specific save_args directly
        ).save(data)

        # 7. Save the metadata YAML file
        self._storage_service.save(
            f"datasets/{dataset_metadata.name}/{dataset_metadata.version}/dataset.yaml",
            yaml.dump(dataset_metadata.model_dump(mode="json", by_alias=True)),
            commit_msg=f"🤖 Create version {dataset_metadata.version} for '{dataset_metadata.name}'",
        )

    @staticmethod
    def best_match(versions: list[str], pattern: str) -> tuple[str | None, bool]:
        """Function to find the best semver match.

        Args:
            versions: List of available versions
            pattern: semver pattern to match
        Returns:
            Best match, and boolean indicating whether this is the last version.
        """
        if not pattern:
            spec = NpmSpec("*")
        else:
            spec = NpmSpec(pattern)
        parsed_versions = [Version(v) for v in versions]

        # Find versions that satisfy the pattern
        matching = [v for v in parsed_versions if v in spec]
        if not matching:
            return None, False

        best_version = max(matching)
        latest_version = max(parsed_versions)
        is_latest = best_version == latest_version

        return str(best_version), is_latest

    def prompt_version_bump(self) -> tuple[str, str | None]:
        """Prompt user for bumping information."""
        parsed = [Version(v) for v in self.versions]
        current_version = max([*parsed, Version("0.0.0")])
        typer.echo(f"Saving dataset: '{self._dataset}'")
        typer.echo(f"Current version: '{current_version}'")

        allowed = ["major", "minor", "patch"]
        bump_type = typer.prompt("Which part to bump? (major/minor/patch)").lower()
        while bump_type not in allowed:
            bump_type = typer.prompt(
                "Invalid choice. Please choose major, minor, or patch"
            ).lower()

        new_version = {
            "major": Version(major=current_version.major + 1, minor=0, patch=0),
            "minor": Version(
                major=current_version.major, minor=current_version.minor + 1, patch=0
            ),
            "patch": Version(
                major=current_version.major,
                minor=current_version.minor,
                patch=current_version.patch + 1,
            ),
        }[bump_type]

        if not typer.confirm(
            f"Do you want to save dataset '{self._dataset}' with version '{new_version}'?"
        ):
            typer.echo("Save cancelled.")
            return None, None

        return str(new_version)

    @property
    def versions(self) -> list[str]:
        """Function to get versions for dataset."""
        paths = self._storage_service.ls(f"datasets/{self._dataset}/*")
        return [
            str(path.relative_to(Path(f"datasets/{self._dataset}"))) for path in paths
        ]

    def _describe(self) -> dict[str, Any]:
        """Describe the dataset by returning its metadata."""
        return {
            "dataset": self._dataset,
            "engine": self._engine,
            "versions": self.versions,
        }
