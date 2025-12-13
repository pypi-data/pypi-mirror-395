from .module_imports import key
from uplink.retry.when import status_5xx
from uplink import (
    Consumer,
    get as http_get,
    post,
    patch,
    delete,
    returns,
    headers,
    retry,
    Body,
    json,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=20, when=status_5xx())
class Business_Information(Consumer):
    """Interface to Business Information resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def brands(self):
        return self.__Brands(self)

    def sites(self):
        return self.__Sites(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    @retry(max_attempts=20, when=status_5xx())
    class __Brands(Consumer):
        """Interface to Brands resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("business-information/brands")
        def list(self, name: Query = None):
            """This call will return a list of all brands."""

        @returns.json
        @http_get("business-information/brands/{uid}")
        def get(self, uid: str):
            """This call will return detailed information about a specific brand."""

        @delete("business-information/brands/{uid}")
        def delete(self, uid: str):
            """This call will delete the specified brand."""

        @returns.json
        @json
        @post("business-information/brands")
        def insert(self, brand: Body):
            """This call will create a new brand with the specified parameters."""

        @json
        @patch("business-information/brands/{uid}")
        def update(self, uid: str, brand: Body):
            """This call will update the specified brand with new parameters."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    @retry(max_attempts=20, when=status_5xx())
    class __Sites(Consumer):
        """Interface to Sites resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("business-information/sites")
        def list(self):
            """This call will return a list of all sites."""

        @returns.json
        @http_get("business-information/sites/{uid}")
        def get(self, uid: str):
            """This call will return detailed information about a specific site."""

        @delete("business-information/sites/{uid}")
        def delete(self, uid: str):
            """This call will delete the specified site."""

        @returns.json
        @json
        @post("business-information/sites")
        def insert(self, site: Body):
            """This call will create a new site with the specified parameters."""

        @json
        @patch("business-information/sites/{uid}")
        def update(self, uid: str, site: Body):
            """This call will update the specified site with new parameters."""

