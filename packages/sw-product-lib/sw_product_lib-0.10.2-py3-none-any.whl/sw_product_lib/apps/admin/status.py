"""Status Update objects and function types."""
from abc import ABC, abstractmethod
from typing import Any, Callable

from pydantic import BaseModel
from strangeworks_core.types.backend import Status as BackendStatus


"""Status Converter.

Converts remote status to a Strangeworks platform status. For now, these are Job and
Backend statuses.

Parameters
----------
remote_status: str | dict
    remote status of object.

Return
------
: Any
    A Strangeworks platform status type.
"""
StatusConverter = Callable[[str | dict], Any]


class BaseStatusUpdate(BaseModel, ABC):
    """Base class represending a status update for a remote object."""

    remote_id: str
    remote_status: str | dict

    @abstractmethod
    def status(self):
        """Return Status as Strangeworks platform type.

        Currently the status returned is for Job or Backends.
        """
        ...


class StatusUpdate(BaseStatusUpdate, BaseModel):
    """Class representing a status update for a remote object.

    If a StatusConverter function is provided as initialization, it
    will be used to convert the remote status to a strangeworks platform
    status. A NotImplementedError will be raised if no such function
    is provided.
    """

    status_converter: StatusConverter | None = None

    def status(self):
        """Return Strangeworks Status."""
        if self.status_converter:
            return self.status_converter(self.remote_status)
        raise NotImplementedError(
            "method for converting to strangeworks status not found."
        )

    def __str__(self):
        """Return string representation of StatusUpdate."""
        return f"remote_id: {self.remote_id}, remote_status: {self.remote_status}"


class BackendUpdate(StatusUpdate, BaseModel):
    """Helper class for handling backend status updates.

    This helper class will return an UNKNOWN status by default instead of raising
    a NotImplementedError when status is called. Either provide this class with a
    StatusConverter function at initialization or extend it to add additional
    functionality.
    """

    data: dict | None = None
    name: str | None = None
    data_schema: str | None = None

    def status(self):
        try:
            return super().status()
        except NotImplementedError:
            ...
        return BackendStatus.UNKNOWN


"""StatusPoller

Defines a function that retrieves a list of status updates from a remote source.
"""
StatusPoller = Callable[[], list[StatusUpdate]]
