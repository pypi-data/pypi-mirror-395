import os
import json
import base64
import datetime as dt
from typing import Optional

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_DEFAULT = "llm7"


def _derive_key(secret_key: str, salt: Optional[str] = None) -> bytes:
    salt_bytes = (salt or SALT_DEFAULT).encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100_000,
        backend=default_backend(),
    )
    return kdf.derive(secret_key.encode("utf-8"))


def _parse_iso8601_utc(s: str) -> dt.datetime:
    # Accept "2026-01-01T00:00:00Z" and offset forms; default to UTC if naive.
    if s.endswith("Z"):
        s = s.replace("Z", "+00:00")
    d = dt.datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def decode_token(token: str) -> Optional[dict]:
    """Return decrypted JSON payload (dict) or None on failure."""
    try:
        secret_key = os.environ["LLM7_SECRET_KEY"]  # must match Worker secret used for encryption
        salt = os.getenv("LLM7_SALT", SALT_DEFAULT)
        key = _derive_key(secret_key, salt)

        raw = base64.b64decode(token)
        iv, data = raw[:12], raw[12:]  # data = ciphertext||tag (AESGCM expects both)
        payload_bytes = AESGCM(key).decrypt(iv, data, None)
        return json.loads(payload_bytes.decode("utf-8"))
    except Exception as e:
        print(f"Token decode error: {e}")
        return None


def is_token_valid(token: str) -> bool:
    try:
        data = decode_token(token)
        if not data or "expiresAt" not in data:
            return False
        expiry = _parse_iso8601_utc(str(data["expiresAt"]))
        now = dt.datetime.now(dt.timezone.utc)
        return now < expiry
    except Exception:
        return False


def extract_sub(token: str) -> Optional[str]:
    try:
        data = decode_token(token)
        if not data or "sub" not in data:
            return None
        return str(data["sub"])
    except Exception:
        return None


def extract_email(token: str) -> Optional[str]:
    try:
        data = decode_token(token)
        if not data or "email" not in data:
            return None
        return str(data["email"])
    except Exception:
        return None


def introspect_token(token: str) -> Optional[dict]:
    """Call `/tokens/introspect` for a token and return the parsed JSON result."""
    try:
        base_url = os.environ["LLM7_TOKEN_URL"].rstrip("/")
        url = f"{base_url}/tokens/introspect"
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            json={"token": token},  # include in body as a fallback
            timeout=5,
        )
        return resp.json()
    except Exception as e:
        print(f"Token introspection error: {e}")
        return None


def token_exists(token: str) -> bool:
    try:
        base_url = os.environ["LLM7_TOKEN_URL"].rstrip("/")
        # Prefer a dedicated admin key; fall back to legacy secret for compatibility.
        admin_key = os.getenv("LLM7_ADMIN_API_KEY") or os.environ["LLM7_SECRET_KEY"]
        url = f"{base_url}/token_exists"
        headers = {"Authorization": f"Bearer {admin_key}"}
        resp = requests.post(url, headers=headers, json={"token": token}, timeout=5)
        return resp.status_code == 200 and resp.json() is True
    except Exception:
        return False


def record_usage(
    email: str, token_value: str, model: str, tokens_in: int, tokens_out: int
) -> bool:
    try:
        base_url = os.environ["LLM7_TOKEN_URL"].rstrip("/")
        admin_key = os.getenv("LLM7_ADMIN_API_KEY") or os.environ["LLM7_SECRET_KEY"]
        url = f"{base_url}/admin/stats"
        headers = {"Authorization": f"Bearer {admin_key}"}
        payload = {
            "email": email,
            "token_value": token_value,
            "model": model,
            "tokens_in": int(tokens_in),
            "tokens_out": int(tokens_out),
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=5)
        return resp.status_code == 201
    except Exception:
        return False
