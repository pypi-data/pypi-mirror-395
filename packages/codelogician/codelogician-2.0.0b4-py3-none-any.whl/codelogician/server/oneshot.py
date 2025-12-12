#
#   Imandra Inc.
#
#   oneshot.py
#

import typer
from typing_extensions import Annotated
import logging, sys, os, dotenv
from pathlib import Path

dotenv.load_dotenv(".env")
if 'IMANDRA_UNI_KEY' not in os.environ:
    print ("CodeLogician requires 'IMANDRA_UNI_KEY' to be set!")
    sys.exit(0)

app = typer.Typer()

from .utils import do_intro
from .config import ServerConfig
from ..strategy.config import StratConfig
from ..strategy.state import StrategyState
from ..strategy.pyiml_strategy import PyIMLStrategy

log = logging.getLogger(__name__)


@app.command()
def run_oneshot(
    dir : Annotated[str, typer.Argument(help="Target directory")],
    clean : Annotated[bool, typer.Option("--clean", help="Start clean by disregarding any existing cache files")] = False,
    config : Annotated[str, typer.Option("--config", help="Server configuration YAML file")] = "config/server_config.yaml"
):
    """
    Run the strategy PyIML in oneshot mode.
    """

    do_intro()

    try:
        servConfig = ServerConfig.fromYAML(config)
    except Exception as e:
        print(f"Failed to load in server config: {str(e)}. Using defaults.")
        servConfig = ServerConfig()

    strat_config = servConfig.strat_config("pyiml")

    if not Path(dir).is_absolute():
        dir = str(Path(dir).resolve())

    if clean:
        if Path(dir).is_dir():
            state = StrategyState(src_dir_abs_path=dir)
        else:
            state = StrategyState(src_dir_abs_path=str(Path(dir).parent))
    else:
        try:
            state = StrategyState.from_directory(dir) # We will later initialize the path
        except Exception as e:
            print (f"Encountered an exception when loading the cache: {str(e)}. Using empty state.")
            state = StrategyState(src_dir_abs_path=dir)

    strategy = PyIMLStrategy(state, strat_config, oneshot=True)
    
    strategy.start()

    log.info("Strategy thread started")
    strategy.join()

    try:
        state.save()
        log.info(f"Saved state to file: {state.src_dir_abs_path}")
    except Exception as e:
        print (f"Failed to save the state to disk: {str(e)}")


if __name__ == "__main__":
    app()