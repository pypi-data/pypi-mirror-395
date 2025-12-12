import ast
import pathlib
from typing import List, Tuple

from flake8_stash.plugin import Plugin


def test_model_forms():
    errors = get_results("sample_model_forms.py")
    expected = [
        (15, 8, "STA011"),
        (25, 8, "STA011"),
        (33, 8, "STA012"),
        (39, 8, "STA011"),
        (49, 8, "STA042"),
    ]
    assert errors == expected


def test_model_serializers():
    errors = get_results("sample_model_serializers.py")
    expected = [
        (16, 8, "STA021"),
        (26, 8, "STA021"),
        (34, 8, "STA022"),
        (40, 8, "STA021"),
        (52, 8, "STA041"),
    ]
    assert errors == expected


def test_filtersets():
    errors = get_results("sample_filtersets.py")
    expected = [
        (16, 8, "STA031"),
        (26, 8, "STA031"),
        (34, 8, "STA032"),
        (40, 8, "STA031"),
    ]
    assert errors == expected


def get_results(filename: str) -> List[Tuple[int, int, str]]:
    current_dir = pathlib.Path(__file__).parent.resolve()
    with open(current_dir / filename, encoding="utf8") as f:
        contents = f.read()

    tree = ast.parse(contents)
    plugin = Plugin(tree)
    return [
        # retrieve position of the error and the code only
        (lineno, col_offset, msg.split()[0][:-1])
        for lineno, col_offset, msg, _ in plugin.run()
    ]
