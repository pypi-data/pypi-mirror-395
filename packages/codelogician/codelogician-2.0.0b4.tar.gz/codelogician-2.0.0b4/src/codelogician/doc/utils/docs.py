# ruff: noqa: E741
#
#   Imandra Inc.
#
#   docs.py
#

from pathlib import Path
from typing import Literal

from fuzzysearch import find_near_matches
from pydantic import BaseModel
from rich import print as printr
from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

from codelogician.util import filter, flat_map, fst, map, maybe, snd, splice, text_read


def abbrev(s): return s if len(s) <= 100 else s[:97] + '...'

def maybe_min(items, **kwargs):
    return None if len(items) == 0 else min(items, **kwargs)

class DocFile(BaseModel):
    """
    DocFile contains the information
    """
    title : str
    path : str
    description : str
    order : int
    content: str

    def topic_match(self, t : str) -> int|None:
        """
        Calculate distance between the specified topic and the title
        """

        res1 = find_near_matches(t.lower(), self.title.lower(), max_l_dist=3)
        res2 = find_near_matches(t.lower(), self.path.lower(), max_l_dist=2)
        return maybe_min([x.dist for x in res1 + res2])

    def __rich__ (self):
        """
        Return a nice representation
        """

        return Panel(
                Group(
                    Text(f'Name: {self.title}'),
                    Text(f'Path: {Path(self.path).name}'),
                    Text(f'Description: {self.description}'),
                    Text('Content:'),
                    Markdown(self.content))
        )

    @staticmethod
    def get_lines_by_char_range(
        text : str,
        start_char_index : int,
        end_char_index : int
        ):
        """
        Retrieves all lines from a given text that contain characters within
        the specified start and end character indexes.

        Args:
            text (str): The input text.
            start_char_index (int): The starting character index (inclusive).
            end_char_index (int): The ending character index (exclusive).

        Returns:
            list: A list of lines that contain characters within the specified range.
        """

        lines = text.splitlines(keepends=True)  # Keep line endings for accurate indexing

        result_lines = []
        current_char_offset = 0

        for line in lines:
            line_start_char = current_char_offset
            line_end_char = current_char_offset + len(line)

            # Check for overlap between the requested range and the line's range
            if (max(start_char_index, line_start_char) < min(end_char_index, line_end_char)):
                result_lines.append(line.strip('\n'))  # Remove newline for clean output

            current_char_offset += len(line)

        return '\n'.join(result_lines)

    def rich_selection(self, start_idx:int, end_idx:int, matched:str):
        """
        Print out the version of the
        """

        selection = self.get_lines_by_char_range(self.content, start_idx, end_idx)
        selection = selection.replace(matched, f'[bold]{matched}[/bold]')

        return Panel(Group(
            Text(f'Name: {self.title}'),
            Text(f'Path: {Path(self.path).name}'),
            Text(f'Matched: {matched}'),
            Text(f'Selected text:\n{selection}'),
        ))


def parse_markdown_or_iml(path: str) -> DocFile:
    """
    Parse the markdown file and return a nice object
    """

    lines = text_read(path).split('\n')
    first: int | None = None
    second: int | None = None
    for i, line in enumerate(lines):
        if first is not None and second is not None:
            # Found two delimiter
            break
        line_trimmed = line.strip()
        if all(c == '-' for c in list(line_trimmed)) and len(line_trimmed) >= 3:
            if first is None:
                first = i
            elif second is None:
                second = i
    if first is None or second is None:
        raise Exception(f'No frontmatter found in documentation {path}')

    pairs = [l.split(':') for l in lines[first + 1 : second] if ':' in l]
    data = {k.strip().lower(): v for k, v in pairs}

    return DocFile(
        title=data['title'],
        order=int(data['order']),
        path=path,
        description=data['description'],
        content='\n'.join([*lines[: first - 1], *lines[second + 1 :]])
        if len(lines) > second + 1
        else '',
    )

type Leaf = tuple[Literal['leaf'], tuple[str, DocFile]]
type Branch = tuple[Literal['branch'], tuple[tuple[str, DocFile], list[Node]]]
type Node = Leaf | Branch

def walk_directory(directory: Path) -> list[Node]:
    """
    Returns a tree, consisting of a list of nodes.
    Each `node` is either `('leaf', (str, DocFile))`, or
    or `('branch', ((str, DocFile), list[node]))`.
    """
    def maybe_parse(p: Path) -> DocFile | None:
        try: return parse_markdown_or_iml(str(p))
        except Exception: return None

    def path_entry(p: Path):
        is_file = p.is_file()
        md = (maybe_parse(p / '_index.md') if not is_file else
              maybe_parse(p) if (p.suffix == '.md' and p.name != '_index.md') or p.suffix == '.iml'
              else None)
        # Sort dirs first then order then filename
        return [] if md is None else [((is_file, md.order, p.name.lower()), (p, md))]

    def node(entry):
        (is_file, _, _), (path, md) = entry
        return (('leaf', (path, md)) if is_file else
                ('branch', ((path, md), sub_nodes(path))))

    def sub_nodes(path):
        return map(node, sorted(flat_map(path_entry, path.iterdir()), key=fst))

    return sub_nodes(Path(directory))


def leaves(nodes):
    def aux(kind, data): return [snd(data)] if kind == 'leaf' else leaves(snd(data))
    return flat_map(splice(aux), nodes)


def flatten_docs(nodes: list[Node]) -> str:
    def do_nodes(l, nodes):
        hd = '#' * l
        def fmt(_, doc): return f'{hd} {doc.title}\n{doc.content}'
        def do_leaf(data):          return [fmt(*data)]
        def do_branch(data, nodes): return [fmt(*data), *do_nodes(l+1, nodes)]
        def do_node(kind, data):
            return (do_leaf if kind == 'leaf' else splice(do_branch))(data)
        return flat_map(splice(do_node), nodes)

    return '\n\n'.join(do_nodes(1, nodes))


def doc_tree(nodes) -> Tree:
    def dir_node(path, doc):
        label = f'[bold magenta]:open_file_folder: {abbrev(doc.description)}'
        return label, ('dim' if path.name.startswith('__') else '')

    def file_label(path, doc):
        text_filename = Text(path.name, 'green')
        text_filename.highlight_regex(r'\..*$', 'bold red')
        text_filename.stylize(f'link file://{path}')
        text_filename.append(f' {abbrev(doc.description)}', 'blue')
        icon = '🐍 ' if path.suffix == '.py' else '📝 ' if path.suffix == '.iml' else '📄 '
        return Text(icon) + text_filename

    def add_nodes(nodes, tree):
        def add_leaf(data): tree.add(file_label(*data))
        def add_branch(data, nodes):
            text, style = dir_node(*data)
            add_nodes(nodes, tree.add(text, style=style, guide_style=style))

        for kind, data in nodes:
            {'leaf': add_leaf, 'branch': splice(add_branch)}[kind](data)

    tree = Tree('Documentation details', guide_style='bold bright_blue')
    add_nodes(nodes, tree)
    return tree


class DocManager:
    """
    Documentation Manager helper
    """
    def __init__ (self, dir:str):
        nodes = walk_directory(Path(dir))
        self.doc_files = leaves(nodes)
        self.tree = doc_tree(nodes)

    def files(self) -> list[DocFile]:
        return self.doc_files

    def find_content(self, query: str, max_hits: int = 5) -> list[DocFile]:
        def doc_matches(d):
            return ([] if len(d.content) == 0 else
                    [(r, d) for r in find_near_matches(query, d.content, max_l_dist=1)])

        all_matches = flat_map(doc_matches, self.doc_files)
        return [doc.rich_selection(hit.start, hit.end, hit.matched)
                for hit, doc in sorted(all_matches, key=lambda x: fst(x).dist)[:max_hits]]

    def find_topic(self, topic:str, dist_cutoff:float = 5.0) -> DocFile | None:
        """
        Find DocFile for a specific topic (if possible)
        """
        topic = topic.replace('.md', '')

        def below_cutoff(dd): return fst(dd) is not None and fst(dd) <= dist_cutoff
        candidates = [(d.topic_match(topic), d) for d in self.doc_files]
        return maybe(snd, maybe_min(filter(below_cutoff, candidates), key=fst))

    def print_contents(self) -> None:
        """
        Print out the contents in a nice way...
        """

        printr(self.tree)
