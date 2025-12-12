"""google.py."""

import logging
from typing import Any, Tuple

from fastapi import Request
from google.auth.transport import requests
from google.oauth2 import id_token
from strangeworks_core.errors.error import StrangeworksError
from strangeworks_core.utils import is_empty_str


logger = logging.getLogger()


def verify_token(
    request: Request,
    verify_signature: bool = True,
) -> Tuple[dict[str, Any], str]:
    """Verify Google Cloud service account token.

    Parameters
    ----------
    request: Request
        Incoming HTTP request.

    verify_signature: bool
        verify that the JWT signature. Doing this verifies that the JWT is from a
        trusted user and that it hasn't been tampered with.

    Returns
    -------
    : Tuple[Mapping, str]
    Tuple  wth JWT claims and the token itself.

    Raises
    ------
    StrangeworksError if auth token cannot be verified.
    """

    if not verify_signature:
        # since the claims from gcp service account are currently not used anywhere, if
        # the caller doesn't want to verify, return empty claims
        return {}, "key"

    header_key = "Authorization"
    auth_header = request.headers.get(header_key)
    if is_empty_str(auth_header):
        raise StrangeworksError.authentication_error(
            f"unable to retrieve auth header ({header_key}) from request"
        )

    logger.debug("retrieving auth type and token from {auth_header}")
    # split the auth type and value from the header.
    type, token = auth_header.split(" ", 1)

    if type.lower() != "bearer":
        raise StrangeworksError.authentication_error(f"unhandled auth type: {type}")

    try:
        claims = id_token.verify_token(token, requests.Request())
        logger.debug(f"successfully verified auth token {token}")
        return claims, token
    except BaseException as ex:
        raise StrangeworksError.authentication_error("error verifying token") from ex
