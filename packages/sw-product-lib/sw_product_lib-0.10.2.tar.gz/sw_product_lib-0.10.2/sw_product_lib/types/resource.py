from __future__ import annotations

import json
from typing import List, Optional

from strangeworks_core.platform.gql import API, Operation
from strangeworks_core.types.resource import Resource as ResourceBase
from strangeworks_core.types.resource import ResourceConfiguration


class Resource(ResourceBase):
    api_url: str | None = None


create_req = Operation(
    query="""
        mutation resourceCreate(
            $activation_id: String!,
            $status: ResourceStatus!,
            $api_route: String,
            $configurations: [StoreConfigurationInput!],
        ){
            resourceCreate(input: {
                resourceActivationId: $activation_id,
                status: $status,
                api_route: $api_route,
                resourceConfigurations: $configurations,
            }) {
                resource {
                id
                slug
                isDeleted
                status
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
              }
            }
        }
        """
)


def create(
    api: API,
    activation_id: str,
    status: str,
    api_route: Optional[str] = None,
    configurations: Optional[List[ResourceConfiguration]] = None,
) -> Resource:
    """Create a new resource definition on the platform.

    Parameters
    ----------
     api: API
        provides access to the platform API.
    """
    api_args = {
        "activation_id": activation_id,
        "status": status,
        "api_route": api_route,
    }

    if configurations:
        for _cfg in configurations:
            if _cfg.valueJson and isinstance(_cfg.valueJson, dict):
                _cfg.valueJson = json.dumps(_cfg.valueJson)
        api_args["configurations"] = [x.model_dump() for x in configurations]
    result = api.execute(
        op=create_req,
        **api_args,
    )

    return Resource.from_dict(result["resourceCreate"]["resource"])


list_req = Operation(
    query="""
        query resources($status_list: [ResourceStatus!]){
            resources(status: $status_list) {
                id
                slug
                status
                isDeleted
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
        """
)


def fetch(
    api: API,
    status_list: Optional[List[str]] = None,
) -> Optional[List[Resource]]:
    """Retrieve a list of available resources.

    Parameters
    ----------
    status_list: Optional(List[str])
        retrieve only those resources whose status is included in this list.
    """
    result = api.execute(op=list_req, **locals())
    return list(map(lambda x: Resource.from_dict(x), result["resources"]))


store_config_op = Operation(
    query="""
        mutation resourceStoreConfiguration(
            $key: String!,
            $resource_slug: String!,
            $type: ResourceConfigurationValueType!,
            $isEditable: Boolean!,
            $isInternal: Boolean!,
            $valueBool: Boolean,
            $valueString: String,
            $valueSecure: String,
            $valueInt: Int,
            $valueJson: String,
            $valueDate: Time,
            $valueFloat: Float,
        ){
            resourceStoreConfiguration(
                input: {
                    resourceSlug: $resource_slug,
                    configuration: {
                        key: $key,
                        type: $type,
                        isEditable: $isEditable,
                        isInternal: $isInternal,
                        valueBool: $valueBool,
                        valueString: $valueString,
                        valueSecure: $valueSecure,
                        valueInt: $valueInt,
                        valueJson: $valueJson,
                        valueDate: $valueDate,
                        valueFloat: $valueFloat,
                    }
                }
            ) {
                resourceConfiguration {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
        """,
)


def store_config(
    api: API,
    resource_slug: str,
    config: ResourceConfiguration,
) -> Resource:
    params = config.model_dump()
    # graphql mutation requires string representation of the object.
    if "valueJson" in params and isinstance(params.get("valueJson"), dict):
        _tmp = params["valueJson"]
        params["valueJson"] = json.dumps(_tmp)
    params["resource_slug"] = resource_slug
    api.execute(op=store_config_op, **params)
    # instead of the response, retrieve the resource which should now have
    # configuration and return that.
    return get(
        api=api,
        resource_slug=resource_slug,
    )


get_op = Operation(
    query="""
        query resource($resource_slug: String!) {
            resource(resourceSlug: $resource_slug){
                id
                slug
                status
                isDeleted
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
    """,
)


def get(
    api: API,
    resource_slug: str,
) -> Resource:
    """Retrieve a resource entry from platform."""
    raw_result = api.execute(
        op=get_op,
        resource_slug=resource_slug,
    )
    return Resource(**raw_result["resource"])


reset_cfg_op = Operation(
    query="""
        mutation reset(
            $resource_slug: String!,
        ) {
        resourceResetConfiguration(input: {resourceSlug: $resource_slug})
        }
    """,
)


def reset_config(
    api: API,
    resource_slug: str,
) -> Resource:
    """Clear out Configuration Items for Resource.

    Parameters
    ----------
    api : API
        _description_
    resource_slug : str
        _description_
    """
    api.execute(
        op=reset_cfg_op,
        resource_slug=resource_slug,
    )
    return get(
        api=api,
        resource_slug=resource_slug,
    )
