"""Verify the TOTP implementation against the RFC 6238 Appendix B vectors."""

import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from submit import build_auth_header, generate_totp  # noqa: E402

SEED_SHA1 = b"12345678901234567890"
SEED_SHA256 = b"12345678901234567890123456789012"
SEED_SHA512 = b"1234567890" * 6 + b"1234"  # 64 bytes (per RFC errata)


@pytest.mark.parametrize("t, sha1, sha256, sha512", [
    (59, "94287082", "46119246", "90693936"),
    (1111111109, "07081804", "68084774", "25091201"),
    (1111111111, "14050471", "67062674", "99943326"),
    (1234567890, "89005924", "91819424", "93441116"),
    (2000000000, "69279037", "90698825", "38618901"),
    (20000000000, "65353130", "77737706", "47863826"),
])
def test_rfc6238_vectors(t, sha1, sha256, sha512):
    assert generate_totp(SEED_SHA1, t, digits=8, digest=hashlib.sha1) == sha1
    assert generate_totp(SEED_SHA256, t, digits=8,
                         digest=hashlib.sha256) == sha256
    assert generate_totp(SEED_SHA512, t, digits=8,
                         digest=hashlib.sha512) == sha512


def test_ten_digit_output_is_zero_padded():
    code = generate_totp(b"ninja@example.comHENNGECHALLENGE004", 59)
    assert len(code) == 10 and code.isdigit()


def test_auth_header_matches_sample():
    # From the challenge's sample request.
    assert build_auth_header("ninja@example.com", "1595942560") == \
        "Basic bmluamFAZXhhbXBsZS5jb206MTU5NTk0MjU2MA=="
