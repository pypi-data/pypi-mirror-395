import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
from deprecated import deprecated
from strangeworks_core.errors.error import StrangeworksError
from strangeworks_core.platform import auth
from strangeworks_core.platform.gql import API, Operation
from strangeworks_core.types.file import File as FileBase
from strangeworks_core.types.job import Job as JobBase
from strangeworks_core.types.job import Status as JobStatus
from strangeworks_core.utils import str_to_datetime

from .resource import Resource


NON_TERMINAL_STATUSES = [JobStatus.CREATED, JobStatus.QUEUED, JobStatus.RUNNING]


class Job(JobBase):
    parent_job_slug: str | None = None
    resource: Resource | None = None

    def __init__(
        self,
        parentJob: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # if the job is from a graphql query, then the parent job slug will be in
        # parentJob.
        # if its from a job object represented as a dictionary, then the parent job
        # slug will be in kwargs as parent_job_slug.
        self.parent_job_slug = (
            parentJob.get("slug") if parentJob else kwargs.get("parent_job_slug")
        )

    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__


class File(FileBase):
    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class JobTag:
    id: str
    tag: str
    display_name: str
    tag_group: str

    def __init__(
        self,
        id: str,
        tag: str,
        displayName: str,
        tagGroup: str,
        **kvargs,
    ):
        self.id = id
        self.tag = tag
        self.display_name = displayName
        self.tag_group = tagGroup

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(**d)


class AppliedJobTag(JobTag):
    def __init__(
        self,
        isSystem: bool,
        dateCreated: datetime,
        tag: Dict[str, Any],
        **kwargs,
    ):
        super().__init__(**tag)
        self.is_system = isSystem
        self.date_created = str_to_datetime(dateCreated)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(**d)


create_request = Operation(
    query="""
            mutation jobCreate(
                $resource_slug: String!
                $workspace_member_slug: String!
                $parent_job_slug: String
                $external_identifier: String
                $status: JobStatus
                $remote_status: String
                $job_data_schema: String
                $job_data: JSON
            ) {
                jobCreate(
                    input: {
                        resourceSlug: $resource_slug
                        workspaceMemberSlug: $workspace_member_slug
                        parentJobSlug: $parent_job_slug
                        externalIdentifier: $external_identifier
                        status: $status
                        remoteStatus: $remote_status
                        jobDataSchema: $job_data_schema
                        jobData: $job_data
                    }
                ) {
                    job {
                        id
                        externalIdentifier
                        slug
                        status
                        isTerminalState
                        remoteStatus
                        jobDataSchema
                        jobData
                        parentJob {
                            slug
                        }
                    }
                }
            }
        """,
)


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
    *args,
    **kvargs,
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
    platform_result = api.execute(
        op=create_request,
        resource_slug=resource_slug,
        workspace_member_slug=workspace_member_slug,
        parent_job_slug=parent_job_slug,
        external_identifier=external_identifier,
        status=status,
        remote_status=remote_status,
        job_data_schema=job_data_schema,
        job_data=job_data,
    )

    return Job.from_dict(platform_result["jobCreate"]["job"])


update_request = Operation(
    query="""
            mutation jobUpdate(
                $job_slug: String!
                $parent_job_slug: String
                $external_identifier: String
                $status: JobStatus
                $remote_status: String
                $job_data_schema: String
                $job_data: JSON
            ) {
                jobUpdate(
                    input: {
                        jobSlug: $job_slug
                        parentJobSlug: $parent_job_slug
                        externalIdentifier: $external_identifier
                        status: $status
                        remoteStatus: $remote_status
                        jobDataSchema: $job_data_schema
                        jobData: $job_data
                    }
                ) {
                    job {
                        id
                        externalIdentifier
                        slug
                        status
                        isTerminalState
                        remoteStatus
                        jobDataSchema
                        jobData
                        parentJob {
                            slug
                        }
                        files {
                            file {
                                slug
                                id
                                label
                                fileName
                                url
                                dateCreated
                                dateUpdated
                            }
                        }
                    }
                }
            }
        """,
)


def update(
    api: API,
    job_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
    **kwargs,
) -> Job:
    """Make an update to a job entry.

    Parameters
    ----------
    api: API
        provides access to the platform API.
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
    platform_result = api.execute(
        op=update_request,
        **locals(),
    )
    return Job.from_dict(platform_result["jobUpdate"]["job"])


get_job_request = Operation(
    query="""
    query job($job_slug: String!) {
        job(jobSlug: $job_slug) {
            id
            childJobs {
                id
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
                files {
                    file {
                        slug
                        id
                        label
                        fileName
                        url
                        dateCreated
                        dateUpdated
                    }
                }
            }
            externalIdentifier
            slug
            status
            isTerminalState
            remoteStatus
            jobDataSchema
            jobData
            parentJob {
                slug
            }
            resource {
                slug
                apiRoute
            }
            files {
                file {
                    slug
                    id
                    label
                    fileName
                    url
                    dateCreated
                    dateUpdated
                }
            }
        }
    }
    """
)


def get(
    api: API,
    id: str,
    **kwargs,
) -> Job:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    id: str
        the job_slug identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by the slug.
    """
    platform_result = api.execute(
        op=get_job_request,
        job_slug=id,
    )
    return Job.from_dict(platform_result["job"])


get_jobs_request = Operation(
    query="""
        query jobs(
            $external_identifier: String,
            $resource_slug: String,
            $parent_job_slug: String,
            $statuses: [JobStatus!]
            $tags: [String!]
            $first: Int,
            $last: Int,
            $before: ID,
            $after: ID,
        ) {
            jobs(
                externalIdentifier: $external_identifier
                resourceSlug: $resource_slug
                parentJobSlug: $parent_job_slug
                statuses: $statuses
                jobTags: $tags
                pagination: {
                    before: $before
                    after: $after
                    first: $first
                    last: $last
                }
            ) {
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        id
                        slug
                        status
                        parentJob {
                            slug
                        }
                        resource {
                            slug
                            apiRoute
                        }
                        externalIdentifier
                        isTerminalState
                        remoteStatus
                        dateCreated
                        dateUpdated
                    }
                }
            }
        }
""",
)


def get_list(
    api: API,
    start_cursor: str = None,
    batch_size: int = 50,
    **kwargs,
) -> Tuple[List[Job], str, bool]:
    """Return list of jobs."""
    platform_result = api.execute(
        op=get_jobs_request, first=batch_size, after=start_cursor, **kwargs
    )
    if "jobs" not in platform_result:
        raise StrangeworksError(
            message="Missing field ('jobs') in response to jobs query",
            status_code=500,
        )
    edges = platform_result.get("jobs").get("edges")
    if edges is None:
        raise StrangeworksError(
            message="Missing field ('edges') in response to jobs query",
            status_code=500,
        )

    if len(platform_result["jobs"]["edges"]) == 0:
        return ([], None, False)

    jobs = [Job.from_dict(edge["node"]) for edge in edges if "node" in edge]
    cursor = platform_result.get("jobs").get("pageInfo").get("endCursor")
    has_next_page = platform_result.get("jobs").get("pageInfo").get("hasNextPage")
    return (jobs, cursor, has_next_page)


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
    as_list, _, _ = get_list(api=api, external_identifier=id)
    if len(as_list) > 1:
        raise StrangeworksError(
            message=f"More than one job returned for remote id {id}", status_code=500
        )
    return None if len(as_list) == 0 else as_list[0]


@deprecated(reason="This function is deprecated. Use job.get_list instead.")
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
    has_next_page: bool = True
    cursor: str = None
    jobs: List[Job] = []
    while has_next_page:
        jobs_batch, cursor, has_next_page = get_list(
            api=api, start_cursor=cursor, statuses=statuses
        )
        jobs.extend(jobs_batch)

    jobs_grouped_by_status = defaultdict(list)
    for job in jobs:
        jobs_grouped_by_status[JobStatus(job.status.strip().upper())].append(job)
    # ensure statuses with no jobs are in the dict
    statuses_with_no_jobs = set(statuses) - set(jobs_grouped_by_status.keys())
    for status in statuses_with_no_jobs:
        jobs_grouped_by_status[status]

    return jobs_grouped_by_status


upload_file_request = Operation(
    query="""
        mutation jobUploadFile(
            $resource_slug: String!,
            $job_slug: String!,
            $override_existing: Boolean!,
            $file_name: String!,
            $json_schema: String,
            $is_hidden: Boolean!,
            $sort_weight: Int!,
            $label: String,
            $content_type: String!,
            $meta_file_type: String,
            $meta_file_size: Int,
            $meta_file_create_date: Time,
            $meta_file_modified_date: Time,
            $is_public: Boolean! = false,
        ){
            jobUploadFile(
                input: {
                    resourceSlug: $resource_slug,
                    jobSlug: $job_slug,
                    shouldOverrideExistingFile: $override_existing,
                    fileName: $file_name,
                    jsonSchema: $json_schema,
                    isHidden: $is_hidden,
                    sortWeight: $sort_weight,
                    label: $label,
                    contentType: $content_type,
                    metaFileType: $meta_file_type,
                    metaFileSize: $meta_file_size,
                    metaFileCreateDate: $meta_file_create_date,
                    metaFileModifiedDate: $meta_file_modified_date,
                    isPublic: $is_public,
                }
            ){
                signedURL
                file {
                    id
                    slug
                    label
                    fileName
                    url
                    metaFileType
                    metaDateCreated
                    metaDateModified
                    metaSizeBytes
                    jsonSchema
                }
            }
        }
        """,
)


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

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        identifier for the resource.
    job_slug: str
        the strangeworks identefier of the job.
    file_path: str
        fully qualified path to the file.
    override_existing: bool
        If True, any existing file with the same name owned by this `Job`
          will be replaced with this file.
    is_hidden: bool
        If true, this file will not be displayed in the portal.
        This can be useful for supporting files that should be saved against the job,
          but typically would be referenced by URL in other contexts.
        (i.e.: an image file which is referenced in a JSON model.)
        This does **not*** prevent a user from accessing this file
          in other contexts, such as job archives.
    is_public: bool
        If True, this file may be accessed by the URL with no authentication.
        In general, most files should NOT be public.
    sort_weight: int
        This is the primary sorting instruction for JobFiles
         when returned to the client.
        The default is 0.
        Files with a higher sort order will be returned first.
        This allows you to control the order of files in the portal if desired.
    file_name: Optional[str]
        the name given to the file.
        This takes precedence over the name in file_path. Must be unique per Job.
    json_schema: Optional[str]
        A full URL to a JSON Schema document which will be used to
         label and validate the content of this file.
        If set, the system will assume the file contains JSON data.
        Please refer to documentation for common platform schemas.
    label: Optional[str]
        An optional label that will be displayed to users in the portal
         instead of the file name "Results 01", etc.
    content_type: Optional[str]
        Used to indicate the original media type of what is going to be uploaded.
        Defaults to `application/x-www-form-urlencoded`.

    Returns
    -------
    File
        The ``File`` object that contains platform information about the file.
    str
        A signed url where the file can be uploaded to.

    """
    p = Path(file_path)
    stats = p.stat()
    meta_size = stats.st_size
    meta_create_date = datetime.fromtimestamp(
        stats.st_ctime, tz=timezone.utc
    ).isoformat()
    meta_modified_date = datetime.fromtimestamp(
        stats.st_mtime, tz=timezone.utc
    ).isoformat()
    meta_type = p.suffix[1:]  # suffix without the .
    if meta_type == "" and file_name:
        # could be the case that p.suffix is coming from a temporary file
        # the temporary file can be without an extension
        # the user could have correctly named the file with an extension
        # so as a final attempt we try to pull the extension from the user file name
        _, ext = os.path.splitext(file_name)
        meta_type = ext[1:]  # again, without the .
    name = file_name or p.name
    ct = content_type or "application/x-www-form-urlencoded"
    res = api.execute(
        op=upload_file_request,
        resource_slug=resource_slug,
        job_slug=job_slug,
        file_name=name,
        override_existing=override_existing,
        json_schema=json_schema,
        is_hidden=is_hidden,
        sort_weight=sort_weight,
        label=label,
        is_public=is_public,
        content_type=ct,
        meta_file_type=meta_type,
        meta_file_size=meta_size,
        meta_file_create_date=meta_create_date,
        meta_file_modified_date=meta_modified_date,
    ).get("jobUploadFile")
    if not res:
        raise StrangeworksError(message="unable to get valid response from platform")

    if "error" in res:
        raise StrangeworksError(message=res.get("error"))
    f = res.get("file")
    signedUrl = res.get("signedURL")
    if not f or not signedUrl:
        raise StrangeworksError(
            message="unable to obtain file details or a place to upload the file"
        )
    return (File.from_dict(f), signedUrl)


tag_request = Operation(
    query="""
        mutation jobAddTags(
            $resource_slug: String!,
            $job_slug: String!,
            $tags: [String!]!,
            ){
            jobAddTags(
                input: {
                    resourceSlug: $resource_slug,
                    jobSlug: $job_slug,
                    tags: $tags }
            ) {
                tags {
                    tag {
                        displayName
                        id
                        tag
                        tagGroup
                    }
                    isSystem
                    dateCreated
                }
            }
        }
    """
)


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
    platform_result = api.execute(
        op=tag_request,
        **locals(),
    )

    if not platform_result:
        raise StrangeworksError(message="unable to get valid response from platform")
    if "error" in platform_result:
        raise StrangeworksError(message=platform_result.get("error"))

    return [
        AppliedJobTag.from_dict(tag) for tag in platform_result["jobAddTags"]["tags"]
    ]


def execute_subjob(
    parent_job_slug: str,
    api_key: str,
    proxy_auth_token: str,
    resource: Resource,
    path: Optional[str] = None,
    json: Optional[Any] = None,
    data: Optional[Any] = None,
    base_url: Optional[str] = None,
) -> Job:
    """Execute Sub-job."""
    if json is None and data is None:
        sub_job = requests.get(
            url=resource.proxy_url(base_url=base_url, path=path),
            headers={
                "Authorization": f"bearer {proxy_auth_token}",
                "x-resource-api-token": api_key,
                "x-strangeworks-parent-job-slug": parent_job_slug,
            },
        )
    else:
        sub_job = requests.post(
            url=resource.proxy_url(base_url=base_url, path=path),
            headers={
                "Authorization": f"bearer {proxy_auth_token}",
                "x-resource-api-token": api_key,
                "x-strangeworks-parent-job-slug": parent_job_slug,
            },
            json=json,
            data=data,
        )

    return sub_job


def get_job_file(
    api_key: str,
    file_path: str,
    base_url: Optional[str] = None,
) -> Job:
    """Return a Job File."""

    authtoken = auth.get_token(
        api_key=api_key,
        base_url=base_url,
        auth_url="product/token",
    )
    file_url = urljoin(base_url, file_path)
    if "files/jobs/" in file_url:
        # Work around for platform bug.
        file_url = file_url.replace("files/", "", 1)
    res = requests.get(url=file_url, headers={"Authorization": f"bearer {authtoken}"})
    return res
