#
#   CodeLogician Server
#
#   main.py
#

import typer
from typing_extensions import Annotated
import argparse, uvicorn, logging, sys, os, dotenv
from pathlib import Path

dotenv.load_dotenv(".env")
if 'IMANDRA_UNI_KEY' not in os.environ:
    print ("CodeLogician requires 'IMANDRA_UNI_KEY' to be set!")
    sys.exit(0)

log = logging.getLogger(__name__)

from .cl_server import CLServer
from .config import ServerConfig
from .state import ServerState
from .endpoints import register_endpoints
from .utils import do_intro

#ch = logging.StreamHandler(sys.stdout)
#ch.setLevel(logging.INFO) # Only show INFO and above
#ch.setFormatter(logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"))
#log.addHandler(ch)

def run_server(
    dir : str,
    state : str | None = None,
    clean : bool = False,
    config : Annotated[str, typer.Option("--config", help="Server configuration YAML file")] = "config/server_config.yaml",
    addr : Annotated[str, typer.Option(help="Server address, host/port")] = "http://127.0.0.1:8000"
    ):
    """
    Run the server
    - dir - target directory
    - state - state file to use
    - clean - should we discard any existing changes
    - config - server configuration
    - addr - address we should use instead of the one provided in the config
    """

    do_intro()

    try:
        servConfig = ServerConfig.fromYAML(config)
    except Exception as e:
        log.warning(f"Failed to load in server config: {str(e)}. Using defaults.")
        servConfig = ServerConfig()

    if state:
        # We need to use the existing state
        abs_path = str(Path(state).resolve())

        if not os.path.exists(abs_path):
            log.warning(f"Specified path for server config doesn't exist: [{abs_path}]. Using defaults.")
            state = ServerState(abs_path=abs_path)
        else:
            try:
                state = ServerState.fromFile(abs_path)
            except Exception as e:
                log.error(f"Failed to create server state from specified file: {abs_path}")
                raise Exception (f"Failed to read in server state: {str(e)}")

    else:
        # We're creating a new state
        server_state_abs_path = os.path.join(os.getcwd(), '.cl_server')

        # TODO: Review removal of try ServerState.fromFile(...)
        state = ServerState(abs_path=server_state_abs_path, strategy_paths=[], config=servConfig)

        if dir:
            # We need to add a strategy directory to the state
            abs_path = str(Path(dir).resolve()) # TODO: is os.path.abspath better?

            if not (os.path.exists(abs_path) and os.path.isdir(abs_path)):
                errMsg = f"Specified path must exist and be a directory: {abs_path}"
                log.error(errMsg)
                return

            state.strategy_paths.append(abs_path)

            if clean:
                log.info(f"Starting clean, so will attempt to remove any existing caches!")
                cache_path = os.path.join(abs_path, '.cl_cache')
                if os.path.exists(cache_path):
                    try:
                        os.remove(cache_path)
                        log.info(f"Removed: {cache_path}")
                    except Exception as e:
                        log.error(f"Failed to remove {cache_path}!")
                        return

    server = CLServer(state)
    register_endpoints(server)

    uvicorn.run(
        server,
        host=state.config.host,
        port=state.config.port,
        #reload=state.config.debug,
        log_level="info"
    )
