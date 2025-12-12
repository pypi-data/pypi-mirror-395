import ast
from typing import Optional, Tuple

from .issues import Base, Issue, get_dunder_all_issue


def get_meta_class(class_def: ast.ClassDef) -> ast.ClassDef:
    for node in reversed(class_def.body):
        # this ignores the fact that class body can have arbitrary python code
        # For example, the `Meta` can be placed inside an `if` statement
        if isinstance(node, ast.ClassDef) and node.name == "Meta":
            return node


def inspect_class(
    class_def: ast.ClassDef,
) -> Tuple[Optional[ast.Assign], Optional[Issue]]:
    meta = get_meta_class(class_def)
    if all_fields_node := get_all_fields_node(meta):
        base = get_base(class_def)
        return all_fields_node, get_dunder_all_issue("fields", base)
    elif exclude_node := get_exclude_node(meta):
        base = get_base(class_def)
        return exclude_node, get_dunder_all_issue("exclude", base)
    else:
        return None, None


def get_base(class_def: ast.ClassDef) -> Base:
    for base in ["ModelForm", "ModelSerializer", "FilterSet"]:
        if is_subclass_of(class_def, base):
            return base


def is_subclass_of(class_def: ast.ClassDef, parent: str) -> bool:
    return any(
        (isinstance(base, ast.Name) and base.id == parent)
        or (isinstance(base, ast.Attribute) and base.attr == parent)
        for base in class_def.bases
    )


def get_exclude_node(meta: ast.ClassDef) -> Optional[ast.Assign]:
    """
    check if the Meta class defines an exclude attribute.
    Ignoring that Meta can have arbitrary python code i.e. exclude can
    be nested under an if statement
    """
    assign_stmts = [node for node in meta.body if isinstance(node, ast.Assign)]
    exclude_nodes = [
        target
        for assign_stmt in assign_stmts
        for target in assign_stmt.targets
        if getattr(target, "id", None) == "exclude"
    ]
    # return the last one since that's the one in effect
    return exclude_nodes[-1] if exclude_nodes else None


def get_all_fields_node(meta: ast.ClassDef) -> Optional[ast.Assign]:
    """
    check if the Meta class defines fields attribute and its value is either
    the string "__all__" or the python variable ALL_FIELDS.
    Ignoring that Meta can have arbitrary python code i.e. fields can
    be nested under an if statement
    """
    fields_stmts = [
        node
        for node in meta.body
        if isinstance(node, ast.Assign)
        and any(getattr(target, "id", None) == "fields" for target in node.targets)
    ]
    # return the last one since that's the one in effect
    for fields_stmt in reversed(fields_stmts):
        is_dunder_all_str = (
            isinstance(fields_stmt.value, ast.Constant)
            and fields_stmt.value.value == "__all__"
        )
        is_dunder_all_var = (
            isinstance(fields_stmt.value, ast.Name)
            and fields_stmt.value.id == "ALL_FIELDS"
            or isinstance(fields_stmt.value, ast.Attribute)
            and fields_stmt.value.attr == "ALL_FIELDS"
        )
        if is_dunder_all_str or is_dunder_all_var:
            return fields_stmt
