


import typer
from typing import Annotated

app = typer.Typer()


@app.command()
def search(
    topic: typer.Argument(help='search topic'),
    query: typer.Argument(help='search query')
):
    
    print (f"Topic is {topic}")
    print (f"Query is {query}")

app()