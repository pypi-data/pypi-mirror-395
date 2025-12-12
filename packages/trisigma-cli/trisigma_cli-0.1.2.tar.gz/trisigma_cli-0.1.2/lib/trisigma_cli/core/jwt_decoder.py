"""JWT token decoder utilities."""

from typing import Optional, Tuple

import jwt


def decode_jwt_token(token: str) -> Optional[dict]:
    """
    Decode JWT token without verification.

    Client doesn't have access to the secret key, so we decode without verification.
    This is safe since we only extract user display information.

    Args:
        token: JWT access token

    Returns:
        Decoded token payload or None if decoding fails
    """
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except (jwt.InvalidTokenError, Exception):
        return None


def _extract_login_from_email(email: Optional[str]) -> Optional[str]:
    """
    Extract login (username) from email address.

    Args:
        email: Email address (e.g., "vabozhev@avito.ru")

    Returns:
        Login part before @ symbol (e.g., "vabozhev") or None if email is None
    """
    if not email:
        return None

    return email.split("@")[0] if "@" in email else email


def extract_user_info(token: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract login and email from JWT token.

    Login is extracted from email (part before @).

    Args:
        token: JWT access token

    Returns:
        Tuple of (login, email) or (None, None) if extraction fails
    """
    payload = decode_jwt_token(token)
    if not payload:
        return None, None

    email = payload.get("email")
    login = _extract_login_from_email(email)

    return login, email
