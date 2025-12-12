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
    owner_email = click.prompt("Owner email", type=str)
    dataset_type = click.prompt("Type", type=str)
    pi = click.prompt("Principal Investigator", type=str)
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
        ownerEmail=owner_email,
        type=dataset_type,
        principleInvestigator=pi,
        creationLocation=creation_location,
        ownerGroup=owner_group,
        scientificMetadata=sci_metadata,
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
    help="Input JSON file to submit (default: metadata.json)",
)
@click.option(
    "--module",
    "-m",
    type=str,
    default="datacatalog",
    help="Module name to load (default: datacatalog)",
)
def submit(input, module):
    """Submit metadata to the datacatalog."""
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
        ingest_cmd = f"module load {module} && datasetIngestor --ingest {input}"
        ingest_result = subprocess.run(
            ingest_cmd, shell=True, executable="/bin/bash", capture_output=True, text=True
        )

        if ingest_result.returncode == 0:
            cat = """
                  |\      _,,,---,,_
           ZZZzz /,`.-'`'    -.  ;-;;,_
                |,4-  ) )-,_. ,\ (  `'-'
                '---''(_/--'  `-'\_)
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
