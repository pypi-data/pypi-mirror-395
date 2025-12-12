# ruff: noqa: E501, RUF012, PTH119
#
#   Imandra Inc.
#
#   tree_views.py
#
import os.path
from typing import Generic, TypeVar

from rich.style import Style
from rich.text import Text
from textual import on
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import TabbedContent, TabPane, Tree
from textual.widgets.tree import TreeNode

from ..util import fst, maybe, maybe_else, mdict, snd
from ..strategy.metamodel import MetaModel

TOGGLE_STYLE = Style.from_meta({"toggle": True})
T = TypeVar("T")

ok, unk, inad = "●", "○", "●" # "⨂", "✓", "-", "x"
status_indicators = {
    "unknown": (unk, "dim"),
    "transparent": (ok, "light_green"),
    "inadmissible": (inad, "bright_red"),
    "admitted_with_opaqueness": (ok, "bright_cyan"),
    "executable_with_approximation": (ok, "bright_yellow"),
    "in_progress": ("*", "blink bold bright_white"),
}


class GraphView(Tree):
    class MoveRequest(Generic[T], Message):
        def __init__(self, node: TreeNode[T]) -> None:
            self.node: TreeNode[T] = node
            super().__init__()

    # fmt: off
    def __init__(
        self, root_label, id, node_info, get_successors, get_descendants, level1, prev_views
    ):
        Tree.__init__(self, root_label, id=id)
        node_by_path = {}
        prev_view = prev_views.get(id)
        prev_root = maybe(lambda t: t.root, prev_view)
        prev_selected_src_node = maybe(lambda t:maybe(lambda n: maybe(fst, n.data), t.cursor_node), prev_view)

        def add_children(prev_node, node, xs):
            def node_sort_key(node): return fst(fst(node_info(node)))
            def node_children_by_label(node):
                return {fst(n.data): n for n in node.children if n.data is not None}
            prev_children = maybe_else({}, node_children_by_label, prev_node)
            for x in sorted(xs, key=node_sort_key):
                add_subtree(prev_children, node, x)

        def add_subtree(prev_children, dest, src_node):
            successors = get_successors(src_node)
            (label, get_fresult), path = node_info(src_node)
            add_node = dest.add_leaf if successors == [] else dest.add
            node = add_node(label, data=(src_node, get_fresult))
            prev_node = prev_children.get(src_node)
            if prev_node is not None and prev_node.is_expanded:
                node.expand()
            if path:
                node_by_path[path] = node

            add_children(prev_node, node, successors)
            if prev_selected_src_node == src_node:
                self.post_message(GraphView.MoveRequest(node))

        self.path_of_node = lambda n: snd(node_info(n))
        self.node_by_path = node_by_path
        self.get_descendants = get_descendants
        self.root.expand()
        add_children(prev_root, self.root, level1)

    def render_label(self, node, base_style, style):
        # if self.mmodel is None:
        #     return Text()
        node_label = node._label.copy()
        node_label.stylize(style)
        def indicator_of_st(status):
            return status_indicators.get(status, ("?", "red"))
        def text(sym_col): return Text(fst(sym_col) + " ", snd(sym_col))
        def toggled_icon():
            icon = self.ICON_NODE_EXPANDED if node.is_expanded else self.ICON_NODE
            return icon, base_style + TOGGLE_STYLE

        sym_col = maybe(lambda d: maybe(indicator_of_st, snd(d)()), node.data)
        prefix = toggled_icon() if node._allow_expand else ("", base_style)
        return Text.assemble(prefix, maybe_else(Text(""), text, sym_col), node_label)
    # fmt: off

    @on(MoveRequest)
    def move_to(self, event):
        self.move_cursor(event.node)

        # if fullpath in self.mmodel.models:
        #     model = self.mmodel.models[fullpath]
        # else:
        #     model = None


def fs_graph(metamodel):
    import os.path

    def nodes_of_path(is_file, path):
        yield path, is_file
        if path != "":
            yield from nodes_of_path(False, os.path.dirname(path))

    def edges_of_path(path):
        if path != "":
            parent = os.path.dirname(path)
            yield parent, path
            yield from edges_of_path(parent)

    paths = list(metamodel.models.keys())
    nodes = {n: is_file for p in paths for n, is_file in nodes_of_path(True, p)}
    edges = {e for p in paths for e in edges_of_path(p)}

    succ = mdict(edges)
    return nodes, lambda n: succ.get(n, [])


def dep_graph(metamodel):
    from codelogician.util import consult_or, distrib, map, map_values, swap

    def module_deps(m):
        return [mm.rel_path for mm in m.dependencies]

    deps = map_values(module_deps, metamodel.models)
    preds = mdict(map(swap, distrib(deps.items())))
    inits = [n for n, _ in deps.items() if not preds.get(n)]
    terms = [n for n, succs in deps.items() if not succs]
    succ = consult_or([], {'': inits, **deps})
    pred = consult_or([], {'': terms, **preds})
    return inits, terms, succ, pred


class TreeViews(Container):
    IDS = {"src-tree", "module-deps", "rev-deps"}
    DEFAULT_CSS = "TreeViews { width: 35% }"
    mmodel = reactive(MetaModel(src_dir_abs_path="<not set>", models={}))

    def __init__(self):
        self.prev_view = None
        Container.__init__(self)

    def active_tree(self):
        return self.query_one("#tree-views").active_pane.query_one(GraphView)

    def watch_mmodel(self, old, new):
        self.call_next(self.diff_recompose, old, new)

    async def diff_recompose(self, _old, new):
        from textual.compose import compose
        # return await self.recompose()
        async with self.batch():
            graph_views = {w.id: w for w in self.query(GraphView)}
            children = self.query_children("*").exclude(".-textual-system")
            try:
                prev_view = self.query_one(TabbedContent).active, graph_views
            except:
                prev_view = None
            await children.remove()
            if self.is_attached:
                self.prev_view = prev_view
                await self.mount_all(compose(self))
                self.prev_view = None

    def compose(self):
        if self.mmodel is not None:
            fs_nodes, fs_succs = fs_graph(self.mmodel)
            dg_inits, dg_terms, dg_succs, dg_preds =  dep_graph(self.mmodel)
            model_by_path = self.mmodel.models
            prev_active_id, prev_views = ("", {}) if self.prev_view is None else self.prev_view

            def result_of_path(path):
                status = model_by_path[path].status()
                return "in_progress" if status.outstanding_task_ID else status.formalization_status.value

            # transitive closure
            def tc(f):
                def g(x): return {z for y in f(x) for z in [y, *g(y)]}
                return g

            # fmt: off
            def fs_node_info(rel_path):
                path = rel_path if fs_nodes[rel_path] else None
                return (os.path.basename(rel_path), lambda: maybe(result_of_path, path)), path

            def dg_node_info(rel_path):
                return (rel_path, lambda: result_of_path(rel_path)), rel_path

            with TabbedContent(id="tree-views", initial=prev_active_id):
                with TabPane("Source tree"):
                    root = os.path.basename(self.mmodel.src_dir_abs_path)
                    yield GraphView(root, "src-tree", fs_node_info, fs_succs, tc(fs_succs), fs_succs(""), prev_views)
                with TabPane("Module deps"):
                    yield GraphView("⊤", "module-deps", dg_node_info, dg_succs, tc(dg_succs), dg_inits, prev_views) # noqa: RUF001
                with TabPane("Rev deps"):
                    yield GraphView("⊥", "rev-deps", dg_node_info, dg_preds, tc(dg_preds), dg_terms, prev_views)
            # fmt: on

    def on_tree_node_selected(self, event):
        def select_path(rel_path):
            def expand_and_select(node):
                def expand_up(n):
                    n.expand()
                    maybe(expand_up, n.parent)

                maybe(expand_up, node.parent)
                other.post_message(GraphView.MoveRequest(node))

            for other_id in self.IDS - {event.control.id}:
                other = self.query_one("#" + other_id)
                maybe(expand_and_select, other.node_by_path.get(rel_path))

        def select_node(node_data):
            maybe(select_path, event.control.path_of_node(fst(node_data)))

        maybe(select_node, event.node.data)
