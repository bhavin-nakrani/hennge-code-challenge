import subprocess
import sys
from pathlib import Path

import pytest

MAIN = Path(__file__).resolve().parent.parent / "main.py"


def run(stdin_text):
    result = subprocess.run(
        [sys.executable, str(MAIN)],
        input=stdin_text.encode(), capture_output=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr.decode()
    return result.stdout.decode().replace("\r\n", "\n")


@pytest.mark.parametrize("stdin_text, expected", [
    # Sample from the challenge
    ("2\n4\n3 -1 1 10\n5\n9 -5 -5 -10 10\n", "1\n11250\n"),
    # Count mismatch -> -1 (too few and too many)
    ("2\n3\n-1 -2\n1\n-1 -2\n", "-1\n-1\n"),
    # Zero and all-positive inputs
    ("2\n3\n0 0 0\n2\n5 7\n", "0\n0\n"),
    # Boundary value -100 (result stays inside int32 as the spec guarantees)
    ("1\n2\n-100 -100\n", "200000000\n"),
    # Windows line endings and extra spaces
    ("1\r\n3\r\n -2  -3 4 \r\n", "97\n"),
])
def test_cases(stdin_text, expected):
    assert run(stdin_text) == expected


def test_reads_exactly_n_cases_ignoring_trailing_input():
    # Extra lines after the last case must not be consumed or affect output.
    assert run("1\n1\n-2\n99\n1 2 3\n") == "16\n"


def test_source_has_no_loops_or_comprehensions():
    import ast
    tree = ast.parse(MAIN.read_text(encoding="utf-8"))
    banned = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp,
              ast.DictComp, ast.GeneratorExp)
    offenders = [type(n).__name__ for n in ast.walk(tree)
                 if isinstance(n, banned)]
    assert offenders == []


def test_no_global_variables():
    import ast
    tree = ast.parse(MAIN.read_text(encoding="utf-8"))
    assigns = [n for n in tree.body
               if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign))]
    assert assigns == []
