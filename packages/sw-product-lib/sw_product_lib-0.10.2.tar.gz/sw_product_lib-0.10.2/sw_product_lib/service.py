"""product.py."""
import json
import logging
import os
import tempfile
from functools import singledispatch
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import requests
from deprecated import deprecated
from fastapi import Request
from pydantic import JsonValue
from strangeworks_core.config.config import Config
from strangeworks_core.errors.error import StrangeworksError
from strangeworks_core.platform import auth
from strangeworks_core.platform.gql import APIInfo
from strangeworks_core.types import JsonObject
from strangeworks_core.types.batch import Options
from strangeworks_core.types.func import Func
from strangeworks_core.types.job import Status as JobStatus
from strangeworks_core.types.machine import Accelerator, Machine
from strangeworks_core.types.resource import KeyType

from sw_product_lib.apps.auth import sw_proxy
from sw_product_lib.apps.context import AppContext, UserRequestContext
from sw_product_lib.apps.jobs.types import PortalFile
from sw_product_lib.client import billing
from sw_product_lib.client.billing import BillingTransaction
from sw_product_lib.platform.gql import ProductAPI
from sw_product_lib.types import backend, batch_job
from sw_product_lib.types import job as job_impl
from sw_product_lib.types import resource
from sw_product_lib.types.job import AppliedJobTag, File, Job
from sw_product_lib.types.resource import Resource, ResourceConfiguration

from . import in_dev_mode


DEFAULT_PLATFORM_BASE_URL = "https://api.strangeworks.com"


_cfg = Config(use_namespace=False)


def _api(api_key: str | None = None, url: str | None = None) -> ProductAPI | None:
    _api_key = api_key or _cfg.get("PRODUCT_LIB_API_KEY")
    _base_url = url or _cfg.get("PRODUCT_LIB_BASE_URL") or DEFAULT_PLATFORM_BASE_URL
    return (
        ProductAPI(api_key=_api_key, base_url=_base_url)
        if _api_key and _base_url
        else None
    )


@deprecated(
    reason=(
        "ServiceContext is deprecated and will be removed in a future release. Use SchedulerRequestContext or UserRequestContext instead."  # noqa
    )
)
class ServiceContext(AppContext):
    """Base Context for Product Lib Requests.

    The Context object encapsulates items needed to make calls to the Product API. The
    attributes of the class are typically extracted from the token sent as a part
    of the request from the platform. For system-level requests (requests whose URL
    does not have a resource slug and only has a product slug), the service request has
    the product slug as well as an API connection. For user requests (requests whose URL
    includes a resource slug), the RequestContext object should be used.
    """

    @classmethod
    @deprecated(
        reason="This method/class will be removed in a future release. Use SchedulerRequestContext or UserRequestContext instead."  # noqa
    )
    def from_request(cls, request: Request):
        """Generate Service Context from a platform proxy token."""
        claims, _ = sw_proxy.verify_token(
            request=request, verify_signature=False if in_dev_mode() else True
        )
        return cls(**claims)


@deprecated(reason="This class is deprecated. Use UserRequestContext instead.")
class RequestContext(UserRequestContext):
    """Context for requests made by a user."""

    resource_token_id: Optional[str] = None
    job_id: str | None = None

    @deprecated(reason="This method is deprecated and will be removed soon.")
    @staticmethod
    def new(**kwargs):
        return UserRequestContext(**kwargs)

    @property
    def _auth_token(self) -> str | None:
        return self.proxy_jwt


def create_job(
    ctx: RequestContext,
    external_identifier: Optional[str] = None,
    status: str = "CREATED",
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
    **kvargs,
) -> Job:
    """Create a job entry for the request

    This method should be called only after the product has either has a job in place
    which will be executed either immediately or within a given period of time.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: Optional[str]
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.
    """
    return job_impl.create(
        api=ctx.api or _api(),
        resource_slug=ctx.resource_slug,
        workspace_member_slug=ctx.workspace_member_slug,
        parent_job_slug=ctx.parent_job_slug,
        external_identifier=external_identifier,
        status=status,
        remote_status=remote_status,
        job_data_schema=job_data_schema,
        job_data=job_data,
    )


def update_job(
    ctx: AppContext,
    job_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
    **kvargs,
) -> Job:
    """Update the job identified by job_slug.


    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
      slug of the job that needs values updated.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: Optional[str]
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.
    """
    return job_impl.update(
        api=ctx.api or _api(),
        job_slug=job_slug,
        parent_job_slug=parent_job_slug,
        external_identifier=external_identifier,
        status=status,
        remote_status=remote_status,
        job_data_schema=job_data_schema,
        job_data=job_data,
    )


def add_job_tags(
    ctx: AppContext,
    job_slug: str,
    tags: List[str],
    job: Job | None = None,
) -> List[AppliedJobTag]:
    """Apply a list of tags to a job.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
      slug of the job that needs values updated.
    tags: List[str]
        list of tags to apply to the job
    job: Job | None
        Optional job object. If available, used to determine the resource slug.
    """
    if job is None or job.resource is None:
        job = get_job(ctx=ctx, job_slug=job_slug)

    return job_impl.add_tags(
        api=ctx.api or _api(),
        resource_slug=job.resource.slug,
        job_slug=job_slug,
        tags=tags,
    )


def create_billing_transaction(
    ctx: AppContext,
    job_slug: str,
    amount: float,
    unit: str = "USD",
    description: Optional[str] = None,
    job: Job | None = None,
    usage: JsonValue | None = None,
) -> BillingTransaction:
    """Create a billing transaction.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        used as identifier for the job.
    amount: float
        numerical amount. can be negative.
    unit: str
        describes the unit for the amount. for example, USD for currency.
    description: str
        a brief description that can be seen by the user.
    job: Job
        strangeworks job
    usage: JsonValue
        dictionary of only usage information
    """

    if usage is not None:
        usage_token = os.environ.get("USAGE_SVC_TOKEN")
        header = {"Authorization": usage_token}
        usage_url = os.environ.get("USAGE_URL")

        ctx_json = ctx.__dict__
        usage["product_slug"] = ctx_json["product_slug"]
        usage["workspace_member_slug"] = ctx_json["workspace_member_slug"]
        usage["workspace_slug"] = ctx_json["workspace_slug"]
        usage["parent_job_slug"] = ctx_json["parent_job_slug"]
        usage["resource_slug"] = ctx_json["resource_slug"]
        usage["job_slug"] = job_slug

        try:
            res = requests.post(url=usage_url, headers=header, json=usage)
            res.raise_for_status()
        except Exception as ex:
            logging.error(
                f"Exception: {str(ex)} status_code: {res.status_code} response: {res.json()}"  # noqa
            )

    if job is None or job.resource is None:
        job = get_job(ctx, job_slug)

    return billing.create_transaction(
        api=ctx.api or _api(),
        resource_slug=job.resource.slug,
        job_slug=job_slug,
        amount=amount,
        unit=unit,
        description=description,
    )


def request_job_clearance(
    ctx: RequestContext,
    amount: float = 0.0,
    unit: str = "USD",
):
    """Request clearance from platform to run a job.

    Parameters
    ----------
    workspaceMemberSlug: str
            used to map workspace and user.
    amount: float
        numerical amount to indicate cost (negative amount) or credit(positive amount)
    unit: str
        unit for the amount
    """
    return billing.request_approval(
        api=ctx.api or _api(),
        resource_slug=ctx.resource_slug,
        workspace_member_slug=ctx.workspace_member_slug,
        amount=amount,
        currency=unit,
    )


def get_resource(ctx: RequestContext) -> Resource:
    """Retrieve a resource definition.

    The resource slug, which is used to identify the resource entry, is retrieved
    from the request context object passed in.

    Parameters:
    ctx: RequestContext
        contains key-values specific to the current request.

    """
    return resource.get(
        api=ctx.api or _api(),
        resource_slug=ctx.resource_slug,
    )


def add_resource_config(
    ctx: RequestContext, resource_slug: str, key: str, value: JsonObject
) -> Resource:
    """_summary_

    Parameters
    ----------
    ctx : RequestContext
        Key-value pairs which make up the current request context
    resource_slug : str
        Identifies a resource. The resource must belong to the same
        product as the api key being used in context.
    key : str
        identifier for the configuration value.
    value : JsonObject
        The value associated with the key. Must be a JSON object
        (see https://www.json.org/json-en.html) Can also be a string
        which is dump of a JSON object.
    Returns
    -------
    Resource
        The resource object with the new configuration.
    """
    _cfg: ResourceConfiguration = ResourceConfiguration(
        key=key,
        valueJson=value,
        value_type=KeyType.JSON,
        is_editable=True,
        is_internal=False,
    )
    return resource.store_config(
        api=ctx.api or _api(),
        resource_slug=resource_slug,
        config=_cfg,
    )


def resource_reset_config(ctx: RequestContext, resource_slug: str) -> Resource:
    """Clear our configuration settings for Given Resource.

    Parameters
    ----------
    ctx : RequestContext
        Current request context
    resource_slug : str
        identifies the resource

    Returns
    -------
    :Resource
        resource after its configurations have been reset.
    """
    return resource.reset_config(
        api=ctx.api or _api(),
        resource_slug=resource_slug,
    )


@singledispatch
def upload_job_artifact(
    data,
    ctx: RequestContext,
    job_slug: str,
    file_name: Optional[str] = None,
    json_schema: Optional[str] = None,
    label: Optional[str] = None,
    overwrite: bool = False,
    is_hidden: bool = False,
    sort_weight: int = 0,
    job: Job | None = None,
    *args,
    **kwargs,
) -> File:
    """Upload payload as a file to the platform.

    Parameters
    ----------
    ctx: RequestContext
        used for making calls to service lib.
    job_slug: str
        maps the file to a job.
    data: Any
        file contents. Only dict supported at this time.
    file_name: Optional[str]
        the name of the file on the platform. if not supplied, the tempfile name will
        be used.
    json_schema: Optional[str]
        identifier or link to a json schema which corresponds to the file contents. If
        the file contents adhere to a schema, it is highly recommended that this field
        is populated.
    label: Optional[str]
        Optional string to set the display name of the file. Used by the platform
        portal.
    overwrite: bool
        indicates whether the file should be overwritten if its already been uploaded
        for the job. Defaults to False.
    is_hidden: bool
        If true, this file will not be displayed in the portal.
        This can be useful for supporting files that should be saved against the job,
        but typically would be referenced by URL in other contexts.
        (i.e.: an image file which is referenced in a JSON model.)
        This does **not*** prevent a user from accessing this file in other contexts,
        such as job archives.
    sort_weight: int
        This is the primary sorting instruction for JobFiles
        when returned to the client.
        The default is 0.
        Files with a higher sort order will be returned first.
        This allows you to control the order of files in the portal if desired.
    job: Job | None
        Optional job object. If available, used to determine the resource slug.
    Returns
    -------
    None
    """
    with tempfile.NamedTemporaryFile(mode="+w") as tmp:
        tmp.write(data)
        tmp.flush()
        return upload_job_file(
            ctx=ctx,
            job_slug=job_slug,
            name=file_name or tmp.name,
            path=tmp.name,
            json_schema=json_schema,
            sort_weight=sort_weight,
            label=label,
            is_hidden=is_hidden,
            overwrite=overwrite,
            job=job,
        )


@upload_job_artifact.register
def _(
    data: dict,
    **kwargs,
) -> File:
    """Upload a job artifact of type dictionary.

    Note that the order of parameters is slightly different for this method with the
    data field coming first. This is to allow the singledispatch decorator to work.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        identifies which job the file is associated with.
    data: str
        data (dictionary)
    file_name: Optional[str]
        file name.
    label: Optional[str]
        Optional string to set the label for the file.
    overwrite: bool
        if True, overwrite the file if it already exists.
    is_hidden: bool
        if True, the file will not be visible to the user.
    sort_weight: int
        used to sort files in the UI.
    job: Job | None
        Optional job object. If available, used to determine the resource slug.
    """
    as_str = json.dumps(data)
    return upload_job_artifact(
        as_str,
        **kwargs,
    )


@upload_job_artifact.register
def _(
    data: list,
    **kwargs,
) -> File:
    """Upload a job artifact of type list.

    Note that the order of parameters is slightly different for this method with the
    data field coming first. This is to allow the singledispatch decorator to work.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        identifies which job the file is associated with.
    data: list
        data (list)
    file_name: Optional[str]
        file name.
    label: Optional[str]
        Optional string to set the label for the file.
    overwrite: bool
        if True, overwrite the file if it already exists.
    is_hidden: bool
        if True, the file will not be visible on the portal.
    sort_weight: int
        used to sort files in the UI.
    job: Job | None
        Optional job object. If available, used to determine the resource slug.
    """
    as_str = json.dumps(data)
    return upload_job_artifact(
        as_str,
        **kwargs,
    )


@upload_job_artifact.register
def _(
    data: PortalFile,
    ctx: RequestContext,
    job_slug: str,
    job: Job | None = None,
    **kwargs,
) -> File:
    """Upload a job artifact of type PortalFile.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        identifies which job the file is associated with.
    data: str
        string to be uploaded as a file.
    file_name: Optional[str]
        file name.
    label: Optional[str]
        Optional string to set the label for the file.
    overwrite: bool
        if True, overwrite the file if it already exists.
    is_hidden: bool
        if True, the file will not be visible to the user.
    sort_weight: int
        used to sort files in the UI.
    job: Job | None
        Optional job object. If available, used to determine the resource slug.
    kwargs: dict | None
        Keyword args. Ignored for now.
    """
    f: File = upload_job_artifact(
        data.data,
        ctx=ctx,
        job_slug=job_slug,
        file_name=data.name,
        json_schema=data.artifact_schema,
        label=data.label,
        overwrite=data.overwrite,
        is_hidden=data.is_hidden,
        sort_weight=data.sort_weight,
        job=job,
    )
    data.url = f.url
    data.file_slug = f.slug
    return f


def upload_job_file(
    ctx: AppContext,
    job_slug: str,
    name: Optional[str],
    path: str,
    json_schema: Optional[str] = None,
    label: Optional[str] = None,
    overwrite: bool = False,
    is_hidden: bool = False,
    sort_weight: int = 0,
    job: Job | None = None,
) -> File:
    """Upload a file associated with a job.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        identifies which job the file is associated with.
    name: Optional[str]
        file name.
    path: str
        fully qualified path to the file.
    json_schema: Optional[str]
        identifier or link to a json schema which corresponds to the file contents. If
        the file contents adhere to a schema, it is highly recommended that this field
        is populated.
    label: Optional[str]
        Optional string to set the display name of the file. Used by the platform
        portal.
    overwrite: bool
        indicates whether the file should be overwritten if its already been uploaded
        for the job. Defaults to False.
    is_hidden: bool
        If true, this file will not be displayed in the portal.
        This can be useful for supporting files that should be saved against the job,
        but typically would be referenced by URL in other contexts.
        (i.e.: an image file which is referenced in a JSON model.)
        This does **not*** prevent a user from accessing this file in other contexts,
        such as job archives.
    sort_weight: int
        This is the primary sorting instruction for JobFiles
        when returned to the client.
        The default is 0.
        Files with a higher sort order will be returned first.
        This allows you to control the order of files in the portal if desired.
    job: Job | None
        Optional job object. If available, used to determine the resource slug.

    Return
    ------
    File
        Object with information about the file that was uploaded.

    raises StrangeworksError if any issues arise while attempting to upload the file.
    """
    if job is None or job.resource is None:
        job = get_job(ctx=ctx, job_slug=job_slug)

    f, signedUrl = job_impl.upload_file(
        api=ctx.api or _api(),
        resource_slug=job.resource.slug,
        job_slug=job_slug,
        file_path=path,
        file_name=name,
        override_existing=overwrite,
        json_schema=json_schema,
        is_hidden=is_hidden,
        sort_weight=sort_weight,
        label=label,
    )
    try:
        fd = open(path, "rb")
    except IOError as e:
        raise StrangeworksError(message=f"unable to open file: {str(e)}")
    else:
        with fd:
            headers = {"content-type": "application/x-www-form-urlencoded"}
            r = requests.put(signedUrl, data=fd, headers=headers)
            if r.status_code not in {requests.codes.ok, requests.codes.no_content}:
                raise StrangeworksError(
                    "unable to upload job file", r.status_code, str(r.content)
                )

    return f


def get_jobs(
    ctx: AppContext,
    resource_slug: str | None = None,
    parent_job_slug: str | None = None,
    tags: List[str] | None = None,
    statuses: List[JobStatus] | None = None,
    cursor: str | None = None,
    batch_size: int = 50,
) -> Tuple[List[Job], str, bool]:
    """Get Jobs (pagination)

    Uses pagination to retrieve list of jobs which match given filters.
    Example of how to paginate over jobs:
    ```python
    has_next_page: bool = True
    cursor: str = None
    while has_next_page:
        jobs, cursor, has_next_page = service.get_jobs(ctx, cursor=cursor)
        ...
        # do something with jobs
    ```
    Avoid reading the complete list of jobs in order to not crash the application due
    insufficient memory. Read jobs in chunks, use them as needed then release by
    dereferencing the list so that the garbage collector can claim the unused memory.

    Parameters
    ----------
    ctx: ServiceContext
        contains key-values specific to the current request.
    resource_slug: str | None
        filters jobs by resource. Defaults to None.
    parent_job_slug: str | None
        filters jobs by their parent slug. Defaults to None.
    tags: List[str] | None
        filters jobs by their tags. Only jobs which have a tag that matches any in the
        list will be returned. Defaults to None.
    statuses: List[str] | None
        filters jobs by their status. Only jobs whose status matches one in the list
        will be returned. Defaults to None.
    cursor: str | None
        Used for pagination. The cursor value from prior call must be supplied in order
        to paginate over the complete result set. The initial value should be None,
        unless the caller wishes the pagination to begin at a certain cursor. Note that
        the cursor may become invalid if its associated job entry is deleted.
    batch_size: int = 50
        Number of job objects to retrieve with each call. Limited to 50.
    """
    return job_impl.get_list(
        api=ctx.api or _api(),
        resource_slug=resource_slug,
        parent_job_slug=parent_job_slug,
        tags=tags,
        statuses=statuses,
        start_cursor=cursor,
        batch_size=50 if batch_size > 50 else batch_size,
    )


def get_job(ctx: AppContext, job_slug: str) -> Job:
    """Get the job identified by job_slug.


    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        job_slug identifies the job which is fetched.

    Returns
    -------
    Job
        A Job object identified by the slug.
    """
    return job_impl.get(api=ctx.api or _api(), id=job_slug)


def get_job_by_external_identifier(
    ctx: RequestContext, external_identifier: str
) -> Optional[Job]:
    """Get the job identified by external_identifier.
    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    external_identifier: str
        external_identifier identifies the job which is fetched.
    Returns
    -------
    Optional[Job]
        A Job object identified by the product identifier or None.
    """
    return job_impl.get_by_external_identifier(
        api=ctx.api or _api(),
        id=external_identifier,
    )


def get_jobs_by_statuses(
    ctx: RequestContext, statuses: List[JobStatus]
) -> Optional[Dict[JobStatus, List[Job]]]:
    """Retrieve jobs filtered by job statuses.

    Parameters:
    ----------
     ctx: RequestContext
        contains key-values specific to the current request.
    statuses: List[JobStatus]
        the statuses used to filter for jobs.

    Returns:
    ----------
    A dictionary where the jobs are grouped by statuses.
    The keys in the dictionary are the statuses.
    Each status has their list of jobs.

    Optional[Dict[JobStatus, List[Job]]]
    """
    return job_impl.get_by_statuses(api=ctx.api or _api(), statuses=statuses)


def get_backends(
    ctx: AppContext,
    product_slugs: Optional[List[str]] = None,
    backend_type_slugs: Optional[List[str]] = None,
    backend_statuses: Optional[List[str]] = None,
    backend_tags: Optional[List[str]] = None,
) -> List[backend.Backend]:
    """Get the backends that live in strangeworks platform.
    Backends can be filtered by various input parameters.

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    product_slugs: Optional[List[str]]
        filter by one or more product slugs
    backend_type_slugs: Optional[List[str]]
        filter by one or more backendType slugs
    backend_statuses: Optional[List[str]]
        filter by one or more backend statuses
    backend_tags: Optional[List[str]]
        filter by one or more backend tags
    status: Optional[str]
        filter by status, optional
    remote_backend_id: Optional[str]
        filter by remote backend id, optional

    Returns
    -------
    List[Backend]
        The list of backend filtered by the params
    """
    return backend.get_backends(
        api=ctx.api or _api(),
        product_slugs=product_slugs,
        backend_type_slugs=backend_type_slugs,
        backend_statuses=backend_statuses,
        backend_tags=backend_tags,
    )


def get_product_backends(
    ctx: AppContext,
    status: Optional[str] = None,
    remote_backend_id: Optional[str] = None,
) -> List[backend.Backend]:
    """Get the backends that this product owns.
    Backends can be filtered by various input parameters.

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    status: Optional[str]
        filter by status, optional
    remote_backend_id: Optional[str]
        filter by remote backend id, optional

    Returns
    -------
    List[Backend]
        The list of backend filtered by the params
    """
    return backend.get_product_backends(
        api=ctx.api or _api(), status=status, remote_backend_id=remote_backend_id
    )


def create_backends(
    ctx: AppContext, backends: List[backend.Backend]
) -> List[backend.Backend]:
    """Create backends specified by the payload

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    backends: List[Backend]
        backends to create

    Returns
    -------
    List[Backend]
        The list of backends created
    """
    return backend.backend_create(api=ctx.api or _api(), payload=backends)


def delete_backend(ctx: AppContext, backend_slug: str) -> None:
    """Delete backend by slug

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    backend_slug: str
        backend to delete

    Returns
    -------
    None
    """
    return backend.backend_delete(api=ctx.api or _api(), backend_slug=backend_slug)


def update_backends(
    ctx: AppContext, backends: List[backend.BackendUpdateInput]
) -> List[backend.Backend]:
    """Update backends specified by the payload
    Overwites all write-able fields, so must include
    original payload, otherwise some fields could be deleted

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    backends: List[BackendUpdateInput]
        backend update input for each backend to update

    Returns
    -------
    List[Backend]
        The list of backends updated
    """
    return backend.backend_update(api=ctx.api or _api(), backend_update_input=backends)


def add_backend_types(
    ctx: AppContext, backend_slug: str, types: List[backend.BackendTypeInput]
):
    """Add backend types to a certain backend.
    Strangeworks defines certain types a backend can adhere to.
    This registers the specified backend with the many types provided.
    The type slugs have to be known by Strangeworks.
    Will raise a StrangeworksError if any types are unkown.

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    backend_slug: str
        backend slug that identifies the backend which you will add types to
    types: List[backend.BackendTypeInput]
        the many types you are registering to this backend.

    """
    backend.backend_add_types(
        api=ctx.api or _api(), backend_slug=backend_slug, backend_types=types
    )


def remove_backend_types(ctx: AppContext, backend_slug: str, types: List[str]):
    """Remove backend types from a certain backend.
    Strangeworks defines certain types a backend can adhere to.
    This un-registers the specified backend with the many types provided.
    The type slugs have to be known by Strangeworks.
    Will raise a StrangeworksError if any types are unkown.

    Parameters
    ----------
    ctx: AppContext
        contains key-values specific to the current request.
    backend_slug: str
        backend slug that identifies the backend which you will add types to
    types: List[str]
        the many types you are un-registering from this backend.

    """
    backend.backend_remove_types(
        api=ctx.api or _api(), backend_slug=backend_slug, backend_types=types
    )


@deprecated(
    reason=(
        "This function is deprecated and will be removed. Use auth.get_token instead."
    )
)
def get_token(key: Optional[str] = None, url: Optional[str] = None) -> str:
    """Obtain a product api token.

    This function is deprecated and will be removed in a future release. Use the
    auth.get_token function to obtain a one-time token or obtain a Callable using
    auth.get_authenticator to refresh tokens from clients such as requests.

    Parameters
    ----------
    key: Optional[str]
        key to use to obtain the token.
    url: Optional[str]
        strangeworks platform base url.

    Return
    ------
    :str
        A JWT token to make calls to the platform.
    """
    return auth.get_token(
        api_key=key or _cfg.get("PRODUCT_LIB_API_KEY"),
        base_url=url or _cfg.get("PRODUCT_LIB_BASE_URL") or DEFAULT_PLATFORM_BASE_URL,
        auth_url=APIInfo.PRODUCT.value.get("auth_url"),
    )


def execute_subjob(
    ctx: RequestContext,
    subjob_resource: Resource,
    parent_job: Union[str, Job],
    subjob_path: Optional[str] = None,
    subjob_json: Optional[Dict[str, Any]] = None,
    subjob_data: Optional[Any] = None,
    raw_result: Optional[bool] = False,
    result_parser: Callable[[Dict[str, Any]], Dict[str, Any]] = Job.from_dict,
) -> Job:
    """Execute a subjob.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    subjob_resource: Resource
        The resource to execute the subjob on.
    parent_job: Union[str, Job]
        A string or job object with the parent job slug.
    parent_job_slug: Optional[str]
        The slug of the parent job of the sub-job.
    subjob_path: Optional[str]
        The path to the sub-job.
    subjob_json: Optional[Dict[str, Any]]
        A JSON serializable Python object to send in the body of the Request.
    subjob_data: Optional[Any]
        The data to send in the body of the request.
        This can be a FormData object or anything that can be passed into
        FormData, e.g. a dictionary, bytes, or file-like object
    raw_result: Optional[bool]
        If True, return the raw JSON response from the platform.
        If False, parse the JSON reponse into a Job object.
    result_parser: Callable[[Dict[str, Any]], Dict[str, Any]]
        A callable function that takes a JSON response from the platform and parses it.

    Returns
    -------
    Job
        A job object denoting the sub-job.
    """
    parent_slug = parent_job.slug if isinstance(parent_job, Job) else parent_job
    if not parent_slug:
        raise ValueError("parent_job (slug or Job object) must be provided.")

    try:
        retval = job_impl.execute_subjob(
            parent_job_slug=parent_slug,
            api_key=ctx.product_api_key,
            proxy_auth_token=ctx._auth_token,
            resource=subjob_resource,
            path=subjob_path,
            json=subjob_json,
            data=subjob_data,
            base_url=_cfg.get("PRODUCT_LIB_BASE_URL") or DEFAULT_PLATFORM_BASE_URL,
        )
        retval.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if retval.status_code == 400:
            raise StrangeworksError(message=retval.text) from e
        raise StrangeworksError(message=e) from e

    as_json = retval.json()

    if raw_result is True:
        return as_json

    return result_parser(as_json)


def get_job_file(ctx: AppContext, file_path: str):
    """Call platform to return file belonging to job or one of its child jobs.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    file_path: str
        path of the file to be downloaded

    Returns
    -------
    json
        json object containing the file contents
    """

    retval = job_impl.get_job_file(
        api_key=ctx.product_api_key,
        file_path=file_path,
        base_url=_cfg.get("PRODUCT_LIB_BASE_URL") or DEFAULT_PLATFORM_BASE_URL,
    )

    return retval.json()


def create_batch_job(
    ctx: RequestContext,
    function: Callable[..., Any],
    fargs: tuple = (),
    fkwargs: dict[str, Any] = {},
    machine: Machine = Machine(),
    accelerator: Optional[Accelerator] = None,
    requirements_path: Optional[str] = None,
    job_slug: Optional[str] = None,
    workspace_member_slug: Optional[str] = None,
    options: Optional[Options] = None,
) -> str:
    """
    Create a batch job.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    function: Callable[..., Any]
        The function to execute.
    fargs: tuple
        The function arguments.
    fkwargs: dict[str, Any]
        The function keyword arguments.
    machine: Machine
        The machine to execute the job on.
    accelerator: Optional[Accelerator]
        An accelerator to use.
    requirements_path: Optional[str]
        The path to the requirements file.
    job_slug: Optional[str]
        The slug of the job.
    workspace_member_slug: Optional[str]
        The slug of the workspace member.
    options: Optional[Options]
        The options for the batch job.

    Returns
    -------
    batch_job_slug: str
        The slug of the batch job.

    """

    f = Func(
        func=function, fargs=fargs, fkwargs=fkwargs, requirements_path=requirements_path
    )

    return batch_job.new(
        api=ctx.api or _api(),
        resource_slug=ctx.resource_slug,
        decorator_name="",
        func=f,
        machine=machine,
        accelerator=accelerator,
        job_slug=job_slug,
        workspace_member_slug=workspace_member_slug,
        options=options,
    )


def get_file(
    ctx: RequestContext,
    file_slug: str,
    file_name: str,
    file_dir: str | Path = Path("."),
    chunk_size: int = 1024 * 1024,
) -> Path:
    """Retrieve file from platform.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    file_slug: str
        file identifier.
    file_name: str
        name to save the file locally.
    file_dir: str
        directory where the file is to be saved.
    chunk_size: int
        how much data to read in at a time in bytes. The size impacts memory
        requirements for the service.

    Returns
    -------
    : Path
        POSIX path to the file.
    """
    _fname = file_name
    _fpath: Path = file_dir if isinstance(file_dir, Path) else Path(file_dir)
    if not _fpath.exists():
        raise StrangeworksError("Directory {file_dir} does not exist.")
    _fpath = _fpath / _fname
    _base_url = _cfg.get("PRODUCT_LIB_BASE_URL") or DEFAULT_PLATFORM_BASE_URL

    authtoken = auth.get_token(
        api_key=ctx.product_api_key,
        base_url=_base_url,
        auth_url="product/token",
    )
    # platform URL for requesting workspace file is
    # workspace/{workspace_slug}/files/{file_slug}
    _url = f"{_base_url}/workspace/{ctx.workspace_slug}/files/{file_slug}"
    with requests.get(
        _url, headers={"Authorization": f"bearer {authtoken}"}, stream=True
    ) as resp:
        resp.raise_for_status()
        with open(_fpath.as_posix(), "wb") as fp:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                fp.write(chunk)
    return _fpath


def get_jobs_to_update(
    ctx: RequestContext,
    cursor: str | None = None,
    batch_size: int = 50,
) -> Tuple[List[Job], str, bool]:
    """Retrieve paginated list of jobs to update.

    Platform will only return jobs which were created by the application. In more
    detailed terms, the jobs whose resource is for the same product as the product
    whose api key is used to request the list will be returned.

    Along with matching the current product, jobs must be in a non-terminal state (see
    NON_TERMINAL_STATUSES in jobs)

    If the resource associated with the job has a api_url specified, this function
    will only retrieve jobs whose resource api url matches the one specified by the
    environment variable STRANGEWORKS_CONFIG_DEFAULT_PRODUCT_CUSTOM_URL.

    Returns
    -------
    : List[Jobs], str, bool
        a tuple consisting of a list of jobs, a string to indicate the cursor, and a
        boolean indicating whether there are any more records to be fetched.
    """
    api_url = _cfg.get("product_custom_url") or None

    jobs, cursor, has_next = job_impl.get_list(
        api=ctx.api or _api(),
        statuses=job_impl.NON_TERMINAL_STATUSES,
        start_cursor=cursor,
        batch_size=50 if batch_size > 50 else batch_size,
    )
    result_list = (
        [j for j in jobs if j.resource.api_url == api_url] if len(jobs) > 0 else []
    )
    return result_list, cursor, has_next
