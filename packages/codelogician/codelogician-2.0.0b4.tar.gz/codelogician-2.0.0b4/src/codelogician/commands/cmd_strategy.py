#
#   Imandra Inc.
#
#   cmd_strategy.py
#


import typer
from rich import print as printr
from rich.pretty import Pretty
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
from typing import Annotated
from logging import getLogger
from .utils import CLServerClient

log = getLogger(__name__)
app = typer.Typer()

console = Console()

@app.command(name="list")
def run_strategy_list ():
    """
    List all current strategies
    """

    cl_client = CLServerClient()
    resp = cl_client.get("/strategy/list")

    if len(resp) == 0:
        console.print("[bold magenta]No strategies[/bold magenta]")
    else:
        for s in resp:
            console.print_json(data=s)

@app.command(name="cws", help="Get current working strategy")
def run_strategy_cws ():
    """
    Get the current working strategy
    """

    cl_client = CLServerClient()
    resp = cl_client.get("/strategy/cws")
    printr (f"Current working strategy: {resp}")

@app.command(name="setcws", help="Set current working stratey (cws)")
def run_strategy_set_cws(
    strat_id : Annotated[str, typer.Argument()]
    ):
    """
    Set current working strategy
    """

    cl_client = CLServerClient()

    try:
        res = cl_client.post(f"/strategy/setcws/{strat_id}")
    except Exception as e:
        printr(f"Encountered an error during POST request: {e}")

    if 'detail' in res:
        printr(f"[bold red]{res['detail']}[/bold red]")
    else:
        printr(f"[bold][magenta]Successfully updated current working strategy to: {strat_id}[/magenta][/bold]")

@app.command(name="create", help="Create a new strategy within the server")
def run_strategy_create (
    stype : Annotated[str, typer.Argument(help="Strategy type (e.g. 'PyIML')")],
    spath : Annotated[str, typer.Argument(help="Strategy directory path")]
    ):
    """
    Create a new strategy
    """
    
    cl_client = CLServerClient()

    try:
        resp = cl_client.post(
            f"/strategy/create", 
            data={'strat_type': stype, 'strat_path': spath}
        )
    except Exception as e:
        printr (f"Encountered an error during POST request: {e}")
        return
    
    printr (f"[bold magenta]Successfully created a strategy: {resp}")

@app.command(name="delete", help="Delete/remove strategy from the server")
def run_strategy_delete (
    strat_id : Annotated[str, typer.Argument(help="Strategy ID of the strategy to be deleted")]
    ):
    """
    Delete an existing strategy
    """

    cl_client = CLServerClient()

    try:
        resp = cl_client.post(f"/strategy/delete/{strat_id}")
    except Exception as e:
        printr (f"Encountered an error during POST request: {e}")
        return
    
    if resp == {'status': 'OK'}:
        printr (f"[bold magenta]Successfully deleted: {strat_id} strategy[/bold magenta]")
    else:
        print (resp)
        printr (f"[bold red]Something went wrong[/bold red]")

@app.command(name="summary", help="Get current working strategy's summary")
def run_strategy_summary () -> dict:
    """
    Retrieve current working strategy's summary
    """

    cl_client = CLServerClient()

    resp = cl_client.get("/strategy/summary")

    print (f"Summary for the current strategy:")
    printr(Pretty(resp))