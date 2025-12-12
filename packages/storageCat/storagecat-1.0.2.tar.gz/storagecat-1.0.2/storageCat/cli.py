import subprocess
import sys

import click

from .classes import SciCat, ScientificMetadata


@click.group()
def cli():
    """StorageCat - SciCat dataset management tool."""
    pass


@cli.command()
@click.option(
    "--output", "-o", default="metadata.json", type=click.Path(), help="Output JSON file path"
)
def build(output):
    cat = """
    |\---/|
    | ,_, |
     \_`_/-..----.
  ___/ `   ' ,""+ \  storageCat
 (__...'   __\    |`.___.';
  (_,...'(_,.`__)/'.....+
    """
    click.echo(click.style(cat, fg="cyan"))
    click.echo(click.style("\n=== SciCat Dataset Creation ===\n", fg="green", bold=True))

    click.echo(click.style("Scientific Metadata (Required):", fg="yellow", bold=True))
    sample_name = click.prompt("Sample name", type=str)
    collection_date = click.prompt("Data collection date", type=str)

    sample_info = {"name": sample_name}
    collection_info = {"date": collection_date}

    click.echo(click.style("\nDataset Information (Required):", fg="yellow", bold=True))
    data_format = click.prompt("Data format", type=str)
    source_folder = click.prompt("Source folder", type=str)
    dataset_name = click.prompt("Dataset name", type=str)
    description = click.prompt("Description", type=str)
    owner = click.prompt("Owner", type=str)
    ip = click.prompt("This will be published (true/false)", type=str)
    dataset_type = click.prompt("Dataset type (raw, derived)", type=str)
    creation_location = click.prompt("Creation location", type=str)
    owner_group = click.prompt("Owner group", type=str)

    other_params = {}
    click.echo(click.style("\nAdditional Parameters (Optional):", fg="cyan"))
    if click.confirm("Add other parameters to scientific metadata?", default=False):
        while True:
            key = click.prompt("  Parameter name (or 'done' to finish)", type=str, default="done")
            if key.lower() == "done":
                break
            value = click.prompt(f"  Value for '{key}'", type=str)
            other_params[key] = value

    other_fields = {}
    if click.confirm("Add other fields to documentation?", default=False):
        while True:
            key = click.prompt("  Field name (or 'done' to finish)", type=str, default="done")
            if key.lower() == "done":
                break
            value = click.prompt(f"  Value for '{key}'", type=str)
            other_fields[key] = value

    sci_metadata = ScientificMetadata(
        sample=sample_info,
        dataCollection=collection_info,
        otherParameters=other_params if other_params else None,
    )

    scicat = SciCat(
        dataFormat=data_format,
        sourceFolder=source_folder,
        datasetName=dataset_name,
        description=description,
        owner=owner,
        type=dataset_type,
        creationLocation=creation_location,
        ownerGroup=owner_group,
        scientificMetadata=sci_metadata,
        isPublished=ip,
        otherFields=other_fields if other_fields else None,
    )

    if output:
        scicat.to_json(output)
        click.echo(click.style(f"\n Dataset saved to: {output}", fg="green", bold=True))
    else:
        click.echo(click.style("\n=== Generated JSON ===", fg="green", bold=True))
        click.echo(scicat.to_json())


@cli.command()
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    default="metadata.json",
    help="Input JSON file to check (default: metadata.json)",
)
@click.option(
    "--module",
    "-m",
    type=str,
    default="datacatalog",
    help="Module name to load (default: datacatalog)",
)
@click.option(
    "--token",
    type=str,
    default=None,
    help="SciCat Token. For PSI, found at https://discovery.psi.ch/user",
)
def check(input, module, token):
    """Check metadata without submitting to the datacatalog."""

    if token is None:
        token = click.prompt("SciCat Token", type=str)

    try:
        click.echo(f"Loading module: {module}")
        load_result = subprocess.run(
            f"module load {module}",
            shell=True,
            executable="/bin/bash",
            capture_output=True,
            text=True,
        )

        if load_result.returncode != 0:
            click.echo(
                click.style(f"Warning: module load returned non-zero exit code", fg="yellow")
            )
            if load_result.stderr:
                click.echo(f"   {load_result.stderr.strip()}")

        click.echo(f"Checking metadata from: {input}")
        check_cmd = f"module load {module} && datasetIngestor -token {token} {input}"
        check_result = subprocess.run(
            check_cmd, shell=True, executable="/bin/bash", capture_output=True, text=True
        )

        click.echo(click.style("\n=== Check Results ===", fg="cyan", bold=True))

        if check_result.stdout:
            click.echo(check_result.stdout)

        if check_result.stderr:
            click.echo(click.style("Errors/Warnings:", fg="yellow"))
            click.echo(check_result.stderr)

        if check_result.returncode == 0:
            cat = """
                  |\      _,,,---,,_
           ZZZzz /`.-'`'    -.  ;-;;,_
                |,4-  ) )-,_. ,\ (  `'-'
                '---''(_/--'  `-'\_)
            """
            click.echo(click.style(cat, fg="cyan"))
            click.echo(
                click.style(
                    f"\nCommand completed (exit code: 0). Now run `storageCat submit` to begin to archive",
                    fg="green",
                )
            )
        else:
            click.echo(
                click.style(
                    f"\nCommand completed with exit code: {check_result.returncode}", fg="yellow"
                )
            )

    except Exception as e:
        click.echo(click.style(f"\nError during check: {str(e)}", fg="red", bold=True))
        sys.exit(1)


@cli.command()
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    default="metadata.json",
    help="Input JSON file to submit (default: metadata.json)",
)
@click.option(
    "--module",
    "-m",
    type=str,
    default="datacatalog",
    help="Module name to load (default: datacatalog)",
)
@click.option(
    "--token",
    type=str,
    default=None,
    help="SciCat Token. For PSI, found at https://discovery.psi.ch/user",
)
def submit(input, module, token=None):
    """Submit metadata to the datacatalog."""
    if token is None:
        token = click.prompt("SciCat Token", type=str)
    try:
        click.echo(f"Loading module: {module}")
        load_result = subprocess.run(
            f"module load {module}",
            shell=True,
            executable="/bin/bash",
            capture_output=True,
            text=True,
        )

        if load_result.returncode != 0:
            click.echo(
                click.style(f"Warning: module load returned non-zero exit code", fg="yellow")
            )
            if load_result.stderr:
                click.echo(f"   {load_result.stderr.strip()}")

        click.echo(f"Ingesting metadata from: {input}")
        ingest_cmd = f"module load {module} && datasetIngestor -token {token} --ingest {input}"
        ingest_result = subprocess.run(
            ingest_cmd, shell=True, executable="/bin/bash", capture_output=True, text=True
        )

        if ingest_result.returncode == 0:
            cat = """
                        _ |\_
                        \` ..|
                   __,.-" =__Y=
                 ."        )
            _   /   ,    \/\_
          ((____|    )_-\ \_-`
          `-----'`-----` `--`
            """
            click.echo(click.style(cat, fg="cyan"))
            click.echo(click.style(f"\nSuccessfully submitted {input}!", fg="green", bold=True))
            if ingest_result.stdout:
                click.echo(ingest_result.stdout)
        else:
            click.echo(click.style(f"\nSubmission failed!", fg="red", bold=True))
            if ingest_result.stderr:
                click.echo(click.style(f"Error: {ingest_result.stderr}", fg="red"))
            sys.exit(1)

    except Exception as e:
        click.echo(click.style(f"\nError during submission: {str(e)}", fg="red", bold=True))
        sys.exit(1)


if __name__ == "__main__":
    cli()
