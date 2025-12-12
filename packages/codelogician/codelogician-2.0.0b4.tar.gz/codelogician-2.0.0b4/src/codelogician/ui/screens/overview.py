#
#   Imandra Inc.
#
#   overview.py
#

import os
from pathlib import Path
from typing import Iterable, Dict

from textual.app import on
from textual.screen import Screen
from textual.reactive import reactive
from textual.widgets import (
    Footer, Input, Static, Button, TabbedContent, TabPane,
    RadioButton, RadioSet, Rule, DirectoryTree, Select
)
from textual.containers import Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll

from codelogician.util import map, dup, maybe_else
from codelogician.strategy.state import StrategyState
from codelogician.strategy.metamodel import MetaModel
from ..common import Border, MyHeader, Source, Status, bind

class FilteredDirectoryTree(DirectoryTree):
    """ We just want to show directories and `cl_cache` files. """
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        l = lambda x: x.name.startswith(".cl_cache") or os.path.isdir(x)
        return [path for path in paths if l(path)]

class SelectFileDirectory(Screen):
    DEFAULT_CSS = """VerticalGroup { align: center middle; width: 70%; height: 90% }"""

    def __init__(self, initial_path): # , name = None, id = None, classes = None):
        # super().__init__(name, id, classes)
        super().__init__()
        self.styles.align_horizontal = 'center'
        self.styles.align_vertical = 'middle'
        self._path_selected = initial_path

    def compose(self):
        with VerticalGroup():
            root = self._path_selected or os.getcwd()
            yield Static("Select directory or cache file location")
            yield FilteredDirectoryTree(path=root, id="directory_tree")
            with HorizontalGroup():
                yield Button("Go up", action="screen.go_up")
                yield Button("Select", action="screen.select")
                yield Button("Cancel", action="screen.cancel")

    @on(DirectoryTree.DirectorySelected)
    def select_directory(self, event):
        self._path_selected = event.path

    def action_cancel(self): self.dismiss(None)
    def action_select(self): self.dismiss(self._path_selected)
    def action_go_up(self):
        directoryTree = self.query_one("#directory_tree")
        directoryTree.path = os.path.dirname(directoryTree.path)
        directoryTree.reload()


class SourceSelectionView(VerticalGroup):
    """
    """
    # DEFAULT_CSS = "TabPane  { padding: 1 1 0 4 }"

    disk_path = reactive(None, recompose=True)

    def __init__(self, status):
        super().__init__()
        self.status = status
        self.disk_path = status.disk_path

    def compose (self):
        source_is_disk = (self.status.source == Source.Disk)
        with Border("Select CL source (server/disk):"):
            with TabbedContent(initial="disk_vg" if source_is_disk else "server_vg"):
                with TabPane("Disk", id="disk_vg"):
                    # with VerticalGroup(id="disk_vg") as vg:
                    yield Static(content=f"Current selection: {self.disk_path or ""}")
                    with HorizontalGroup():
                        yield Button("Select source", id="directory_view")
                        yield Button("Apply", id="apply_disk")
                with TabPane("Server", id="server_vg"):
                    # with VerticalGroup(id="server_vg") as vg:
                    yield Static("Enter CodeLogician server details:")
                    yield Input(value=self.status.server_addr or "", id="server_address")
                    yield Button("Apply", id="apply_server")

    @on(Button.Pressed, "#apply_server")
    def on_apply_server (self) -> None:
        host = self.query_one("#server_address")
        self.app.set_server(host.value)

    @on(Button.Pressed, "#apply_disk")
    def on_apply_disk (self, event : Button.Pressed):
        self.app.load_disk_strat_states(self.disk_path)

    @on(Button.Pressed, "#directory_view")
    def on_directory_view(self, event : Button.Pressed):
        def get_path(path : str | None):
            if path: self.disk_path = path

        self.app.push_screen(SelectFileDirectory(self.disk_path), get_path)


class StatusView(Static):
    status = reactive(None, layout=True, init=False)
    def render(self): return self.status


class StatesView(VerticalScroll):
    strat_states = reactive({}, recompose=True)

    def compose(self):
        if self.strat_states:
            for idx, strat in enumerate(self.strat_states.values()):
                pretty = maybe_else("N/A", lambda m: m.rich_summary(), strat.curr_meta_model)
                yield Border(strat.src_dir_abs_path, Static(pretty))


class OverviewScreen(Screen):
    """ Overview Screen """

    DEFAULT_CSS = """OverviewScreen Border {
        border: round $primary;
        border-title-align: center;
        padding: 0 1 0 1;
    }"""

    strat_states    = reactive({})
    mmodel          = reactive(None, recompose=True)
    status          = reactive(Status(source=Source.Server))

    def __init__(self):
        Screen.__init__(self)
        self.title = "Overview"
        bind(self, "status", "strat_states", "mmodel")

    def compose(self):
        strat_states = self.strat_states or []
        kwargs = maybe_else({}, lambda m: {"value": m.src_dir_abs_path}, self.mmodel)

        yield MyHeader()
        with VerticalGroup():
            with HorizontalGroup() as h:
                yield SourceSelectionView(self.status)
                with VerticalGroup():
                    yield Border("TUI Status", StatusView().data_bind(OverviewScreen.status))
                    with Border("Select an available strategy:"):
                        yield Select(options=map(dup, self.strat_states),
                                    prompt="Click to select a strategy",
                                    allow_blank=False, **kwargs)
            yield Static(" [b]Summary of available strategies[/b]")
            yield StatesView().data_bind(OverviewScreen.strat_states)

        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed):
        self.app.do_select_strategy(event.value)
