# Copyright (c) 2025 Tylt LLC. All rights reserved.
# Derivative works may be released by researchers,
# but original files may not be redistributed or used beyond research purposes.

"""Main CLI entrypoint for CUDAG."""

from __future__ import annotations

from pathlib import Path

import click

from cudag import __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """CUDAG - ComputerUseDataAugmentedGeneration framework.

    Create generator projects with 'cudag new', then generate datasets
    with 'cudag generate'.
    """
    pass


@cli.command()
@click.argument("name")
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default=".",
    help="Directory to create the project in (default: current directory)",
)
def new(name: str, output_dir: str) -> None:
    """Create a new CUDAG project.

    NAME is the project name (e.g., 'appointment-picker').
    """
    from cudag.cli.new import create_project

    project_dir = create_project(name, Path(output_dir))
    click.echo(f"Created project: {project_dir}")
    click.echo("\nNext steps:")
    click.echo(f"  cd {project_dir}")
    click.echo("  # Edit screen.py, state.py, renderer.py, and tasks/")
    click.echo("  cudag generate --config config/dataset.yaml")


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to dataset config YAML",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    help="Override output directory",
)
def generate(config: str, output_dir: str | None) -> None:
    """Generate a dataset from the current project.

    Requires a dataset config file (YAML) and the project's screen/task definitions.
    """
    config_path = Path(config)
    click.echo(f"Loading config: {config_path}")

    # TODO: Implement full generation by loading project modules
    # For now, show what would be done
    click.echo("Generation not yet implemented - use project's generate.py directly")


@cli.command()
@click.argument("dataset_dir", type=click.Path(exists=True))
def upload(dataset_dir: str) -> None:
    """Upload a dataset to Modal volume.

    DATASET_DIR is the path to the generated dataset directory.
    """
    click.echo(f"Uploading: {dataset_dir}")
    click.echo("Upload not yet implemented")


@cli.command()
@click.argument("dataset_dir", type=click.Path(exists=True))
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show all errors (default: first 10)",
)
def validate(dataset_dir: str, verbose: bool) -> None:
    """Validate a dataset against the CUDAG schema.

    DATASET_DIR is the path to the generated dataset directory.

    Checks:
    - Required filesystem structure (images/, test/, etc.)
    - Training record schema (data.jsonl, train.jsonl, val.jsonl)
    - Test record schema (test/test.json)
    - Image path validity (all referenced images exist)

    Exit codes:
    - 0: Dataset is valid
    - 1: Validation errors found
    """
    from cudag.validation import validate_dataset

    dataset_path = Path(dataset_dir)
    errors = validate_dataset(dataset_path)

    if not errors:
        click.secho(f"Dataset valid: {dataset_dir}", fg="green")
        raise SystemExit(0)

    # Show errors
    click.secho(f"Found {len(errors)} validation error(s):", fg="red")
    display_errors = errors if verbose else errors[:10]
    for error in display_errors:
        click.echo(f"  {error}")

    if not verbose and len(errors) > 10:
        click.echo(f"  ... and {len(errors) - 10} more (use -v to see all)")

    raise SystemExit(1)


@cli.group()
def eval() -> None:
    """Evaluation commands."""
    pass


@eval.command("generate")
@click.option("--count", "-n", default=100, help="Number of eval cases")
@click.option("--dataset-dir", type=click.Path(exists=True), help="Dataset directory")
def eval_generate(count: int, dataset_dir: str | None) -> None:
    """Generate evaluation cases."""
    click.echo(f"Generating {count} eval cases")
    click.echo("Eval generation not yet implemented")


@eval.command("run")
@click.option("--checkpoint", type=click.Path(exists=True), help="Model checkpoint")
@click.option("--dataset-dir", type=click.Path(exists=True), help="Dataset directory")
def eval_run(checkpoint: str | None, dataset_dir: str | None) -> None:
    """Run evaluations on Modal."""
    click.echo("Running evaluations")
    click.echo("Eval running not yet implemented")


@cli.command()
def datasets() -> None:
    """List datasets on Modal volume."""
    click.echo("Listing datasets on Modal volume...")
    click.echo("Dataset listing not yet implemented")


if __name__ == "__main__":
    cli()
