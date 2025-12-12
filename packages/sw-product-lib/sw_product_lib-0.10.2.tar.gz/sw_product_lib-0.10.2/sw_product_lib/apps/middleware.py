"""middleware.py."""

import logging
from typing import Awaitable, Callable, Type

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from strangeworks_core.errors.error import StrangeworksError

from sw_product_lib import is_service_disabled
from sw_product_lib.apps.context import (
    AppContext,
    BaseRequestContext,
    SchedulerRequestContext,
)
from sw_product_lib.service import RequestContext


logger = logging.getLogger(__name__)
# items in open_paths do not require any authentication.
default_public_paths = ["/docs", "/openapi.json", "/", "/redoc"]


class StrangeworksMiddleware(BaseHTTPMiddleware):
    """Middleware for handling interations between apps and the SW platform.

    Requests to public paths do not require authorization tokens. All other requests
    require a valid auth token unless the application is running in dev mode. An auth
    token is valid if its signature and its issuer can be verified.

    If the application is running in dev mode, requests to paths in scheduler_paths
    will not require any tokens or "Authorization" header. Requests to all other paths
    (other than those in public_paths) will require a jwt token with claims for
    workspace member slug and resource slug.

    To enable the application to run in dev mode, set the following environment variable
    ```bash
    export STRANGEWORKS_CONFIG_DEFAULT_DEV_MODE=True
    ```

    Context objects are items that are created in the middleware and are used when
    making calls to the platform. The RequestContext object is generated and attached
    to the request for user initiated requests. SchedulerContext is generated for
    requests from the Google Cloud Scheduler. The SchedulerContext object contains the
    client to make calls to the product API.The RequestContext object has items to
    identify which user and workspace the request is coming from.

    The paths "/docs", "/openapi.json", "/", and "/redoc" are always included in public
    paths.

    Service can be disabled (reject requests) by setting the following environment
    variable:
    ```bash
    export STRANGEWORKS_CONFIG_DEFAULT_SERVICE_DISABLED=True
    ```

    Healthcheck (/) is not affected by the SERVICE_DISABLED setting.
    """

    def __init__(
        self,
        *args,
        scheduler_paths: list[str] = [],
        public_paths: list[str] = [],
        user_req_ctx_factory: Type[BaseRequestContext] = RequestContext,
        svc_req_ctx_factory: Type[BaseRequestContext] = SchedulerRequestContext,
        **kwargs,
    ):
        """Initialize Strangeworks Middleware."""
        super().__init__(*args, **kwargs)
        self.public_paths = list(set(public_paths + default_public_paths))
        self.scheduler_paths = scheduler_paths
        self.user_req_ctx_factory: Type[BaseRequestContext] = user_req_ctx_factory
        self.svc_req_ctx_factory: Type[BaseRequestContext] = svc_req_ctx_factory

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Dispatch Strangeworks Requests.

        Handles verification of requests based on paths. Creates context objects
        and attaches them to requests so that handlers can access and interact
        with the platform product API.

        Parameters
        ----------
        request: Request
            The request to the application. Commonly from a user via the platform or
            Google Cloud Scheduler.
        call_next: Callable
            The handler method to call after middleware.

        Returns
        -------
        : Awaitable
            An Awaitable object from the next handler.
        """
        if is_service_disabled() and request.url.path != "/":
            logger.warning(
                "Service has been disabled. Request ignored: {request.url.path}"
            )
            return JSONResponse(status_code=503, content="service has been disabled")

        logger.debug(f"Handling request {request.url.path}")
        try:
            if request.url.path in self.scheduler_paths:
                logger.debug("generating SchedulerRequestContext from request")
                ctx = self.svc_req_ctx_factory.from_request(request=request)
                request.state.ctx = ctx
            elif request.url.path in self.public_paths:
                logger.debug(
                    "request is for a public path. no token validation necessary."
                )
                ctx: AppContext = AppContext()
                request.state.ctx = ctx
            else:
                logger.debug("generating RequestContext from user request")
                # using RequestContext for now. Switch over to UserRequestContext
                # once all the apps are ready.
                ctx = self.user_req_ctx_factory.from_request(request=request)
                request.state.ctx = ctx
        except BaseException as ex:
            # wrap exception as StrangeworksError
            raise StrangeworksError(
                f"error handling request to {request.url.path}"
            ) from ex

        return await call_next(request)
