"""artifact.py."""

from typing import Any, Iterator, Protocol

from pydantic import BaseModel

from ._base import HTTPRequest, RemoteJobResponse


class Artifact(BaseModel):
    """Job Artifact Model

    Artifacts are items generated during job exectution which we are interesting in
    saving. A job result is an example of an artifact. Artifacts may generated as value
    add-ons from items associated with a job. For example, an artifact of a circuit
    diagram can be generted and saved from the circuit information in the  initial job
    request.

    Attributes
    ----------
    data: Any
        Artifact contents. Uploaded as job file.
    name: str
        Name for the artifact.
    """

    data: Any
    name: str | None = None


class PortalFile(Artifact):
    """Artifact with Additional Attributes for Portal.

    These attributes inform the portal how to handle the file.

    Attributes
    ----------
    artifact_schema: str| None = None
        URL to a JSON Schema document which will be used to label and validate the
        content of this file. Defaults to None.
    label: str | None = None
        If specified, the label is presented in the portal as the file name. Defaults
        to None.
    url: str | None = None
        A full url to download the file. Authorization is required to access the file
        if it is not public. Defaults to None.
    file_slug: str | None = None
        Unique, URL-friendly identifier.
    sort_weight: int = 0
        Indicates the sort order for this file in lists. Higher is displayed first.
    overwrite: bool = False
        Indicates whether an identical file already in the workspace should be
        overwritten with this one. Defaults to False
    is_hidden: bool = False
        If true, this file will not be displayed in the portal. There is currently
        no method on any of the APIs (sdk, platform, product) to access a file whose
        is_hidden attribute is set to True. Defaults to False.
    """

    artifact_schema: str | None = None
    label: str | None = None
    url: str | None = None
    file_slug: str | None = None
    sort_weight: int = 0
    overwrite: bool = False
    is_hidden: bool = False


class ArtifactGenerator(Protocol):
    def __call__(
        self,
        *,
        request: HTTPRequest | None = None,
        response: RemoteJobResponse | None = None,
        **kwargs
    ) -> Iterator[PortalFile]:
        ...
