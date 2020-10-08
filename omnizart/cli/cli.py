"""The entry point of the ``omnizart`` command.

Sub-commands are also added here.

Examples
--------
.. code-block:: bash

    omnizart --help
    omnizart music --help
"""

import click

import omnizart.constants.datasets as dset
from omnizart.remote import download, download_large_file_from_google_drive
from omnizart.utils import ensure_path_exists
from omnizart.cli.music import music
from omnizart.cli.drum import drum
from omnizart.cli.transcribe import transcribe


@click.group()
def entry():
    pass


@click.command()
@click.argument("dataset", type=click.Choice(["Maestro", "MusicNet", "McGill"], case_sensitive=False))
@click.option(
    "-o", "--output", default="./", help="Path for saving the downloaded dataset.", type=click.Path(writable=True))
def download_dataset(dataset, output):
    """A quick command for downloading datasets."""
    url = {
        "maestro": dset.MaestroStructure.url,
        "musicnet": dset.MusicNetStructure.url,
        "mcgill": dset.McGillBillBoard.url
    }[dataset.lower()]
    ensure_path_exists(output)
    click.echo(f"Downloading {dataset} dataset and save to {output}")
    if "drive.google.com" in url:
        download_large_file_from_google_drive(url, save_path=output, save_name=dataset+".zip")
    else:
        download(url, save_path=output)


entry.add_command(music)
entry.add_command(drum)
entry.add_command(transcribe)
entry.add_command(download_dataset)


if __name__ == "__main__":
    entry()
