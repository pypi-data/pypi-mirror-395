from __future__ import annotations

from typing import List, Optional

from deprecated import deprecated
from strangeworks_core.platform.gql import API

from sw_product_lib.types.resource import Resource, ResourceConfiguration  # noqa
from sw_product_lib.types.resource import create as create_resource
from sw_product_lib.types.resource import fetch as fetch_resource
from sw_product_lib.types.resource import get as get_resource
from sw_product_lib.types.resource import store_config as resource_store_config


@deprecated(reason=("Please use sw_product_lib.types.resource module instead."))
def create(
    api: API,
    activation_id: str,
    status: str,
    api_route: Optional[str] = None,
    configurations: Optional[List[ResourceConfiguration]] = None,
) -> Resource:
    """Create a new resource definition on the platform.

    Parameters
    ----------
     api: API
        provides access to the platform API.
    """
    return create_resource(
        api=api,
        activation_id=activation_id,
        status=status,
        api_route=api_route,
        configurations=configurations,
    )


@deprecated(reason=("Please use sw_product_lib.types.resource module instead."))
def fetch(
    api: API,
    status_list: Optional[List[str]] = None,
) -> Optional[List[Resource]]:
    """Retrieve a list of available resources.

    Parameters
    ----------
    status_list: Optional(List[str])
        retrieve only those resources whose status is included in this list.
    """
    return fetch_resource(api=api, status_list=status_list)


@deprecated(reason=("Please use sw_product_lib.types.resource module instead."))
def store_config(
    api: API,
    resource_slug: str,
    config: ResourceConfiguration,
) -> Resource:

    return resource_store_config(api=api, resource_slug=resource_slug, config=config)


@deprecated(reason=("Please use sw_product_lib.types.resource module instead."))
def get(
    api: API,
    resource_slug: str,
) -> Resource:
    """Retrieve a resource entry from platform."""
    return get_resource(api=api, resource_slug=resource_slug)
