#
#   Imandra Inc.
#
#   help.py
#

from pathlib import Path
from textual.screen import Screen
from textual.widgets import Footer, MarkdownViewer

from codelogician.doc.utils.docs import flatten_docs, walk_directory
from ..common import MyHeader


class HelpScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.title = "Help"

    def compose(self):
        doc_path = Path(__file__).parent / "../../doc/data"
        text = flatten_docs(walk_directory(doc_path.resolve()))

        yield MyHeader()
        markdown_viewer = MarkdownViewer(text, show_table_of_contents=True)
        markdown_viewer.code_indent_guides = False
        yield markdown_viewer
        yield Footer()
