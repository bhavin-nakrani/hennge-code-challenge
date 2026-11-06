"""HENNGE Challenge - Python.

Reads N test cases from standard input. Each test case is a line with an
integer X followed by a line with X space-separated integers Yn. For every
test case the program prints the sum of Yn ** 4 over all non-positive Yn,
or -1 when the number of integers does not match X.

Constraints:
  * no global variables
  * no for / while loops and no list / set / dict comprehensions
  * no output until all input has been read
  * input is read line by line (there is no EOF)
"""

import sys


def read_line(stream):
    """Read one line, stripping whitespace and a stray UTF-8 BOM."""
    return stream.readline().lstrip("﻿").strip()


def read_int(stream):
    """Read the next non-blank line as an integer.

    Blank lines (e.g. from stray CR/LF) are skipped. At real EOF readline()
    returns "" and int("") raises, so this can never recurse forever.
    """
    raw = stream.readline()
    text = raw.lstrip("﻿").strip()
    if not text and raw:
        return read_int(stream)
    return int(text)


def sum_of_fourth_powers(numbers):
    """Return the sum of y ** 4 for every non-positive y in numbers."""
    return sum(map(lambda y: y ** 4, filter(lambda y: y <= 0, numbers)))


def solve_case(expected_count, tokens):
    """Solve a single test case, returning -1 if the count does not match."""
    if len(tokens) != expected_count:
        return -1
    return sum_of_fourth_powers(map(int, tokens))


def read_cases(stream, remaining, results):
    """Recursively read `remaining` test cases and collect their results."""
    if remaining <= 0:
        return results
    expected_count = read_int(stream)
    tokens = read_line(stream).split()
    return read_cases(
        stream, remaining - 1, results + [solve_case(expected_count, tokens)]
    )


def main():
    case_count = read_int(sys.stdin)
    results = read_cases(sys.stdin, case_count, [])
    sys.stdout.write("\n".join(map(str, results)) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
