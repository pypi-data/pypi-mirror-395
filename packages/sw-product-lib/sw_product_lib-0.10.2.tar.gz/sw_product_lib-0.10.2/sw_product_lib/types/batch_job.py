from typing import Optional

from strangeworks_core.batch.utils import send_batch_request
from strangeworks_core.platform.gql import API, Operation
from strangeworks_core.types.batch import Options
from strangeworks_core.types.func import Func
from strangeworks_core.types.machine import Accelerator, Machine


def new(
    api: API,
    resource_slug: str,
    decorator_name: str,
    func: Func,
    machine: Optional[Machine] = None,
    accelerator: Optional[Accelerator] = None,
    job_slug: Optional[str] = None,
    workspace_member_slug: Optional[str] = None,
    options: Optional[Options] = None,
    **kwargs
) -> str:
    """
    Create a new batch job.

    Parameters
    ----------
    api : API
        The strangeworks platform API object.
    resource_slug : str
        The resource slug.
    decorator_name : str
        The decorator name.
    func : Func
        The function to run.
    machine : Optional[Machine]
        The machine to run the job on.
    accelerator : Optional[Accelerator]
        The accelerator to run the job on.
    job_slug : Optional[str]
        The job slug. Associate the batch job with a strangeworks job.
    workspace_member_slug : Optional[str]
        The workspace member slug. Associate the batch job with a workspace member.
    options : Optional[Options]
        The batch job options.
    **kwargs: dict
        Additional keyword arguments.

    Returns
    -------
    batch_job_slug: str

    """

    init_batch_job = Operation(
        query="""
        mutation batchJobInitiateCreate(
            $init: InitiateBatchJobCreateInput!
            $resource_slug: String!
            $job_slug: String
            $workspace_member_slug: String
        ){
            batchJobInitiateCreate(
                input: {
                    initiate: $init
                    resourceSlug: $resource_slug
                    jobSlug: $job_slug
                    workspaceMemberSlug: $workspace_member_slug
                }
            ) {
                batchJobSlug
                signedURL
            }
        }
        """
    )

    return send_batch_request(
        api,
        init_batch_job,
        decorator_name,
        func,
        machine,
        accelerator,
        resource_slug=resource_slug,
        job_slug=job_slug,
        workspace_member_slug=workspace_member_slug,
        options=options,
        **kwargs
    )
