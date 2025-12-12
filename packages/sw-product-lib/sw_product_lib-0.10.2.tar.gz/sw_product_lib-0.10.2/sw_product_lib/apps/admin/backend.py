"""backend.py."""

import json
import logging

from strangeworks_core.types.backend import Backend
from strangeworks_core.types.backend import Status as BackendStatus
from strangeworks_core.types.base import RemoteObject

from sw_product_lib import service
from sw_product_lib.apps.context import AppContext
from sw_product_lib.types.backend import BackendCreateInput, BackendUpdateInput

from .status import BackendUpdate, StatusPoller


def _fix_remote_status(remote_status: any) -> str:
    if isinstance(remote_status, str):
        return remote_status
    if isinstance(remote_status, dict):
        # convert to json string
        return json.dumps(remote_status)
    return str(remote_status)


def process_update(
    status_updates: list[BackendUpdate],
    existing_objects: list[RemoteObject],
):
    """Process Remote Status Updates for Backends.

    Parameters
    ----------
    status_updates: list[StatusUpdate]
        list of status updates retrieved from the remote source.
    existing_objects: list[RemoteObject]
        list of remote objects from the Strangeworks platform.

    Returns
    -------
    :(list[BackendCreateInput], list[BackendUpdateInput])
        tuple consisting of a list of backend create inputs and a list of backend
        update inputs.
    """
    new_objects: list[BackendCreateInput] = []
    object_updates: list[BackendUpdateInput] = []

    platform_dict: dict[str, RemoteObject] = (
        dict(
            (b.remote_id, b)
            for b in existing_objects
            if b.status != BackendStatus.RETIRED
        )
        if existing_objects
        else {}
    )
    for status_update in status_updates:
        platform_object = platform_dict.pop(status_update.remote_id, None)
        if platform_object is None:
            logging.info(
                f"new backend: (name: {status_update.name or status_update.remote_id}, status: {status_update})"  # noqa
            )

            new_objects.append(
                BackendCreateInput(
                    name=status_update.name or status_update.remote_id,
                    remoteBackendId=status_update.remote_id,
                    status=status_update.status(),
                    remoteStatus=_fix_remote_status(status_update.remote_status),
                    data=status_update.data,
                    dataSchema=status_update.data_schema,
                )
            )
        else:
            logging.info(
                f"status update for backend (name: {status_update.name or status_update.remote_id}, slug: {platform_object.slug}) status={status_update}"  # noqa
            )
            object_updates.append(
                BackendUpdateInput(
                    backendSlug=platform_object.slug,
                    remoteBackendId=status_update.remote_id,
                    remoteStatus=_fix_remote_status(status_update.remote_status),
                    status=status_update.status(),
                )
            )

    if platform_dict:
        # if there are remaining platform objects with no status updates, set their
        # status to UNKNOWN
        for obj in platform_dict.values():
            logging.info(
                f"no update received for backend (slug: {obj.slug}, setting status to UNKNOWN)"  # noqa
            )
            object_updates.append(
                BackendUpdateInput(
                    backendSlug=obj.slug,
                    status=BackendStatus.UNKNOWN,
                    remoteBackendId=obj.remote_id,
                )
            )
    return (new_objects, object_updates)


def update_backend_status(ctx: AppContext, poller: StatusPoller):
    """Update Backend Status.

    Retrieves status updates using the poller and applies them. The lists of
    newly created backends and updated backends are returned to allow the caller
    to perform additional product-specific updates.

    Parameters
    ----------
    ctx: ServiceContext
        Context object used for making requests to the platform.
    poller: StatusPoller
        Function for retrieving status updates from remote source.

    Return:
    :(list[Backend], list[Backend])
        A tuple with list of new backends that were created and list of backends whose
        status was updated.
    """
    # poll remote status updates
    status_updates = poller()
    # if any status updates were received, retrieve backends from platform
    backends = service.get_backends(
        ctx,
        product_slugs=ctx.product_slug,
        backend_statuses=["ONLINE", "OFFLINE", "MAINTENANCE", "UNKNOWN"],
    )

    creates, updates = process_update(status_updates, backends)

    updated_backends: list[Backend] = []
    # it takes much longer to update each backend individually so continue sending
    # the complete list of updates for now.
    try:
        updated_backends: list[Backend] = service.update_backends(ctx, backends=updates)
    except BaseException as e:
        logging.error("Error updating backends")
        logging.exception(e)

    created_backends: list[Backend] = []
    for new_backend in creates:
        try:
            res: list[Backend] = (
                service.create_backends(ctx, [new_backend]) if creates else []
            )
            created_backends.extend(res)
        except BaseException as e:
            logging.error(
                f"Error creating new backend (name: {new_backend.name}, remote_id: {new_backend.remoteBackendId})"  # noqa
            )
            logging.exception(e)

    return (created_backends, updated_backends)
