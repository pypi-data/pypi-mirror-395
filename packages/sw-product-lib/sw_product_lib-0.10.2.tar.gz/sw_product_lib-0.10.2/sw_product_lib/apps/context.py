"""context.py"""

import os
from abc import ABC, abstractmethod
from typing import Any

from fastapi import Request
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from sw_product_lib import DEFAULT_PLATFORM_BASE_URL, in_dev_mode
from sw_product_lib.apps.auth import gcp, sw_proxy
from sw_product_lib.platform.gql import ProductAPI


class AppContext(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    product_slug: str | None = Field(
        default=None, validation_alias=AliasChoices("product_slug", "ProductSlug")
    )
    product_api_key: str | None = os.environ.get("PRODUCT_LIB_API_KEY")
    base_url: str = os.environ.get("PRODUCT_LIB_BASE_URL", DEFAULT_PLATFORM_BASE_URL)
    api: ProductAPI | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.api is None and self.product_api_key:
            self.api = ProductAPI(api_key=self.product_api_key, base_url=self.base_url)


class BaseRequestContext(AppContext, ABC):
    """Abstract Base Class for all Request Context Classes."""

    @classmethod
    @abstractmethod
    def from_request(cls, request: Request) -> "BaseRequestContext":
        """Construct Context from FastAPI Request.

        This is where authentication (verify jwt signature) should occur.
        """
        pass


class SchedulerRequestContext(BaseRequestContext):
    """Context for Scheduler Requests.

    Expects a JWT token from a Google Cloud service account.
    """

    scheduler_jwt: str | None = None
    claims: dict | None = None

    @classmethod
    def _validate_request(
        cls,
        *,
        request: Request,
        **kwargs,
    ) -> dict[str, Any]:
        """Validate Service Token."""
        claims, token = gcp.verify_token(
            request=request, verify_signature=not in_dev_mode()
        )

        return {
            "scheduler_jwt": token,
            "claims": claims,
        }

    @classmethod
    def from_request(cls, *, request: Request):
        class_args = cls._validate_request(request=request)
        return cls(**class_args)


class UserRequestContext(BaseRequestContext):
    """Context for User-Initiated Requests.

    Expects a Strangeworks platform proxy jwt token.
    """

    workspace_member_slug: str = Field(
        validation_alias=AliasChoices("workspace_member_slug", "WorkspaceMemberSlug")
    )
    resource_slug: str | None = Field(
        default=None, validation_alias=AliasChoices("resource_slug", "ResourceSlug")
    )
    resource_token_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("resource_token_id", "ResourceTokenID"),
    )
    resource_entitlements: list[str] | None = Field(
        default=None, validation_alias=AliasChoices("ResourceEntitlements")
    )
    workspace_slug: str | None = Field(
        default=None, validation_alias=AliasChoices("workspace_slug", "WorkspaceSlug")
    )

    parent_job_slug: str | None = None
    experiment_trial_id: str | None = None

    proxy_jwt: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "_auth_token", "proxy_jwt", "x-strangeworks-access-token"
        ),
    )

    @classmethod
    def _validate_request(
        cls,
        *,
        request: Request,
    ) -> dict[str, Any]:
        """Validate User Request.

        Returns tuple of dictionary and string. The dictionary has the claims and parent
        job slug (if there is a parent) and the string contains the jwt token.
        """
        claims, token = sw_proxy.verify_token(
            request=request, verify_signature=not in_dev_mode()
        )
        init_args = {"proxy_jwt": token}
        init_args |= claims

        parent_job_slug: str | None = request.headers.get(
            "x-strangeworks-parent-job-slug"
        )
        if parent_job_slug:
            init_args["parent_job_slug"] = parent_job_slug
        return init_args

    @classmethod
    def from_request(cls, request: Request):
        class_args = cls._validate_request(request=request)
        return cls(**class_args)
