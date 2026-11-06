# HENNGE Backend Challenge (Recursion 004)

A solution to the HENNGE coding challenge, written in Python.

| File | Purpose |
|------|---------|
| `main.py` | **Mission 1.** The only file you submit. Uses the standard library only. |
| `submit.py` | **Mission 3** helper. Generates the TOTP and POSTs your gist URL. |
| `tests/` | Pytest suite for both scripts. |
| `docs/` | How the code works ([solution](docs/solution.md), [TOTP](docs/totp.md)). |
| `submission.md` | Step-by-step guide to the gist and the final submission. |

## Requirements

- Python 3.13 or newer (the grader runs 3.13+)
- Git (optional, for gists via the command line)

## Setup

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env      # then edit .env
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env             # then edit .env
```

`requirements.txt` lists only what `submit.py` and the tests need
(`requests`, `python-dotenv`, `pytest`). **`main.py` has no dependencies.**

## Configuration (`.env`)

| Variable | Description |
|----------|-------------|
| `CONTACT_EMAIL` | Your email address. Used in the JSON body, as the Basic-Auth user ID, and in the TOTP secret. |
| `GIST_URL` | Your secret gist URL, e.g. `https://gist.github.com/you/abc123` |
| `SOLUTION_LANGUAGE` | `python` |
| `CHALLENGE_URL` | The challenge endpoint (already set to the default) |

`.env` is listed in `.gitignore`. Never commit it.

## Run the solution

```bash
python main.py
```
Then type or paste the input. Output appears once all test cases have been read.

```bash
# Run the sample (bash)
printf '2\n4\n3 -1 1 10\n5\n9 -5 -5 -10 10\n' | python main.py
# -> 1
# -> 11250
```

## Run the tests

```bash
python -m pytest -q
```

The tests cover the sample, count mismatches (`-1`), zero and positive values,
CRLF input, and exact line-by-line reading (no EOF). They also include an AST
check that `main.py` has no loops, comprehensions, or global variables, and the
official RFC 6238 test vectors for the TOTP generator.

## Submit

See [submission.md](submission.md).
