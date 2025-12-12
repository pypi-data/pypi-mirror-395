#
#   Imandra Inc.
#
#   cmd_models.py
#


import typer, time
from typing import Annotated
from rich import print as printr
from rich.live import Live
from logging import getLogger
log = getLogger(__name__)

from .utils import CLServerClient
from ..strategy.model import Model, ModelList

app = typer.Typer()


@app.command("list")
def run_model_list (
    live : Annotated[bool, typer.Option(help="If used, then will run the command in a loop.")] = False,
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
    ):
    """
    List info about all models in the current strategy
    """

    cl_client = CLServerClient(addr)

    if live:
        resp = cl_client.get("metamodel/list")
        model_list = ModelList.model_validate_json(resp.json())

        with Live(model_list, refresh_per_second=4) as live:
            while True:
                resp = cl_client.get("metamodel/list")
                live.update(ModelList.model_validate_json(resp.json()))
                time.sleep(1)

    else:
        resp = cl_client.get("metamodel/list")
        printr (ModelList.model_validate_json(resp.json()))

@app.command("view")
def run_model_view (
    index : Annotated[int, typer.Argument(help="Index of the model to view")],
    live : Annotated[bool, typer.Option(help="If used, then will run the command in a loop.")] = False,
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
    ):
    """
    View model specified by index
    """

    cl_client = CLServerClient(addr)

    resp = cl_client.get(f"model/byindex/{index}")
    model = Model.model_validate_json(resp.json())

    if live:
        with Live(model, refresh_per_second=1) as live:
            resp = cl_client.get(f"model/byindex/{index}")
            live.update(Model.model_validate_json(resp.json()))
            time.sleep(1)
    else:
        printr (model)


@app.command("freeze")
def run_model_cmd_freeze(
    index : Annotated[int, typer.Argument(help="Freezes the IML code b/c of user changes.")],
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
    ):
    
    cl_client = CLServerClient(addr)

    resp = cl_client.post(f"model/cmd/freeze/{index}")

    printr (resp.json())

@app.command("unfreeze")
def run_model_cmd_unfreeze(
    index : Annotated[int, typer.Argument(help="Unfreezes the model if frozen. User-specified IML code will be overriden if needed.")],
    addr : Annotated[str, typer.Option(help="CL Server address")] = "http://127.0.0.1:8000"
    ):
    
    cl_client = CLServerClient(addr)
    
    resp = cl_client.post(f"model/cmd/unfreeze/{index}")

    printr(resp.json())