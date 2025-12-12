#
#   Imandra Inc.
#
#   decomps.py
#

from pathlib import Path
from typing import Dict
from rich.text import Text
from textual import on, work
from textual.app import events
from textual.containers import (
    HorizontalGroup,
    ScrollableContainer,
    VerticalGroup,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Placeholder,
    Footer,
    Rule,
    Button,
    Label,
    Static,
    Pretty
)

from ..common import Border, MyHeader, decomp_ui, opaques_rich, bind
from ..step_view import StepView
from ..tree_views import TreeViews

from codelogician.strategy.model import Model
from codelogician.strategy.metamodel import MetaModel, MetaModelUtils
from codelogician.strategy.state import StrategyState


class DecompsScreen(Screen):
    """ """

    mmodel = reactive(None, recompose=True)

    def on_mount(self):
        self.title = "Region Decompositions"
        bind(self, "mmodel")

    # def watch_mmodel(self, old_value: MetaModel, new_value: MetaModel):
    #     """ """
    #     pass

    def compose (self):
        """ """

        yield MyHeader()
        with VerticalScroll():
            if self.mmodel:
                for idx, (path, model) in enumerate(self.mmodel.models.items()):
                    yield Rule()
                    yield Label("[$primary][b]%s[/b][/]" % path)
                    with HorizontalGroup():
                        yield Button("View model", id=f"btn_{idx}_view_model")
                        with VerticalGroup() as v:
                            v.styles.padding = [0, 0, 0, 1]
                            for decomp in model.decomps():
                                yield Rule()
                                yield decomp_ui(decomp)

        yield Footer()

if __name__ == '__main__':
    pass
