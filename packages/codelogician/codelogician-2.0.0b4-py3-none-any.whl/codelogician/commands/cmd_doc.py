#
#   Imandra Inc.
#
#   cmd_doc.py
#

from pathlib import Path
from typing import Annotated, Final

import typer
from rich import print as printr

from codelogician.doc.utils.api_ref import _load_iar

# =====
# # app
# =====

APP_HELP: Final = """\
A CLI tool for working with ImandraX documentation, api reference, examples and other data.

- Guides - articles on writing IML and using ImandraX
- Applications - tutorials on formalizing various domains (e.g. web development) with ImandraX and reasoning about resulting models
- Examples - a set of worked IML examples
- Ref - ImandraX reference (built-in modules and APIs)
- Errors - a collection of 
- Approximations - a collection of function approximations that may be useful in your coding

Tips:
- Start with `codelogician doc overview` to see available topics
- `codelogician doc prompt` will generate a prompt you could `feed` into your agent/LLM that has a summary of 

- Refer to doc when working with .iml files
    - See available modules: `codelogician doc ref summary`
    - Look up specific modules: `codelogician doc ref list -m <module>`

    - To view 
- To dump docs to markdown files: `codelogician doc dump PATH_TO_STORE_DOCS`
- To search the documents: `codelogician doc search TOPIC`
""" 

app = typer.Typer(
    help=APP_HELP, 
    add_completion=False,
    rich_markup_mode='rich'
)


# =====
# ### doc overview
# =====

def load_doc():
    from pathlib import Path

    from codelogician.doc.utils.docs import DocManager
    doc_location = Path(__file__).parent / '../doc/data'
    return DocManager(str(doc_location.resolve()))


@app.command(name='contents', help='List the contents of the available documentation')
def contents():
    """
    Show the table of contents
    """

    doc = load_doc()
    doc.print_contents()


@app.command(name='prompt', help='Generate a prompt to teach LLMs/Agents how to use ImandraX')
def run_prompt_cmd ():
    """
    Show IML overview documentation.
    """

    from codelogician.doc.utils.prompts import (
        iml_caveats,
        iml_intro,
        lang_agnostic_meta_eg_overview,
        lang_agnostic_meta_egs_str,
    )

    iml_overview = (
        iml_intro
        + iml_caveats
        + lang_agnostic_meta_eg_overview
        + lang_agnostic_meta_egs_str
    )
    typer.echo(iml_overview)

@app.command(help='Dump IML overview and API reference to markdown files')
def dump (
    dir_path: Annotated[
        Path, typer.Argument(help='Directory path to write markdown files')
    ],
):
    
    from codelogician.doc.utils.api_ref import iml_overview_api_dump
    iml_overview_api_dump(dir_path)
    typer.secho('Successfully ', fg='green')


@app.command(name='search', help='Search the entire directory')
def search (
    query : Annotated[str, typer.Argument(help='Search query')],
    topic : Annotated[str, typer.Argument(help='Search a specific topic. Must be one of: guide, api, examples, errors, applications')] = 'all'
):
    """
    Search the documentation with an optional topic parameter. 
    """

    if topic.lower() not in ['all', 'guide', 'api', 'examples', 'errors', 'applications']:
        typer.secho('Optional parameter `topic` has invalid value. Expected one of: `guide`, `api`, `examples`, `errors`, or `applications`')
        typer.Exit(1)

    doc = load_doc()

    results = doc.find_content(query)
    for r in results:
        printr(r)


@app.command(name='view', help='View a specific chapter or topic in documentation')
def view (
        desc : Annotated[str, typer.Argument(help='View a specific topic. Will look for the closest match (within reason)')]
    ):

    doc = load_doc()

    doc_file = doc.find_topic (desc)

    if doc_file is None:
        printr('Found no topic matching the title')
    else:
        printr(doc_file)

# =====
# ### doc api-reference
# =====


api_ref_app = typer.Typer(
    help='IML Reference (built-in functions, types and modules)'
)
app.add_typer(api_ref_app, name='ref')

#@api_ref_app.callback(invoke_without_command=True)
#def default(ctx: typer.Context):
#  typer.echo(ctx.get_help())

@api_ref_app.command(name='summary', help='Provide an overview of the available modules')
def api_ref_summary():
    """
    Show summary of IML Reference (unique modules).
    """
    
    iar = _load_iar()
    modules = sorted({entry.module for entry in iar})

    typer.echo(
        f'IML Reference - {len(iar)} total entries across {len(modules)} modules\n'
    )
    typer.echo('Available modules:')
    for module in modules:
        count = sum(1 for entry in iar if entry.module == module)
        if module == '':
            typer.echo(f'  (global): {count} entries')
        else:
            typer.echo(f'  {module}: {count} entries')


@api_ref_app.command(name='view', help='List IML API reference entries (optionally filtered by module)')
def api_ref_view (
    module: Annotated[str | None, typer.Argument(help='Filter by module name')] = None,
):
    """
    List IML API reference entries (optionally filtered by module)."""
    iar = _load_iar()

    if module is not None:
        iar = [entry for entry in iar if entry.module.lower() == module.lower()]
        if not iar:
            typer.secho(
                f'No entries found for module: {module}', fg=typer.colors.RED, err=True
            )
            raise typer.Exit(1)

    typer.echo(f'Showing {len(iar)} entries\n')

    for entry in iar:
        typer.echo(f"Module: {entry.module or '(global)'}")
        typer.echo(f'Name: {entry.name}')
        typer.echo(f'Signature: {entry.signature}')
        if entry.doc:
            typer.echo(f'Doc: {entry.doc}')
        if entry.pattern:
            typer.echo(f'Pattern: {entry.pattern}')
        typer.echo()

#@api_ref_app.command(name="search", help="Search the Reference")
#def ref_search(
#    topic : Annotated[str, typer.Argument()]
#    ):
#    """
#    Search the ImandraX reference guide
#    """
#    typer.echo(f"Need to return the results of reference search")