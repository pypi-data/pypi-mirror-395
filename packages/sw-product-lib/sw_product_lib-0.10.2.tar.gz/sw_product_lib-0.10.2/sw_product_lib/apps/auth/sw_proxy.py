"""sw_proxy.py."""

import logging
from typing import Any, Tuple

from fastapi import Request
from jose import jwt
from strangeworks_core.errors.error import StrangeworksError

from sw_product_lib import cfg


logger = logging.getLogger(__name__)


def verify_token(
    request: Request, verify_signature: bool = True
) -> Tuple[dict[str, Any], str]:
    """Verify Strangeworks platform proxy token.

    Parameters
    ----------
    request: Request
        Incoming HTTP request.

    verify_signature: bool
        verify that the JWT signature. Doing this verifies that the JWT is from a
        trusted user and that it hasn't been tampered with.

    Returns
    -------
    : Tuple[Mapping, token]
    Tuple  wth JWT claims and the token itself.

    Raises
    ------
    StrangeworksError if auth token cannot be verified.
    """
    logger.debug("Verifying sw platform product auth token")
    header_key = "x-strangeworks-access-token"
    token = request.headers.get(header_key)
    if not token:
        raise StrangeworksError.authentication_error(
            f"unable to retrieve auth header ({header_key}) from request"
        )

    if not verify_signature:
        logger.warning(
            "DEV_MODE is set to True. Token signature will not be verified. Only claims will be retrieved"  # noqa
        )
    opts = {"verify_signature": verify_signature}
    key = cfg.get("jwt_signing_key") or ""
    if not key and verify_signature:
        raise StrangeworksError(
            "unable to obtain signing key for auth token validation."
        )
    try:
        logger.debug(f"verifying token ({token}), verify_sig: {verify_signature})")
        claims = jwt.decode(token=token, key=key, options=opts, issuer="strangeworks")
        return claims, token
    except BaseException as ex:
        raise StrangeworksError.authentication_error(
            "auth token failed verification"
        ) from ex
