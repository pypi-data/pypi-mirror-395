from dataclasses import dataclass
from typing import Literal, Optional

Attr = Literal["fields", "exclude"]
Base = Optional[Literal["ModelForm", "ModelSerializer", "FilterSet"]]


def get_dunder_all_issue(attr: Attr, base: Base = None) -> "Issue":
    mapping = {
        ("fields", "ModelForm"): STA011,
        ("exclude", "ModelForm"): STA012,
        ("fields", "ModelSerializer"): STA021,
        ("exclude", "ModelSerializer"): STA022,
        ("fields", "FilterSet"): STA031,
        ("exclude", "FilterSet"): STA032,
        ("fields", None): STA041,
        ("exclude", None): STA042,
    }
    return mapping[(attr, base)]


@dataclass
class Issue:
    code: str
    msg: str
    attr: Attr
    base: Base = None


STA011 = Issue(
    code="STA011",
    msg="The use of `fields = '__all__'` in model forms is not allowed. List the fields one by one instead.",
    attr="fields",
    base="ModelForm",
)
STA012 = Issue(
    code="STA012",
    msg="The use of `exclude` in model forms is not allowed. Use `fields` instead.",
    attr="exclude",
    base="ModelForm",
)
STA021 = Issue(
    code="STA021",
    msg="The use of `fields = '__all__'` in model serializers is not allowed. List the fields one by one instead.",
    attr="fields",
    base="ModelSerializer",
)
STA022 = Issue(
    code="STA022",
    msg="The use of `exclude` in model serializers is not allowed. Use `fields` instead.",
    attr="exclude",
    base="ModelSerializer",
)
STA031 = Issue(
    code="STA031",
    msg="The use of `fields = '__all__'` in filtersets is not allowed. List the fields one by one instead.",
    attr="fields",
    base="FilterSet",
)
STA032 = Issue(
    code="STA032",
    msg="The use of `exclude` in filtersets is not allowed. Use `fields` instead.",
    attr="exclude",
    base="FilterSet",
)
STA041 = Issue(
    code="STA041",
    msg="The use of `fields = '__all__'` is not allowed. List the fields one by one instead.",
    attr="fields",
)
STA042 = Issue(
    code="STA042",
    msg="The use of `exclude` is not allowed. Use `fields` instead.",
    attr="exclude",
)
