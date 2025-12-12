"""backend.py."""
from typing import List

from deprecated import deprecated
from strangeworks_core.platform.gql import API

from sw_product_lib.types import backend
from sw_product_lib.types.backend import (
    Backend,
    BackendCreateInput,
    BackendTypeInput,
    BackendUpdateInput,
)


@deprecated(reason=("Please use sw_product_lib.types.backend.get_backends instead."))
def get_backends(
    api: API,
    product_slugs: List[str] = None,
    backend_type_slugs: List[str] = None,
    backend_statuses: List[str] = None,
    backend_tags: List[str] = None,
) -> List[Backend]:
    """Retrieve a list of available backends."""
    return backend.get_backends(
        api=api,
        product_slugs=product_slugs,
        backend_type_slugs=backend_type_slugs,
        backend_statuses=backend_statuses,
        backend_tags=backend_tags,
    )


@deprecated(
    reason=("Please use sw_product_lib.types.backend.get_product_backends instead.")
)
def get_product_backends(
    api: API,
    status: str = None,
    remote_backend_id: str = None,
) -> List[Backend]:
    """Fetch backends for product

    Parameters
    ----------
    api: API
        provides access to the product API
    status: str
        filter by backend status
    remote_backend_id: str
        filter by the backend id set by the product

    Returns
    -------
    List[Backend]
        The list of backends filtered by the params
    """
    return backend.get_product_backends(
        api=api, status=status, remote_backend_id=remote_backend_id
    )


@deprecated(
    reason=("Please use sw_product_lib.types.backend.backend_add_types instead.")
)
def backend_add_types(
    api: API,
    backend_slug: str,
    backend_types: List[BackendTypeInput],
) -> None:
    return backend.backend_add_types(
        api=api, backend_slug=backend_slug, backend_types=backend_types
    )


@deprecated(
    reason=("Please use sw_product_lib.types.backend.backend_remove_types instead.")
)
def backend_remove_types(
    api: API,
    backend_slug: str,
    backend_type_slugs: List[str],
) -> None:
    return backend.backend_remove_types(
        api=api, backend_slug=backend_slug, backend_type_slugs=backend_type_slugs
    )


@deprecated(reason=("Please use sw_product_lib.types.backend.backend_create instead."))
def backend_create(
    api: API,
    payload: list[BackendCreateInput],
) -> list[Backend]:
    backend.backend_create(api=api, payload=payload)


@deprecated(reason=("Please use sw_product_lib.types.backend.backend_delete instead."))
def backend_delete(
    api: API,
    backend_slug: str,
) -> None:
    return backend.backend_delete(api=api, backend_slug=backend_slug)


@deprecated(reason=("Please use sw_product_lib.types.backend.backend_update instead."))
def backend_update(
    api: API,
    backend_update_input: List[BackendUpdateInput],
) -> Backend:
    return backend.backend_update(api=api, backend_update_input=backend_update_input)
