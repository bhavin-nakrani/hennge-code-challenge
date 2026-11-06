# Submission Guide

Before you start, read the challenge rules once more. Submit **only `main.py`**,
use a **secret** gist, and send the POST yourself.

## Checklist

- [ ] `python -m pytest -q` passes
- [ ] The sample input prints `1` and `11250`
- [ ] Python 3.13+ is installed: `python --version`

---

## Mission 2: Create a secret gist

### Option A: Website (easiest)

1. Sign in to GitHub and open <https://gist.github.com/>.
2. Leave **"Gist description"** blank or enter something neutral.
3. Set **"Filename including extension"** to exactly `main.py`.
4. Paste the entire contents of `main.py`.
5. Open the dropdown on the green button and choose
   **"Create secret gist"**. Do **not** choose "Create public gist".
6. Copy the URL from the address bar. It looks like
   `https://gist.github.com/<your-username>/<gist-id>`.

### Option B: GitHub CLI

```bash
gh auth login                 # once
gh gist create main.py        # gists are SECRET by default; do NOT pass --public
```
The command prints the gist URL.

### Check the gist

- Open the URL in a private/incognito window. You should see the code, and the
  gist should be marked **Secret** and not appear on your public profile.
- It must contain **only one file**, `main.py`.
- Do not edit the gist after you submit.

---

## Mission 3: Send the URL

1. Set up the project if you haven't already (see [README](README.md)):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Fill in `.env`:
   ```
   CONTACT_EMAIL=your.real@email.com
   GIST_URL=https://gist.github.com/<your-username>/<gist-id>
   SOLUTION_LANGUAGE=python
   ```
   Check your email address carefully. HENNGE will contact you there.
3. Preview the request without sending anything:
   ```bash
   python submit.py --dry-run
   ```
4. Send it:
   ```bash
   python submit.py
   ```
5. Expected result:
   ```
   Status: 200
   Response: {"message":"Congratulations! You have achieved mission 3"}
   ```

### Troubleshooting

| Response | Likely cause |
|----------|--------------|
| `401 Unauthorized` | Wrong email, the clock is off by more than about 30 seconds, or the email in the body differs from the auth user. Sync your clock, then retry **once**. |
| `400 Bad Request` | Malformed JSON or wrong field names. Run with `--dry-run` to check the body. |
| Other 4xx | Read the response message. It usually says what is wrong. |

Don't retry in a loop. The rules forbid brute force. Fix the cause, then send again.

### Alternative: curl (if you'd rather not use the script)

Generate the TOTP with the script, then send the request within 30 seconds:
```bash
python -c "from submit import generate_totp; print(generate_totp(b'YOUR_EMAILHENNGECHALLENGE004'))"
curl -u "YOUR_EMAIL:TOTP_HERE" -H "Content-Type: application/json" \
  -d '{"github_url":"GIST_URL","contact_email":"YOUR_EMAIL","solution_language":"python"}' \
  https://api.challenge.hennge.com/challenges/backend-recursion/004
```

---

## After you submit

- Keep the gist secret and unchanged. HENNGE reviews it after Mission 3.
- Do not publish this repository publicly. `.gitignore` already excludes `.env`.
- Be ready to explain `main.py` yourself. [docs/solution.md](docs/solution.md)
  walks through it.
