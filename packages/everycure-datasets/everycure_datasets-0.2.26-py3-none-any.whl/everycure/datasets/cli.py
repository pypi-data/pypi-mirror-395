"""CLI for datasets registry operations."""

from pathlib import Path

import typer

from everycure.datasets.generate_schema import generate_all_schemas
from everycure.datasets.validate import validate_datasets

app = typer.Typer(
    name="datasets",
    help="Datasets registry management CLI",
    add_completion=False,
    no_args_is_help=True,
)

schema_app = typer.Typer(
    name="schema",
    help="Schema management commands",
    add_completion=False,
)

app.add_typer(schema_app)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Datasets registry management CLI."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


@app.command()
def validate(
    datasets_dir: Path | None = typer.Option(
        None,
        "--datasets-dir",
        "-d",
        help="Path to the datasets directory (default: auto-detect)",
    ),
) -> None:
    """
    Validate dataset YAML files and directory structure.

    Checks:
    - Dataset names are snake_case
    - Version directories follow semantic versioning (MAJOR.MINOR.PATCH)
    """
    return validate_datasets(datasets_dir)


@schema_app.command()
def generate() -> None:
    """
    Generate JSON schema(s) from the Pydantic models.
    """
    repo_root = Path.cwd()
    schema_dir = repo_root / ".schema"
    generate_all_schemas(schema_dir)
    typer.echo(f"✓ Generated all JSON schemas in {schema_dir}")


if __name__ == "__main__":
    app()
