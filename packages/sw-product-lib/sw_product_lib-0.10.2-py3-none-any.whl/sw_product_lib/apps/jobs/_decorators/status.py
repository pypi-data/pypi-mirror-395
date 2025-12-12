"""status.py."""

import functools
import logging

from fastapi import BackgroundTasks
from strangeworks_core.types.job import Job

from sw_product_lib import service
from sw_product_lib.apps.context import UserRequestContext

from ..types import ArtifactGenerator, HTTPRequest, HTTPSubmitter, RemoteJobResponse


logger = logging.getLogger(__name__)


def status_updater(
    _func=None,
    *,
    artifact_generator: ArtifactGenerator | None = None,
):
    """Handle Job Updates

    Wrap the given function to handle the Strangeworks job status update.

    Use an artifact generator only if generating artifacts is a "lightweight" operation.

    ###Example
    ```python
    @status_updater
    def get_status(req: HTTPRequest) -> RemoteJobResponse:
        ...

    Parameters
    ----------
    artifact_generator: ArtifactGenerator
        If one is provided, will be scheduled as a background task.
    """

    def _decorator(func: HTTPSubmitter):
        @functools.wraps(func)
        def _wrapper(
            *args,
            ctx: UserRequestContext,
            http_request: HTTPRequest,
            bg_tasks: BackgroundTasks | None = None,
            **kwargs,
        ):
            #
            # send status update request
            #
            status_update: RemoteJobResponse = func(http_request, *args, **kwargs)
            # if a status update request is successful, return the status update
            # no matter what happens.
            #
            # update job status.
            #
            # return response even if errors are encountered.
            #
            try:
                #
                # defensive programming here with the remote_id
                #
                remote_id: str | None = status_update.remote_job_id
                if not remote_id:
                    logger.error("unable to update job status: missing remote job id")
                    return
                #
                # find corresponding strangeworks job.
                # if job is not found, log it and return
                sw_job: Job | None = service.get_job_by_external_identifier(
                    ctx, remote_id
                )
                if not sw_job:
                    logger.error(
                        "unable to update job status: cannot find job for remote id {remote_id}"  # noqa
                    )
                    return

                logger.info(
                    f"updating job status {sw_job.slug} (remote_id: {remote_id}) to {status_update.sw_status}"  # noqa
                )
                #
                # capture and log any error while trying to update job status
                #
                try:
                    service.update_job(
                        ctx,
                        job_slug=sw_job.slug,
                        status=status_update.sw_status,
                        remote_status=status_update.remote_status,
                    )
                except Exception as ju_ex:
                    logger.error(f"error updating job status {sw_job.slug}")
                    logger.exception(ju_ex)
                #
                # set up artifact generator as a background task if one provided.
                # log any errors
                #
                try:
                    if artifact_generator:

                        def fn():
                            for portal_artifact in artifact_generator(
                                request=http_request,
                                response=status_update,
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
                return status_update

        return _wrapper

    if _func is None:
        return _decorator
    else:
        return _decorator(_func)


def result_fetcher(
    _func=None,
    *,
    artifact_generator: ArtifactGenerator | None = None,
):
    """Handle Fetching Job Result Requests.

    Wrap given function which can retrieve a remote job result with operations to
    upload the job result to the associated job object in the Strangeworks platform.

    Use an artifact generator only if generating artifacts is a "lightweight" operation.

    Parameters
    ----------
    artifact_generator: ArtifactGenerator | None

    """

    def _decorator(func: HTTPSubmitter):
        @functools.wraps(func)
        def _wrapper(
            *,
            ctx: UserRequestContext,
            http_request: HTTPRequest,
            bg_tasks: BackgroundTasks | None = None,
            **kwargs,
        ):
            job_result: RemoteJobResponse = func(job_request=http_request, **kwargs)
            # if we got this far, return the result even if unable to upload
            # job result or run the artifact generator (if one was supplied)
            try:
                #
                # being really defensive here with remote id
                #
                remote_id = job_result.remote_job_id
                if not remote_id:
                    logger.error("unable to update job status: missing remote job id")
                    return
                #
                # find corresponding strangeworks job.
                # if job is not found, log it and return
                sw_job: Job | None = service.get_job_by_external_identifier(
                    ctx, remote_id
                )
                if not sw_job:
                    logger.error(
                        "unable to upload result: cannot find job for remote id {remote_id}"  # noqa
                    )
                    return
                #
                # capture and log any error while tring to upload job result
                #
                try:
                    service.upload_job_artifact(
                        job_result.result(),
                        ctx=ctx,
                        job_slug=sw_job.slug,
                        file_name="result.json",
                    )
                except Exception as uj_ex:
                    logger.error(f"error uploading result for {sw_job.slug}")
                    logger.exception(uj_ex)
                #
                # capture and log any error with artifact generator (if one provided)
                #
                try:
                    if artifact_generator:

                        def fn():
                            for portal_artifact in artifact_generator(
                                request=http_request,
                                response=job_result,
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
                return job_result

        return _wrapper

    if _func is None:
        return _decorator
    else:
        return _decorator(_func)
