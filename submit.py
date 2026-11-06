"""HENNGE Challenge - Mission 3 helper.

Builds the JSON payload, generates a 10-digit TOTP (RFC 6238, HMAC-SHA-512,
time step 30s, T0 = 0) and POSTs it to the challenge endpoint using HTTP
Basic Authentication.

Settings are read from a .env file (see .env.example).

Usage:
    python submit.py --dry-run   # show payload and headers, send nothing
    python submit.py             # actually submit
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import struct
import sys
import time

import requests
from dotenv import load_dotenv

SECRET_SUFFIX = "HENNGECHALLENGE004"


def generate_totp(secret, for_time=None, time_step=30, t0=0, digits=10,
                  digest=hashlib.sha512):
    """Generate an RFC 6238 TOTP value.

    `secret` is the raw shared secret as bytes (NOT base32-encoded).
    """
    now = time.time() if for_time is None else for_time
    counter = int((now - t0) // time_step)
    message = struct.pack(">Q", counter)  # 8-byte big-endian counter
    mac = hmac.new(secret, message, digest).digest()

    # Dynamic truncation (RFC 4226 section 5.3): use the low 4 bits of the
    # LAST byte of the HMAC as offset (valid for SHA-1, SHA-256 and SHA-512).
    offset = mac[-1] & 0x0F
    binary = struct.unpack(">I", mac[offset:offset + 4])[0] & 0x7FFFFFFF

    return str(binary % (10 ** digits)).zfill(digits)


def build_auth_header(user_id, password):
    token = base64.b64encode(f"{user_id}:{password}".encode("utf-8"))
    return "Basic " + token.decode("ascii")


def load_settings():
    load_dotenv()
    settings = {
        "email": os.getenv("CONTACT_EMAIL", "").strip(),
        "gist_url": os.getenv("GIST_URL", "").strip(),
        "language": os.getenv("SOLUTION_LANGUAGE", "python").strip(),
        "api_url": os.getenv(
            "CHALLENGE_URL",
            "https://api.challenge.hennge.com/challenges/backend-recursion/004",
        ).strip(),
    }
    missing = [key for key in ("email", "gist_url") if not settings[key]]
    if missing:
        sys.exit(f"Missing values in .env: {', '.join(missing)}")
    return settings


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="print the request without sending it")
    args = parser.parse_args()

    settings = load_settings()
    payload = {
        "github_url": settings["gist_url"],
        "contact_email": settings["email"],
        "solution_language": settings["language"],
    }
    secret = (settings["email"] + SECRET_SUFFIX).encode("ascii")
    password = generate_totp(secret)
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Authorization": build_auth_header(settings["email"], password),
    }
    body = json.dumps(payload, separators=(",", ":"))

    print(f"POST {settings['api_url']}")
    print(f"TOTP: {password}")
    print(f"Body: {body}")

    if args.dry_run:
        print("Dry run - nothing sent.")
        return

    response = requests.post(settings["api_url"], data=body,
                             headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
