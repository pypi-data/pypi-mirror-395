from typing import Any
from textual.widgets import Tree
from textual.widgets.tree import TreeNode


def find_first_match(node: TreeNode[Any], query: str) -> TreeNode[Any] | None:
    """Depth-first search for partial label match."""
    if query in node.label.plain.lower():
        return node
    for child in node.children:
        match = find_first_match(child, query)
        if match:
            return match
    return None


def focus_node(tree: Tree, node: TreeNode[Any]) -> None:
        """Expand path and set cursor."""
        current = node
        while current.parent and not current.parent.is_expanded:
            current.parent.expand()
            current = current.parent
        tree.move_cursor(node)
        if not node.allow_expand:
            tree.move_cursor(node)
        else:
            node.expand()
