import ast

from .dunder_all import get_meta_class, inspect_class


class Plugin:
    name = "flake8-stash"
    version = "0.11.0"

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        classes_with_meta = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, ast.ClassDef) and get_meta_class(node)
        ]
        for class_def in classes_with_meta:
            node, issue = inspect_class(class_def)
            if node and issue:
                msg = f"{issue.code}: {issue.msg}"
                yield node.lineno, node.col_offset, msg, type(self)
