#
#   Imandra Inc.
#
#   main.py - Main entrypoint for CodeLogician
#

import logging, asyncio, os, shutil, typer
from pathlib import Path
from typing import Annotated, Final

from rich import print as printr

#from codelogician.commands.cmd_search import run_search
from codelogician.commands.cmd_doc import app as doc_app
from codelogician.commands.cmd_eval import app as eval_app
from codelogician.commands.cmd_metamodel import app as metamodel_app
from codelogician.commands.cmd_model import app as model_app
from codelogician.commands.cmd_sketches import app as sketches_app
from codelogician.commands.cmd_strategy import app as strategy_app

# logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("fsevents").setLevel(logging.WARNING)
#logging.getLogger("strategy.pyiml_strategy").setLevel(logging.WARNING)
#logging.getLogger("strategy.cl_worker").setLevel(logging.WARNING)
#logging.getLogger("strategy.metamodel").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

def setup_logging(debug:bool=False):
    logging.basicConfig(
        level = logging.DEBUG if debug else logging.WARNING,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [logging.FileHandler("cl.log"), logging.StreamHandler()],
    )

CL_HELP : Final = """
[bold deep_sky_blue1][italic]CodeLogician[/italic] is the neurosymbolic agentic governance framework for AI-powered coding.[/bold deep_sky_blue1] :rocket:

[white]***[bold italic purple]It helps your coding agent think logically about the code it's producing and test cases it's generating.[/bold italic purple]***
The fundamental flaw that all LLM-powered assistants have is the reasoning they're capable of is based on statistics,
while you need rigorous logic-based automated reasoning.

- Generated code is based on explainable logic, not pure statistics
- Generated test cases are generated come with quantitative coverage metrics
- Generated code is consistent with the best security practices leveraging formal verification

To run [bold italic deep_sky_blue1]CodeLogician[/bold italic deep_sky_blue1], please obtain an [bold italic deep_sky_blue1]Imandra Universe API[/bold italic deep_sky_blue1] key available
(there's a free starting plan) at [bold italic deep_sky_blue1]https://universe.imandra.ai[/bold italic deep_sky_blue1] and make
sure it's available in your environment as [bold italic deep_sky_blue1]`IMANDRA_UNIVERSE_KEY`[/bold italic deep_sky_blue1].

[bold deep_sky_blue1 italic]Three typical workflows[/bold deep_sky_blue1 italic]:
1. [bold deep_sky_blue1 italic]DIY mode[/bold deep_sky_blue1 italic] - this is where your agent (e.g. Grok) uses the CLI to:
  - Learn how to use IML/ImandraX via `doc` command (e.g. `codelogician doc --help`)
  - Synthesizes IML code and uses the `eval` command to evaluate it
  - If there're errors, use `codelogician doc view errors` command to study how to correct the errors and re-evalute the code

2. [bold deep_sky_blue1 italic]Agent/multi-agent mode[/bold deep_sky_blue1 italic] - CodeLogician Agent is a Langgraph-based agent for automatically formalizing source code.
  - With `agent` command you can formalize a single source code file (e.g. `codelogician agent PATH_TO_FILE`)
  - With `multiagent` command you can formalize a whole directory (e.g. `codelogician agent PATH_TO_DIR`)

3. [bold deep_sky_blue1 italic]Server[/bold deep_sky_blue1 italic] - this is a "live" and interactive version of the `multiagent` command, but one you can interact with and one that
"listens" to live updates and automatically updates formalization as necessary. You can start the server and connect to it
with the TUI (we recommend separate terminal screens).

Learn more at[/white] [bold italic deep_sky_blue1]https://www.codelogician.dev![/bold italic deep_sky_blue1]
"""

app = typer.Typer(
    name="CodeLogician",
    help=CL_HELP,
    rich_markup_mode="rich"
)

app.add_typer(model_app     , name="model"      , help="Model-related commands (e.g. view and list)")
app.add_typer(strategy_app  , name="strategy"   , help="Server function for creating and managing strategies")
app.add_typer(metamodel_app , name="metamodel"  , help="Server metamodel-related functions")
app.add_typer(sketches_app  , name="sketches"   , help="Server API for creating and managing sketches")
app.add_typer(doc_app       , name="doc"        , help="Documentation, guides and ImandraX reference")
app.add_typer(eval_app      , name="eval"       , help="Evaluate IML file via ImandraX API")


#@app.callback(invoke_without_command=True)
#def default(ctx: typer.Context):
#  print (ctx.command.params)
#  typer.echo(ctx.get_help())

@app.command(name="sample", help="Creates a sample Python project in specified directory (relative to the current directory)")
def run_sample_cmd(
    tgt_dir : Annotated[str, typer.Argument(help="Target directory where to place the sample project")]
    ):
    """
    Create a sample project
    """

    full_tgt_dir = Path(os.path.join(os.getcwd(), tgt_dir)).resolve()

    try: os.makedirs(full_tgt_dir)
    except:
        typer.secho(f"⚠️ Sample directory already exists!")
        pass

    if not os.path.exists(full_tgt_dir):
        print (f"🛑 Failed to create sample project directory: {full_tgt_dir}")
        return

    source_dir = "data/sample_bank_app"

    for filepath in os.listdir(source_dir):
        if filepath.endswith(".py"):
            tgt_filepath = os.path.join(full_tgt_dir, Path(filepath).name)
            try:
                shutil.copyfile(os.path.join(source_dir, filepath), tgt_filepath)
            except Exception as e:
                typer.secho (f"🛑 Failed to copy project file: {filepath} {tgt_filepath}: {e}", err=True)
                raise typer.Exit(1)

    typer.secho(f"✅ Created sample project in: {full_tgt_dir}")

@app.command(name="server", help="Start the server")
def run_server_cmd (
    dir     : Annotated[str, typer.Argument(help="Starting directory")],
    state   : Annotated[str | None, typer.Option(help="Server state path")] = None,
    clean   : Annotated[bool, typer.Option(help="Disregard existing strategy caches")] = False,
    config  : Annotated[str, typer.Option(help="Configuration path")] = "config/server_config.yaml",
    debug   : Annotated[bool, typer.Option(help="Debug mode")] = False,
    addr    : Annotated[str, typer.Option(help="Server host/port")] = "http://127.0.0.1:8000"
    ):

    from codelogician.server.main import run_server

    setup_logging(debug=debug)

    run_server (
        dir = dir,
        state = state,
        clean = clean,
        config = config,
        addr = addr
    )

@app.command(name="multiagent", help="Run the CL server in autoformalization mode for a directory and then quit.")
def run_oneshot_cmd(
    dir     : Annotated[str, typer.Argument(help="Target directory")],
    clean   : Annotated[bool, typer.Option(help="Start clean by disregarding any existing cache files")] = False,
    config  : Annotated[str, typer.Option(help="Server configuration YAML file")] = "config/server_config.yaml",
    debug   : Annotated[bool, typer.Option(help="Debug mode")] = False
    ):

    from codelogician.server.oneshot import run_oneshot

    setup_logging(debug=debug)
    run_oneshot(dir, clean, config)

@app.command(name="tui", help="Run the TUI")
def run_tui_cmd(
    addr : Annotated[str, typer.Option(help="Server host/port")] = "http://127.0.0.1:8000"
    ):
    """
    Run the TUI
    """

    from codelogician.ui.main import run_tui

    run_tui(addr)

@app.command(name="agent", help="Formalize a file via CodeLogician agent")
def run_frmfile_cmd (
    file : Annotated[Path, typer.Argument(help="Path to a source code file to run the CL agent on")],
    outfile : Annotated[Path, typer.Argument(help="Output file path to save the resulting CL Agent state")] = Path("cl_result.json"),
    artifacts : Annotated[bool, typer.Option(help="Should we generate artifacts like Verification Goals and Decomposition requests")]=True
    ):
    """
    Read the provided file and run CodeLogician Agent on it, saving the result in `outfile` file.
    """

    from imandra.u.agents.code_logician import SUPPORTED_LANGUAGES

    from codelogician.tools.cl_caller import call_cl_agent

    language = None
    for l in SUPPORTED_LANGUAGES:
        lang, ext = l
        if file.suffix == ext:
            language = lang
            break

    if language is None:
        typer.secho(f"🛑 Unsupported language with extension: {file.suffix}. Only the following are supported: {SUPPORTED_LANGUAGES}")
        raise typer.Exit(1)

    try:
        src_code = file.read_text()
    except Exception as e:
        typer.secho(f"🛑 Failed to read the file: {e}")
        raise typer.Exit(1)

    try:
        res = asyncio.run(call_cl_agent(src_code = src_code, language=language, artifacts=artifacts))
    except Exception as e:
        typer.secho(f"🛑 Caught exception during the call: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    if res is None:
        typer.secho(f"🛑 Failed to execute the CL agent. Received `None`", err=True)
        raise typer.Exit(1)

    printr(res)

    try:
        with open(outfile, "w") as outfile_file:
            data = res.model_dump(mode='json')
            fields = ['status', 'src_code', 'src_lang', 'eval_res', 'vgs', 'region_decomps', 'iml_code', 'iml_model']
            select_data = {k: data[k] for k in fields if k in data }
            import json
            print (json.dumps(select_data, indent=4), file=outfile_file)
            typer.secho(f"✅ Written results to {outfile}!")

    except Exception as e:
        typer.secho(f"🛑 Failed to print to out file: {e}", err=True)
        raise typer.Exit(1)


def run_codelogician():
    app()

if __name__ == "__main__":
    app()
