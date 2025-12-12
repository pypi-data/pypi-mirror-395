#
#   Imandra Inc.
#
#   cmd_sketches.py
#

import typer
from typing import Annotated

from rich import print as rprint
from logging import getLogger
log = getLogger(__name__)

from .utils import CLServerClient

app = typer.Typer()

@app.command("list")
def run_sketches_list (
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
    ):
    """
    Run search command
    """

    cl_client = CLServerClient(addr)

    response = cl_client.get("sketches/list")

    if len(response.json()) == 0:
        print ("No results found!")
    else:
        for res in response.json():
            rprint (res)
    
@app.command("create")
def run_sketches_create(
    rel_path : Annotated[str, typer.Argument(help="Relative path of the model to use as the anchor")],
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
):
    """
    Create a new sketch
    """
    
    typer.echo(f"I'm in run_sketches_create")

@app.command("delete")
def run_sketches_delete(
    sketch_id : Annotated[str, typer.Argument(help="Sketch ID of the sketch to be deleted")],
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
):
    """
    Delete a sketch
    """
    typer.echo(f"I'm in run_sketches_delete")