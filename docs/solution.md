# How `main.py` works (Mission 1)

## The problem

```
N                   number of test cases (1..100)
X                   number of integers expected (1..100)
Y1 Y2 ... Yx        integers in -100..100
... repeated N times
```

For each test case, print the sum of `Y ** 4` over every `Y` that is
**not positive** (so `Y <= 0`). If the line does not contain exactly `X`
integers, print `-1` for that case.

Sample: `3 -1 1 10` → only `-1` counts → `(-1)^4 = 1`.
`9 -5 -5 -10 10` → `625 + 625 + 10000 = 11250`.

## Rules and how each one is met

| Rule | How it is met |
|------|---------------|
| No `for` / `while` loops | Test cases are read with **recursion** (`read_cases`). |
| No list/set/dict comprehensions | Values are processed with `map`, `filter` and `sum`. |
| No global variables | Module level holds only `import sys` and function definitions. All state is passed as arguments. |
| Standard library only | Only `sys` is imported. |
| No output until all input is read | Results are collected in a list and printed once at the end. |
| No blank lines between answers | Output is `"\n".join(results)`. |
| No EOF | Reads exactly the lines it needs with `readline()` instead of `sys.stdin.read()`, which would wait for an EOF that never comes. |
| Single file with `main()` | Yes, guarded by `if __name__ == "__main__":`. |

## Walkthrough

```python
def sum_of_fourth_powers(numbers):
    return sum(map(lambda y: y ** 4, filter(lambda y: y <= 0, numbers)))
```
`filter` keeps the non-positive numbers, `map` raises each one to the fourth
power, and `sum` adds them up. These are lazy iterators, so no intermediate
list is built and no comprehension is needed.

```python
def solve_case(expected_count, tokens):
    if len(tokens) != expected_count:
        return -1
    return sum_of_fourth_powers(map(int, tokens))
```
The count check runs on the raw tokens first, so a mismatch returns `-1`.

```python
def read_cases(stream, remaining, results):
    if remaining <= 0:
        return results
    expected_count = read_int(stream)
    tokens = read_line(stream).split()
    return read_cases(stream, remaining - 1,
                      results + [solve_case(expected_count, tokens)])
```
This replaces the `for` loop. Each call reads one test case and recurses with
one fewer remaining. `N <= 100`, so the depth stays well below Python's
default limit of 1000.

`main()` reads `N`, calls `read_cases`, then writes all results at once.

## Robustness details

- `read_int` skips blank lines before `N` and `X`, and strips a UTF-8 BOM.
  These can appear when input is piped from Windows tools. At a real EOF,
  `readline()` returns `""` and `int("")` raises, so it cannot recurse forever.
- `split()` without arguments tolerates multiple spaces, tabs and `\r`.
- Zero counts as "not positive", but `0 ** 4 == 0`, so it does not change the sum.

## Complexity

O(total number of integers) time. Memory is O(X) per line plus O(N) for the results.
