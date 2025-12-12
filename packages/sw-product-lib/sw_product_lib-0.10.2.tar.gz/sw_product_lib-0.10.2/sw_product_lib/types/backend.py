"""backend.py."""
from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field
from strangeworks_core.errors.error import StrangeworksError
from strangeworks_core.platform.gql import API, Operation
from strangeworks_core.types.backend import Backend as BackendBase
from strangeworks_core.types.backend import Status


class AppliedBackendTag(BaseModel):
    id: str
    tag: str
    is_system: bool = Field(alias=AliasChoices("is_system", "isSystem"))
    display_name: str | None = Field(
        default=None, alias=AliasChoices("display_name", "displayName")
    )
    tag_group: str | None = Field(
        default=None, alias=AliasChoices("tag_group", "tagGroup")
    )


class BackendType(BaseModel):
    id: str
    slug: str
    display_name: str | None = Field(
        default=None, alias=AliasChoices("display_name", "displayName")
    )
    description: str | None = None
    schema_url: str | None = Field(
        default=None, alias=AliasChoices("schema_url", "schemaURL")
    )


class BackendTypeInput(BaseModel):
    typeSlug: str = Field(alias=AliasChoices("slug", "type_slug", "typeSlug"))
    data: dict


class BackendUpdateInput(BaseModel):
    """Backend Update Inputs.

    Each object is for an update of a single backend identified by backendSlug. One or
    more fields can be updated per request.
    """

    backendSlug: str
    data: dict | None = None
    dataSchema: str | None = None
    name: str | None = None
    remoteBackendId: str | None = None
    remoteStatus: str | None = None
    status: Status | None = None


class BackendCreateInput(BaseModel):
    """Inputs for Creating a New Backend.

    The fields name, remoteBackendId, and status are mandatory.
    """

    name: str
    remoteBackendId: str
    status: Status
    remoteStatus: str | None = None
    data: dict | None = None
    dataSchema: str | None = None


class BackendRegistration(BaseModel):
    backend_type_id: str = Field(alias=AliasChoices("backend_type_id", "backendTypeId"))
    backend_type: BackendType = Field(alias=AliasChoices("backend_type", "backendType"))
    data: dict | None = None
    date_created: datetime | None = Field(
        default=None, alias=AliasChoices("date_created", "dateCreated")
    )
    date_updated: datetime | None = Field(
        default=None, alias=AliasChoices("date_updated", "dateUpdated")
    )


class Backend(BackendBase):
    backend_registrations: list[BackendRegistration] | None = Field(
        default=None,
        alias=AliasChoices("backend_registrations", "backendRegistrations"),
    )
    tags: list[AppliedBackendTag] | None = None

    @classmethod
    def from_dict(cls, res: dict):
        return cls(**res)


get_all_strangeworks_backends_request = Operation(
    query="""
        query backends(
            $product_slugs: [String!],
            $backend_type_slugs: [String!],
            $backend_statuses: [BackendStatus!],
            $backend_tags: [String!]) {
                backends(
                    productSlugs: $product_slugs,
                    backendTypeSlugs: $backend_type_slugs,
                    backendStatuses: $backend_statuses,
                    backendTags: $backend_tags){
                        id,
                        name,
                        status,
                        remoteBackendId,
                        remoteStatus,
                        slug,
                    }
                }
    """
)


def get_backends(
    api: API,
    product_slugs: list[str] = None,
    backend_type_slugs: list[str] = None,
    backend_statuses: list[str] = None,
    backend_tags: list[str] = None,
) -> list[Backend]:
    """Retrieve a list of available backends."""
    backends_response = api.execute(
        op=get_all_strangeworks_backends_request,
        **locals(),
    )
    return [Backend.from_dict(b) for b in backends_response["backends"]]


get_backends_request = Operation(
    query="""
    query v($status: BackendStatus, $remote_backend_id: String) {
    viewer {
        backends(status: $status, remoteBackendId: $remote_backend_id) {
            id
            slug
            name
            status
            remoteBackendId
            remoteStatus
            data
            dataSchema
            dateRefreshed
            backendRegistrations {
                backendType {
                    id
                    schemaURL
                    slug
                    displayName
                    description
                }
                backendTypeId
                data
            }
        }
    }
    }
    """,
)


def get_product_backends(
    api: API,
    status: str = None,
    remote_backend_id: str = None,
) -> list[Backend]:
    """Fetch backends for product

    Parameters
    ----------
    api: API
        provides access to the product API
    status: str
        filter by backend status
    remote_backend_id: str
        filter by the backend id set by the product

    Returns
    -------
    List[Backend]
        The list of backends filtered by the params
    """
    platform_res = api.execute(
        op=get_backends_request, status=status, remote_backend_id=remote_backend_id
    )
    return [Backend.from_dict(b) for b in platform_res["viewer"]["backends"]]


backend_add_type_mutation = Operation(
    query="""
    mutation backendAddTypes(
        $backend_slug: String!,
        $backend_types: [BackendTypeInput!]
        ){
        backendAddTypes(input: {
            backendSlug: $backend_slug,
            backendTypes: $backend_types
        }) {
            backendSlug
            backendTypeSlugs
        }
    }
    """,
)


def backend_add_types(
    api: API,
    backend_slug: str,
    backend_types: list[BackendTypeInput],
) -> None:
    platform_res = api.execute(
        op=backend_add_type_mutation,
        backend_slug=backend_slug,
        backend_types=[t.model_dump(mode="json") for t in backend_types],
    )
    if "backendAddTypes" not in platform_res:
        raise StrangeworksError.server_error(f"invalid response {platform_res}")


backend_remove_types_mutation = Operation(
    query="""
    mutation backendRemoveTypes($backend_slug: String!, $backend_type_slugs: [String!]){
        backendRemoveTypes(input: {
            backendSlug: $backend_slug,
            backendTypeSlugs: $backend_type_slugs
        }) {
            backendSlug
            backendTypeSlugs
        }
    }
    """,
)


def backend_remove_types(
    api: API,
    backend_slug: str,
    backend_type_slugs: list[str],
) -> None:
    platform_res = api.execute(
        op=backend_remove_types_mutation,
        backend_slug=backend_slug,
        backend_type_slugs=backend_type_slugs,
    )
    if "backendRemoveTypes" not in platform_res:
        raise StrangeworksError.server_error(f"invalid response {platform_res}")


backend_create_mutation = Operation(
    query="""
    mutation backendCreate($backends: [ProductBackendInput!]){
        backendCreate(input: {backends: $backends}) {
            backends {
                id
                slug
                name
                status
                remoteBackendId
                remoteStatus
                data
                dataSchema
                dateRefreshed
                backendRegistrations {
                    backendType {
                        id
                        schemaURL
                        slug
                        displayName
                        description
                    }
                    backendTypeId
                    data
                }
            }
        }
    }
    """
)


def backend_create(
    api: API,
    payload: list[BackendCreateInput],
) -> list[Backend]:
    backends = [b.model_dump(mode="json") for b in payload]
    platform_res = api.execute(
        op=backend_create_mutation,
        backends=backends,
    )

    if (
        "backendCreate" not in platform_res
        or "backends" not in platform_res["backendCreate"]
    ):
        raise StrangeworksError.server_error(f"invalid response {platform_res}")
    res = [
        Backend.from_dict(backend_dict)
        for backend_dict in platform_res["backendCreate"]["backends"]
    ]
    return res


backend_delete_mutation = Operation(
    query="""
    mutation backendDelete($backend_slug: String!){
        backendDelete(input: { backendSlug: $backend_slug })
    }
    """,
)


def backend_delete(
    api: API,
    backend_slug: str,
) -> None:
    api.execute(op=backend_delete_mutation, backend_slug=backend_slug)


backend_update_mutation = Operation(
    query="""
    mutation backendUpdate($backends: [ProductBackendUpdateInput!]){
        backendUpdate(input: {backends: $backends}) {
            backends {
                id
                slug
                name
                status
                remoteBackendId
                remoteStatus
                data
                dataSchema
                dateRefreshed
                backendRegistrations {
                    backendType {
                        id
                        schemaURL
                        slug
                        displayName
                        description
                    }
                    backendTypeId
                    data
                }
            }
        }
    }
    """,
)


def backend_update(
    api: API,
    backend_update_input: list[BackendUpdateInput],
) -> Backend:
    backends = [update.model_dump(mode="json") for update in backend_update_input]

    platform_res = api.execute(op=backend_update_mutation, backends=backends)
    if (
        "backendUpdate" not in platform_res
        and "backends" not in platform_res["backendUpdate"]
    ):
        raise StrangeworksError.server_error(f"invalid response {platform_res}")
    return [Backend.from_dict(res) for res in platform_res["backendUpdate"]["backends"]]
