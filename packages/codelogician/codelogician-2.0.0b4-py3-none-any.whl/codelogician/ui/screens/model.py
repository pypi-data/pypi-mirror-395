# ruff: noqa: E741, UP031, RUF012
from pathlib import Path

from rich.text import Text
from textual import on, work
from textual.app import events
from textual.css.query import NoMatches
from textual.containers import (
    Horizontal,
    HorizontalGroup,
    ScrollableContainer,
    VerticalGroup,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Button,
    Collapsible,
    Footer,
    Label,
    Pretty,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from codelogician.util import filter, maybe, maybe_else, not_none, fst
from codelogician.strategy.model import Model
from codelogician.strategy.metamodel import MetaModel

from ..common import Border, MyHeader, decomp_ui, opaques_rich, vg_ui, bind
from ..step_view import StepView
from ..tree_views import TreeViews
from .model_cmds import ModelCommandsView


def code_view(title, lang, code, collapsed=True, max_height=16):
    from rich.syntax import Syntax

    with Collapsible(title=title, collapsed=collapsed) as c:
        c.styles.height = "auto"
        with ScrollableContainer() as c:
            c.styles.height = "auto"
            c.styles.max_height = max_height
            renderable = Syntax(code, lang, line_numbers=True, indent_guides=True)
            s = Static(renderable, id=lang, classes='code')
            s.styles.width = "auto"
            s.styles.min_width = "100%"
            yield s


def view_opaques(opaques):
    header, table = opaques_rich(opaques)
    with Collapsible(title=header):  # "Opaque functions"):
        yield Static(table)


def view_vgs(vgs):
    with Collapsible(title="Verification goals"):
        for i, vg in enumerate(vgs):
            yield Border("VG #%d" % (i + 1), vg_ui(vg))


def view_decomps(decomps):
    with Collapsible(title="Region decomposition"):
        for i, d in enumerate(decomps):
            yield Border("#%d" % (i + 1), decomp_ui(d))

def view_errors(errors):
    def error_ui(e):
        from textual.widgets import Pretty
        return Pretty(e)

    with Collapsible(title="Formalization errors"):
        for i, e in enumerate(errors):
            yield Border("#%d" % (i + 1), error_ui(e))


def if_nonempty(f, xs):
    if len(xs) > 0:
        yield from f(xs)


class ModelStateView(VerticalGroup):
    DEFAULT_CSS = """StepView { margin: 0 1 0 0; }"""

    def __init__(self, model, container):
        VerticalGroup.__init__(self)
        self.model = model
        self.container = container

    def compose(self):
        fstate = self.model.agent_state
        if fstate is None:
            yield Static("Not formalised")
        else:
            yield from code_view("IML code", "ocaml", fstate.iml_code, collapsed=False)
            yield from if_nonempty(view_opaques, fstate.opaque_funcs)
            yield from if_nonempty(view_vgs, fstate.vgs)
            yield from if_nonempty(view_decomps, fstate.region_decomps)
            yield from if_nonempty(view_errors, fstate.errors)


class ModelView(VerticalGroup):
    DEFAULT_CSS = "#status { margin-top: 1; margin-bottom: 1 }"

    def __init__(self, model: Model, container):
        VerticalGroup.__init__(self)
        self.model = model
        self.container = container

    def compose(self):
        yield Label("[$accent][b]%s[/b][/]" % self.model.rel_path)
        with VerticalScroll():
            yield Static(self.model.status(), id="status")
            yield from code_view("Src code", "python", self.model.src_code, collapsed=False)
            yield ModelStateView(self.model, self.container)

class DecompsView(VerticalGroup):
    def __init__(self, state_of_path, paths: list[Path], container, *args, **kwargs):
        VerticalGroup.__init__(self, *args, **kwargs)
        self.state_of_path = state_of_path
        self.paths = paths

    def compose(self):
        with VerticalScroll():
            for p in self.paths:
                yield Label("[$primary][b]%s[/b][/]" % p)
                with VerticalGroup() as v:
                    state = self.state_of_path(p)
                    v.styles.padding = [0, 0, 0, 2]
                    if state is not None:
                        for i, decomp in enumerate(state.region_decomps):
                            yield Border("Decomp #%d" % (i + 1), decomp_ui(decomp))
                    else:
                        yield Static("[$foreground-muted]Not formalised[/]")
                yield Static("")


class VGsView(VerticalGroup):
    def __init__(self, state_of_path, paths: list[Path], container, *args, **kwargs):
        VerticalGroup.__init__(self, *args, **kwargs)
        self.state_of_path = state_of_path
        self.paths = paths

    def compose(self):
        with VerticalScroll():
            for p in self.paths:
                yield Label("[$primary][b]%s[/b][/]" % p)
                with VerticalGroup() as v:
                    state = self.state_of_path(p)
                    v.styles.padding = [0, 0, 0, 2]
                    if state is not None:
                        for i, vg in enumerate(state.vgs):
                            yield Border("VG #%d" % (i + 1), vg_ui(vg))
                    else:
                        yield Static("[$foreground-muted]Not formalised[/]")
                yield Static("")


class OpaquesView(VerticalGroup):
    def __init__(self, state_of_path, paths: list[Path], container, *args, **kwargs):
        VerticalGroup.__init__(self, *args, **kwargs)
        self.state_of_path = state_of_path
        self.paths = paths

    def compose(self):
        with VerticalScroll():
            for p in self.paths:
                yield Label("[$primary][b]%s[/b][/]" % p)
                with VerticalGroup() as v:
                    v.styles.padding = [0, 0, 0, 1]
                    state = self.state_of_path(p)
                    if state is not None:
                        header, table = opaques_rich(state.opaque_funcs)
                        yield Static(table)
                    else:
                        yield Static(" [$foreground-muted]Not formalised[/]")


class ModelScreen(Screen):
    DEFAULT_CSS = """
        #panes { width: 65% }
        #panes TabPane { padding: 0 1 0 1; }
        Label.subtree-descriptor { color: $accent; margin-bottom: 1; width: 1fr }
        OpaquesView { background: $surface }
        VGsView { background: $surface }
        """

    mmodel = reactive(None)
    last_update = reactive("-never-")
    selected = reactive(None)

    def on_mount(self):
        self.title = "Model View"
        bind(self, "last_update", "mmodel")

    def empty_container(self, id):
        container = self.query_one(id)
        container.remove_children()
        return container

    def watch_mmodel(self, old_mm: MetaModel, new_mm: MetaModel):
        if self.selected and self.selected in new_mm.models:
            self.select_path(self.selected)
        else:
            for id in ['#model_tab', '#opaques_tab', '#decomps_tab', '#vgs_tab']:
                self.empty_container(id).mount(Static("<Nothing selected>"))

    def compose(self):
        yield MyHeader()
        with Horizontal():
            yield TreeViews().data_bind(ModelScreen.mmodel)
            with TabbedContent(id="panes"):
                with TabPane("Model state", id="model_tab"):
                    yield Static("<Nothing selected>")
                with TabPane("Command entry", id="commands_tab"):
                    yield Static("<Nothing selected>")
                with TabPane("Opaque functions", id="opaques_tab"):
                    yield Static("<Nothing selected>")
                with TabPane("Decomposition requests", id="decomps_tab"):
                    yield Static("<Nothing selected>")
                with TabPane("Verification goals", id="vgs_tab"):
                    yield Static("<Nothing selected>")

        yield Footer()

    def watch_selected(self, _, selected):
        maybe(self.select_path, selected)

    def select_path(self, rel_path):
        # fmt: off
        tree = self.query_one(TreeViews).active_tree()
        file_path = None if rel_path == "" else tree.path_of_node(rel_path)
        children = tree.get_descendants(rel_path)
        paths = filter(not_none, [file_path, *map(tree.path_of_node, children)])
        descriptor = ("All modules" if rel_path == "" else
                      { "src-tree":   (f"Just the module [b]{rel_path}[/b]" if file_path else
                                       f"Modules in directory [b]{rel_path}[/b]:")
                      , "rev-deps":    f"Modules [b]{rel_path}[/b] and its dependents:"
                      , "module-deps": f"Module [b]{rel_path}[/b] and its dependencies:"
                      }[tree.id])

        def state_of_path(p):
            return self.mmodel.models[p].agent_state

        def update_(id, mk_view):
            container = self.empty_container(id)
            container.mount(Label(descriptor, classes="subtree-descriptor"))
            container.mount(mk_view(state_of_path, paths, self))
        # fmt: on

        model = self.mmodel.models.get(rel_path)
        if model: # and model.src_code:
            container = self.empty_container("#model_tab")
            container.mount(ModelView(model, self))

        container = self.empty_container("#commands_tab")
        container.mount(ModelCommandsView(model, self))

        update_("#opaques_tab", OpaquesView)
        update_("#decomps_tab", DecompsView)
        update_("#vgs_tab", VGsView)

    def on_tree_node_selected(self, event):
        self.selected = maybe_else("", fst, event.node.data)

    @on(Button.Pressed, "#send_commands")
    def add_model_commands(self, event):
        """ Add commands to the model """
        pass
