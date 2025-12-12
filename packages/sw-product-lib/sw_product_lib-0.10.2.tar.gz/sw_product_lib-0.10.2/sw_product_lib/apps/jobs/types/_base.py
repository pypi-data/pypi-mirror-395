"""types.py."""

from typing import Any, Protocol

from pydantic import BaseModel
from requests import Response

from sw_product_lib.types.job import JobStatus


class HTTPRequest(BaseModel):
    """Denotes the Request to the Remote Service."""

    url: str
    method: str = "GET"
    kwargs: dict[str, Any] | None = None


class RemoteResponse(BaseModel):
    """Response from Remote Job Submission

    Doesn't support streaming payloads yet.
    """

    json_content: dict | None = None
    text_content: str | None = None
    content_type: str | None = None
    status: int = 200
    headers: dict[str, str] = {}
    encoding: str = "utf-8"

    @classmethod
    def _parse_requests_response(cls, response: Response) -> dict:
        # octet-stream can be interpreted as we may not know what the content
        # type is.
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        args: dict[str, Any] = {"content_type": content_type.strip()}

        if "application/json" in content_type:
            args["json_content"] = response.json()
        elif "text/" in content_type:
            args["text_content"] = response.text

        args["status"] = response.status_code
        args["headers"] = response.headers
        args["encoding"] = response.encoding
        return args

    @classmethod
    def from_requests_response(cls, response: Response, **kwargs):
        """Generate Object from Response."""
        args = cls._parse_requests_response(response)
        all_args = args | kwargs
        return cls(**all_args)


class RemoteJobResponse(RemoteResponse):
    """Object with Job Submit Response.

    No matter the operation, the response must have a remote_job_id.
    """

    remote_job_id: str
    remote_status: str | None = None
    sw_status: JobStatus = JobStatus.CREATED

    def result(self):
        if self.status == 200:
            if self.json_content:
                return self.json_content
            if self.text_content:
                return self.text_content
        return None


class HTTPSubmitter(Protocol):
    def __call__(
        self, job_request: HTTPRequest, *args: Any, **kwargs: Any
    ) -> RemoteJobResponse:
        ...
