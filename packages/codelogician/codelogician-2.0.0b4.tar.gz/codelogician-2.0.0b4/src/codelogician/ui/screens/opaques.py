#
#   Imandra Inc.
#
#   screen_opaques.py
#

from pathlib import Path
from typing import Dict

from textual import on, work
from textual.app import events
from textual.reactive import reactive
from textual.containers import (
    HorizontalGroup,
    VerticalGroup,
    VerticalScroll,
)
from textual.screen import Screen
from textual.widgets import (
    Rule,
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

from codelogician.strategy.metamodel import MetaModel, MetaModelUtils
from codelogician.strategy.state import StrategyState

from ..common import Border, MyHeader, opaques_rich, bind
from ..step_view import StepView
from ..tree_views import TreeViews


class OpaquesScreen(Screen):
    """ """

    mmodel = reactive("", recompose=True)

    def on_mount(self):
        self.title = "Opaques"
        bind(self, "mmodel")

    # def watch_mmodel(self, old_value: MetaModel, new_value: MetaModel):
    #     pass

    def compose(self):
        """ """
        yield MyHeader()
        with VerticalScroll():
            # mmodel can still be None - `curr_meta_model` doesn't guarantee anything
            if self.mmodel:
                for model_idx, (path, model) in enumerate(self.mmodel.models.items()):
                    yield Rule()
                    yield Label("[$primary][b]%s[/b][/]" % path)
                    with HorizontalGroup():
                        yield Button("View model", id=f"view_{model_idx}")
                        # yield Rule("vertical")
                        with VerticalGroup():
                            if model.agent_state is not None:
                                _, table = opaques_rich(model.agent_state.opaque_funcs)
                                yield Static(table)
                            else:
                                yield Static(" [$foreground-muted]Not formalised[/]")
        yield Footer()

    def on_button_pressed(self, event:Button.Pressed):
        """ Need to go to the `model` screen and focus on the specific model """
        # TODO Implement this
        pass
