"""job.py."""
from typing import Dict, List, Optional, Tuple

from deprecated import deprecated
from strangeworks_core.platform.gql import API
from strangeworks_core.types.job import Status as JobStatus

from sw_product_lib.types.job import AppliedJobTag, File, Job
from sw_product_lib.types.job import add_tags as job_add_tags
from sw_product_lib.types.job import create as job_create
from sw_product_lib.types.job import get as job_get
from sw_product_lib.types.job import (
    get_by_external_identifier as job_get_by_external_id,
)
from sw_product_lib.types.job import get_by_statuses as job_get_by_statuses
from sw_product_lib.types.job import update as job_update
from sw_product_lib.types.job import upload_file as job_upload_file


@deprecated(reason=("Please use sw_product_lib.types.job.create instead."))
def create(
    api: API,
    resource_slug: str,
    workspace_member_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
) -> Job:
    """Create a job entry

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    workspaceMemberSlug: str
        used to map workspace and user.
    parentJobSlug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: {Optionapstr
        status of the job. Refer to the  platform for possible values.
    remoteStatus: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    jobDataSchema: Optional[str]
        link to the json schema describing job output.
    jobData: Optional[str]
        job output.

    Returns
    -------
    : Job
        The ``Job`` object
    """
    return job_create(**locals())


@deprecated(reason=("Please use sw_product_lib.types.job.update instead."))
def update(
    api: API,
    resource_slug: str,
    job_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
) -> Job:
    """Make an update to a job entry.

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    job_slug: str
        identifier used to retrieve the job.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: {Optionapstr
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.

    Returns
    -------
    : Job
        The ``Job`` object
    """
    return job_update(
        api=api,
        resource_slug=resource_slug,
        job_slug=job_slug,
        parent_job_slug=parent_job_slug,
        external_identifier=external_identifier,
        status=status,
        remote_status=remote_status,
        job_data_schema=job_data_schema,
        job_data=job_data,
    )


@deprecated(reason=("Please use sw_product_lib.types.job.get instead."))
def get(
    api: API,
    resource_slug: str,
    id: str,
) -> Job:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        identifier for the resource.
    id: str
        the job_slug identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by the slug.
    """
    return job_get(api, resource_slug, id)


@deprecated(
    reason=("Please use sw_product_lib.types.job.get_by_external_identifier instead.")
)
def get_by_external_identifier(
    api: API,
    id: str,
) -> Optional[Job]:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    id: str
        the external_identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by id or None.
    """
    return job_get_by_external_id(api, id)


@deprecated(
    reason=("Please use sw_product_lib.types.job.get_by_external_identifier instead.")
)
def get_by_statuses(
    api: API, statuses: List[JobStatus]
) -> Optional[Dict[JobStatus, List[Job]]]:
    """Retrieve jobs filtered by job statuses.

    Parameters:
    ----------
    api: API
        provides access to the platform API.
    statuses: List[JobStatus]
        the statuses used to filter for jobs.

    Returns:
    ----------
    A dictionary where the jobs are grouped by statuses.
    The keys in the dictionary are the statuses.
    Each status has their list of jobs.

    Optional[Dict[JobStatus, List[Job]]]
    """
    return job_get_by_statuses(api, statuses)


@deprecated(reason=("Please use sw_product_lib.types.job.upload_file instead."))
def upload_file(
    api: API,
    resource_slug: str,
    job_slug: str,
    file_path: str,
    override_existing: bool = False,
    is_hidden: bool = False,
    is_public: bool = False,
    sort_weight: int = 0,
    file_name: Optional[str] = None,
    json_schema: Optional[str] = None,
    label: Optional[str] = None,
    content_type: Optional[str] = None,
) -> Tuple[File, str]:
    """Upload a file associated with a job.

    This function has been deprecated. Please use the upload_file function in the
    sw_product_lib.types.job module instead.
    """
    return job_upload_file(
        api=api,
        resource_slug=resource_slug,
        job_slug=job_slug,
        file_path=file_path,
        override_existing=override_existing,
        is_hidden=is_hidden,
        is_public=is_public,
        sort_weight=sort_weight,
        file_name=file_name,
        json_schema=json_schema,
        label=label,
        content_type=content_type,
    )


@deprecated(reason=("Please use sw_product_lib.types.job.add_tags instead."))
def add_tags(
    api: API,
    resource_slug: str,
    job_slug: str,
    tags: List[str],
) -> List[AppliedJobTag]:
    """Add tags to job

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used to identify the resource
    job_slug: str
        used to identify the job
    tags: List[str]
        a list of strings with which to tag the job

    Returns
    -------
    : Job
        The ``Job`` object with newly associated tags
    """
    return job_add_tags(api, resource_slug, job_slug, tags)
