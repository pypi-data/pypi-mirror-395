#
#   Imandra Inc.
#
#   app.py
#

from pathlib import Path
from textual import work
from textual.app import App
from textual.reactive import reactive
from textual.screen import Screen

from .screens.model import ModelScreen
from .screens.intro import IntroScreen
from .screens.overview import OverviewScreen
from .screens.decomps import DecompsScreen
from .screens.opaques import OpaquesScreen
from .screens.vgs import VGsScreen
from .screens.sketches import SketchScreen
from .screens.help import HelpScreen

from .commands import ServerCommandsProvider, ModelCommandsProvider
from .common import InfoScreen, Source, Status

from ..strategy.state import StrategyState
from ..strategy.config import StratConfigUpdate
from ..strategy.metamodel import MetaModel
from ..strategy.sketch import SketchContainer
from ..util import head, map_values, maybe

import os, httpx, json, argparse, datetime
import typer
from typing_extensions import Annotated

app = typer.Typer()

def curr_meta_model(s): return s.curr_meta_model
def sketches(s): return s.sketches


class CodeLogicianTUI(App):
    CSS_PATH = "tui.tcss"

    status : reactive[None | Status]  = reactive(None)
    strat_states : reactive[dict[str, StrategyState]] = reactive({})
    mmodel : reactive[None | MetaModel] = reactive(None)
    sketch_container : reactive[None | SketchContainer] = reactive(None)
    last_update : reactive[str] = reactive("---")

    MODES = {
        "intro"     : IntroScreen,
        "overview"  : OverviewScreen,
        "model"     : ModelScreen,
        "opaques"   : OpaquesScreen,
        "vgs"       : VGsScreen,
        "decomps"   : DecompsScreen,
        "sketch"    : SketchScreen,
        "help"      : HelpScreen
    }

    DEFAULT_MODE = 'intro'
    BINDINGS = [
        ("i", "switch_mode('intro')"    , "Intro"               ),
        ("o", "switch_mode('overview')" , "Overview"            ),
        ("m", "switch_mode('model')"    , "Model"               ),
        ("v", "switch_mode('vgs')"      , "Verification Goals"  ),
        ("d", "switch_mode('decomps')"  , "Decomps"             ),
        ("k", "switch_mode('opaques')"  , "Opaques"             ),
        ("s", "switch_mode('sketch')"   , "Sketches"            ),
        ("h", "switch_mode('help')"     , "Help"                ),
        ("q", "quit"                    , "Quit"                )
    ]

    COMMANDS = App.COMMANDS | {ServerCommandsProvider} | {ModelCommandsProvider}


    def __init__(self, status: Status):
        super().__init__()
        self.status = status

        # We should now have the issue resolved altogether
        self.console.set_window_title("Imandra CodeLogician v2.0")

    @work()
    async def cl_server_state_retriever(self):
        """
        Polls the server to retrieve the latest state information
        """

        if self.status.source != Source.Server: return

        status = self.status.copy()
        try:
            endpoint = f"{status.server_addr}/strategy/states"
            blob = json.loads(httpx.get(endpoint).text.strip("'"))
            # self.strat_states = map_values(StrategyState.fromJSON, blob)
            self.strat_states = {
                strat_state.src_dir_abs_path: strat_state for
                strat_state in map(StrategyState.fromJSON, blob)
            }
            status.server_last_update = datetime.datetime.now()
            some_strat_state = head(self.strat_states.values())
            # TODO: only override if not set or current setting no longer exists
            self.mmodel = maybe(curr_meta_model, some_strat_state)
            self.sketch_container = maybe(sketches, some_strat_state)
            self.last_update = str(status.server_last_update)
            status.server_error = None

        except Exception as e:
            msg = f"Error when connecting to the server: {e}"
            status.server_error = msg

        self.status = status

    def on_mount(self) -> None:
        if self.status.source == Source.Disk: # TODO: can disk_path be None?
            self.load_disk_strat_states(self.status.disk_path, True)
        elif self.status.source == Source.Server: # TODO: can server_addr be None?
            self.set_server(self.status.server_addr)

    def on_unmount(self) -> None:
        """ on_unmount """
        self.cont = False

    def do_update_strat_config (self, config : StratConfigUpdate):
        """
        This is the callback for PyIMLStrategy configuration
        """
        pass

    def do_execute_server_command (self, command):
        """
        """
        pass

    def do_view_model (self, model_path : str):
        """
        Focus the view on a specific model
        """
        pass

    def do_select_strategy(self, strat_path : str):
        """ Select a specific strategy """
        # TODO: what if strat_path is invalid?
        self.mmodel = maybe(curr_meta_model, self.strat_states[strat_path])
        self.sketch_container = maybe(sketches, self.strat_states[strat_path])

    def set_server(self, host:str):
        """
        Set the source to be the server
        """

        self.status.source = Source.Server
        self.status.server_addr = host
        self.status.disk_error = None
        self.selected_strat = None
        self.timer = self.set_interval(5, self.cl_server_state_retriever)
        self.cl_server_state_retriever()

    def load_disk_strat_states(self, path : Path, startup:bool=False):
        """ Here, we're loading the strategy state directly from disk """

        status = self.status
        status.source = Source.Disk
        status.server_error = None
        status.server_last_update = None
        status.disk_path = path
        try:
            state = StrategyState.from_directory(str(path))
            status.disk_error = None
            self.strat_states = {state.src_dir_abs_path: state}
            self.mmodel = state.curr_meta_model
        except Exception as e:
            errMsg = f"Error loading from disk: {repr(e)}"
            if startup: print(errMsg)
            else: self.push_screen(InfoScreen(errMsg, 'error'))
            status.disk_error = errMsg

        self.status = status

    def get_system_commands(self, screen: Screen):
        yield from super().get_system_commands(screen)


@app.command()
def run_tui(
    server_addr : Annotated[str, typer.Option(help="Server to connect to by default")] = "http://127.0.0.1:8000"
):
    """
    """

    status = Status(
        source = Source.Server,
        server_addr=server_addr,
        disk_path=os.getcwd()
    )

    CodeLogicianTUI(status=status).run()

if __name__ == "__main__":

    app()
    #parser = argparse.ArgumentParser()
    #set_tui_arguments(parser)

    #args = parser.parse_args()
    #run_tui(args)
