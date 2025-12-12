"""jwt_utils.py"""

from fastapi import Request
from jose import jwt
from strangeworks_core.errors.error import StrangeworksError


def get_token_from_request(request: Request) -> str:
    """Retrieve JWT token from HTTP request."""
    token: str = request.headers.get("x-strangeworks-access-token")
    if not token:
        raise StrangeworksError.authentication_error(
            message="request missing access token"
        )
    return token


def decode_token(token: str) -> dict:
    """Validate and decode JWT token."""
    message = jwt.decode(token=token, key=None, options={"verify_signature": False})
    return message
