"""gql.py."""
from strangeworks_core.platform.gql import API, APIInfo


class ProductAPI(API):
    """Wrapper for base API class to provide access to the Product API."""

    def __init__(self, **kwargs):
        kwargs.pop("api_type") if "api_type" in kwargs else None
        super().__init__(api_type=APIInfo.PRODUCT, **kwargs)
