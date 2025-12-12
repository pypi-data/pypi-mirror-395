"""submitter.py.

Handles the job creation aspects of an application.
"""

import functools
import logging
from typing import Any, Callable, ParamSpec, Protocol, TypeVar

from fastapi import BackgroundTasks
from strangeworks_core.errors.error import StrangeworksError

from sw_product_lib import service
from sw_product_lib.apps.context import UserRequestContext
from sw_product_lib.types import Job, JobStatus

from ..types import ArtifactGenerator, HTTPRequest, HTTPSubmitter, RemoteJobResponse


logger = logging.getLogger(__name__)


class JobSubmitter(Protocol):
    def __call__(
        self,
        ctx: UserRequestContext,
        job_request: HTTPRequest,
        *args: Any,
        **kwargs: Any,
    ) -> RemoteJobResponse:
        ...


P = ParamSpec("P")
N = TypeVar("N", int, float)
CostEstimator = Callable[P, N]


def _submitter(
    _func=None,
    *,
    cost_estimator: CostEstimator | None = None,
    artifact_generator: ArtifactGenerator | None = None,
):
    """
    Uses the given function to generate a job submitter on the Strangeworks platform.
    The function being decorated must be of type HTTPSubmitter.

    Use an artifact generator only if generating artifacts is a "lightweight" operation.

    ### Example
    ```python
    @job_submitter
    def submit_job(payload, headers) -> RemoteJobResponse:
        # submit a request to ibm and return result object as
        res = requests.post(provider_url, headers, payload)
        res_payload = res.json()
        remote_id = res_payload.get("id")
        return RemoteJobResponse.from_requests_result(res, remote_job_id=remote_id)
    ```

    Parameters
    ----------
    cost_estimator: CostEstimator
        A function that estimates the cost that will be incurred from the job request.
    artifact_generator: ArtifactGenerator
        If one is provided, will be scheduled as a background task.
    """

    def _decorator_job_submitter(func: HTTPSubmitter) -> JobSubmitter:
        @functools.wraps(func)
        def _wrapper_job_submitter(
            *args,
            ctx: UserRequestContext,
            job_request: HTTPRequest,
            bg_tasks: BackgroundTasks | None = None,
            **kwargs,
        ):
            sw_job: Job = service.create_job(ctx)  # type: ignore
            #
            # add tags to job if any provided
            #
            try:
                tags = kwargs.pop("tags", None)
                # add tags to job if any provided
                if tags:
                    logger.debug(f"adding job tags {tags}")
                    service.add_job_tags(ctx, sw_job.slug, tags=tags)
            except StrangeworksError as se:
                # unable to add job tags for some reason. log as error and continue.
                logger.error("unable to add job tags {tags} for {sw_job.slug})")
                logger.exception(se)
            #
            # save request
            #
            try:
                service.upload_job_artifact(
                    job_request.model_dump_json(),
                    job_slug=sw_job.slug,
                    ctx=ctx,
                    file_name="job_submit_request.json",
                    job=sw_job,
                )
            except StrangeworksError as se:
                # unable to save the request. log the error but continue processing
                logger.error(
                    "error uploading job request as artifact of job {sw_job.slug}"
                )
                logger.exception(se)
            #
            # generate cost estimate and request job clearance. If any errors are
            # raised during this phase are terminal.
            #
            cost_estimate = cost_estimator(job_request) if cost_estimator else 0.0
            try:
                if not service.request_job_clearance(
                    ctx=ctx, amount=cost_estimate  # type: ignore[misc]
                ):
                    # did not get clearance. update job status to failed and raise
                    # error.
                    try:
                        service.update_job(
                            ctx=ctx,
                            job_slug=sw_job.slug,
                            status=JobStatus.FAILED,
                        )
                    except Exception as ex:
                        # do not allow an exception from update_job shadow the
                        # job clearance.
                        logging.error(
                            f"Error updating job status for failed job clearance {sw_job.slug}"  # noqa
                        )
                        logging.exception(ex)

                    raise StrangeworksError(
                        f"Job clearance denied for {ctx.resource_slug} (job slug: {sw_job.slug})"  # noqa
                    )
            except Exception as err:
                # erroring while trying to get job clearance is a terminal error.
                service.update_job(
                    ctx=ctx,
                    job_slug=sw_job.slug,
                    status=JobStatus.FAILED,
                )
                raise StrangeworksError(
                    f"job clearance request failed {ctx.resource_slug}. (job slug: {sw_job.slug})"  # noqa
                ) from err
            # submit request to remote system.
            try:
                logging.info(f"submitting job request (job slug: {sw_job.slug})")
                submit_response: RemoteJobResponse = func(job_request, *args, **kwargs)
                # update sw_job
                job_updates: dict[str, Any] = {"status": submit_response.sw_status}
                if submit_response.remote_job_id:
                    job_updates["external_identifier"] = submit_response.remote_job_id
                if submit_response.remote_status:
                    job_updates["remote_status"] = submit_response.remote_status
                sw_job = service.update_job(
                    ctx=ctx,
                    job_slug=sw_job.slug,
                    **job_updates,
                )
            except Exception as err:
                # errors submitting request or not updating the job with the remote job
                # id are terminal errors. try updating job status and raise an error.
                try:
                    service.update_job(
                        ctx=ctx,
                        job_slug=sw_job.slug,
                        status=JobStatus.FAILED,
                    )
                except Exception as juerr:
                    logger.error(
                        f"unable to update job with remote submit error {sw_job.slug}"
                    )
                    logger.exception(juerr)
                    raise StrangeworksError(
                        f"Error during job submission on remote system. Unable to update job status {sw_job.slug}"  # noqa
                    ) from err
                raise StrangeworksError(
                    f"Error during job submission on remote system ({sw_job.slug})"
                ) from err
            # save the job submission response.
            try:
                service.upload_job_artifact(
                    submit_response.model_dump_json(),
                    job_slug=sw_job.slug,
                    ctx=ctx,
                    file_name="job_submit_response.json",
                    job=sw_job,
                    is_hidden=True,
                )
            except Exception as ex:
                # unable to upload response. log and continue.
                logger.error(f"unable to upload job submission response {sw_job.slug}")
                logger.exception(ex)
            #
            # set up artifact generator as a background task if one provided ...
            #
            try:
                if artifact_generator:

                    def fn():
                        for portal_artifact in artifact_generator(
                            request=job_request, response=submit_response
                        ):  # type: ignore
                            service.upload_job_artifact(
                                portal_artifact,
                                ctx=ctx,
                                job_slug=sw_job.slug,
                                job=sw_job,
                            )

                    (
                        bg_tasks.add_task(func=fn)
                        if bg_tasks
                        else logger.warning(
                            "unable to artifact generator without background tasks"
                        )
                    )
            except Exception as err:
                # error with artifact generator. non-terminal error.
                # log information and continue.
                logger.error(f"unable to run artifact generator {sw_job.slug}")
                logger.exception(err)
            finally:
                return submit_response

        return _wrapper_job_submitter  # type: ignore

    if _func is None:
        return _decorator_job_submitter
    else:
        return _decorator_job_submitter(_func)
