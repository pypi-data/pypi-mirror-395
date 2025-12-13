from typing import Any
from textual.widgets.tree import TreeNode


def build_tree(node: TreeNode, data: Any, new: dict = {}, deleted: list = []) -> TreeNode:
        """Recursively adds JSON data to the tree."""
        # DICT
        if isinstance(data, dict):
            for key, value in data.items():
                modif = ""
                if isinstance(value, (dict, list)):
                    branch = node.add(f"[bold blue{modif}]{key}[/]", expand=False)
                    build_tree(branch, value)
                else:
                    node.add_leaf(f"[blue{modif}]{key}:[/] [green]{value!r}[/]")
        # LIST
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    branch = node.add(f"[bold magenta]Item {index}[/]", expand=False)
                    build_tree(branch, item)
                else:
                    node.add_leaf(f"[magenta][{index}]:[/] [green]{item!r}[/]")
        # LEAFS:
        else:
            # Fallback for root level primitives
            node.add_leaf(f"[green]{data!r}[/]")
        return node