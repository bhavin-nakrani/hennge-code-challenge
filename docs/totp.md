# How `submit.py` works (Mission 3)

Mission 3 is an HTTP POST protected by Basic Auth. The password is a TOTP
(RFC 6238) with these non-default settings:

| Parameter | Value |
|-----------|-------|
| Time step X | 30 seconds |
| T0 | 0 (Unix epoch) |
| Hash | **HMAC-SHA-512** (the default is SHA-1) |
| Digits | **10** (the default is 6) |
| Shared secret | `<email>HENNGECHALLENGE004`, as raw ASCII bytes (**not** base32) |

## The algorithm

1. `T = floor((now - T0) / X)`, the number of 30-second steps since the epoch.
2. Pack `T` as an **8-byte big-endian** integer.
3. `HMAC-SHA-512(secret, packed_T)` gives a 64-byte digest.
4. **Dynamic truncation** (RFC 4226 §5.3): `offset = last_byte & 0x0F`. Take
   the 4 bytes at `offset` and clear the top bit (`& 0x7FFFFFFF`).
5. `code = value % 10**10`, zero-padded to 10 digits.

### About the errata

The reference Java code in RFC 6238 contains mistakes that the errata point
out, and a few online generators copy them:

- The SHA-256 and SHA-512 test seeds should be 32 and 64 bytes long. The
  tests in `tests/test_submit.py` use the corrected seeds, and all
  18 official vectors pass.
- The truncation offset must come from the **last** byte of the digest
  (byte 63 for SHA-512), not byte 19 as with SHA-1. The code uses `mac[-1]`.
- The 10-digit modulus `10**10` is larger than the 31-bit truncated value
  (at most 2,147,483,647). The code therefore never overflows, and short
  values are padded with `zfill`.

## The request

```
POST /challenges/backend-recursion/004
Authorization: Basic base64("<email>:<totp>")
Content-Type: application/json

{"github_url":"...","contact_email":"...","solution_language":"python"}
```

A test checks `build_auth_header` against the challenge's sample header.

The TOTP changes every 30 seconds, so the script generates it right before
sending. If you get a 401, check that your computer's clock is accurate.
