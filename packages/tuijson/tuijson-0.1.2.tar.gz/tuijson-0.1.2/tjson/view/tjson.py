from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.containers import Horizontal
from jsondiff import diff, delete
from .search_screen import SearchScreen, Search
from ..controller.search import find_first_match, focus_node
from ..controller.build_tree import build_tree


class T_JSON(App):
    """A Textual app to visualize JSON data in a tree structure."""

    CSS = """
    Tree {
        padding: 1;
        scrollbar-gutter: stable;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("e", "expand_all", "Expand Tree"),
        ("d", "expand_both", "Expand Both Trees"),
        ("c", "collapse_all", "Collapse Tree"),
        ("f", "collapse_both", "Collapse Both Trees"),
        ("s", "search", "Search"),
    ]

    def __init__(self,
                 json_data: Any, title: str = "JSON Tree",
                 json_data2: Any = None, title2: str = "JSON Tree"):
        super().__init__()
        self.json_data = json_data
        self.app_title = title
        self.json_data2 = json_data2
        self.app_title2 = title2
        self.current_node = None

    def compose(self) -> ComposeResult:
        yield Header(True, name="TJSON", icon="🌳")
        with Horizontal():
            yield Tree(self.app_title)
            if self.json_data2:
                yield Tree(self.app_title2)
        yield Footer()

    def on_mount(self) -> None:
        """Load the JSON data into the tree when the app starts."""
        # NOTE: Could use "add_json", but "build tree" has a nicer formatting.
        #tree.add_json(self.json_data, tree.root)
        trees = self.query(Tree)
        for tree in trees:
            tree.root.expand()
        json_diff = {}
        if self.json_data2:
            json_diff = diff(self.json_data, self.json_data2)
            deleted = json_diff.pop(delete, {})
            build_tree(trees[0].root, self.json_data, deleted=deleted)
            build_tree(trees[1].root, self.json_data2, new=json_diff)
        else:
            build_tree(trees[0].root, self.json_data)


    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        self.current_node = event.node

    def action_expand_all(self) -> None:
        trees = self.query(Tree)
        for tree in trees:
            if tree.has_focus:
                tree.root.expand_all()

    def action_expand_both(self) -> None:
        trees = self.query(Tree)
        for tree in trees:
            tree.root.expand_all()

    def action_collapse_all(self) -> None:
        trees = self.query(Tree)
        for tree in trees:
            if tree.has_focus:
                tree.root.collapse_all()
                tree.root.expand()

    def action_collapse_both(self) -> None:
        trees = self.query(Tree)
        for tree in trees:
            tree.root.collapse_all()
            tree.root.expand()
    
    def action_search(self) -> None:
        self.push_screen(SearchScreen())
    
    def on_search(self, event: Search) -> None:
        query = event.query
        trees = self.query(Tree)
        for tree in trees:
            if tree.has_focus:
                break
        if self.current_node:
            node = find_first_match(self.current_node, query)
        if not node:
            node = find_first_match(tree.root, query)
        if node:
            focus_node(tree, node)
            self.set_focus(tree)
