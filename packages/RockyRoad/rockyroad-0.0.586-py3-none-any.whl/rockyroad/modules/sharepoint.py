from .module_imports import get_key
from uplink.retry.when import status_5xx
from uplink import (
    Consumer,
    get as http_get,
    returns,
    headers,
    retry,
    Query,
    delete,
    post,
    patch,
    Body,
    json,
)

# Module configuration
USE_SERVICES_API = True
key = get_key(use_services_api=USE_SERVICES_API)

@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=20, when=status_5xx())
class Sharepoint(Consumer):
    """Inteface to Sharepoint resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._services_base_url if USE_SERVICES_API else Resource._base_url
        super().__init__(base_url=self._base_url, *args, **kw)

    def mappings(self):
        return self.__Mappings(self)

    def tree(self):
        return self.__Tree(self)

    @returns.json
    @http_get("sharepoint/sites")
    def list_sites(self):
        """This call will return list of sites."""

    @returns.json
    @http_get("sharepoint/files")
    def list_files(self, site_name: Query = None, drive_name: Query = None, item_id: Query = None):
        """This call will return list of files for the specified site, drive, and item."""
    

    @headers({"Ocp-Apim-Subscription-Key": key})
    @retry(max_attempts=20, when=status_5xx())
    class __Mappings(Consumer):
        """Interface to Sharepoint Mappings resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=self._base_url, *args, **kw)

        @returns.json
        @http_get("sharepoint/mappings")
        def list(
            self,
            machine_uid: Query = None,
            machine_catalog_uid: Query = None,
            ):
            """This call will return list of mappings."""

        @returns.json
        @http_get("sharepoint/mappings/{uid}")
        def get(self, uid: str):
            """This call will return a mapping for the specified uid."""

        @delete("sharepoint/mappings/{uid}")
        def delete(self, uid: str):
            """This call will delete a mapping for the specified uid."""

        @returns.json
        @json
        @post("sharepoint/mappings")
        def insert(self, mapping: Body):
            """This call will create a mapping with the specified parameters."""

        @json
        @patch("sharepoint/mappings/{uid}")
        def update(self, uid: str, mapping: Body):
            """This call will update a mapping with the specified parameters."""
    
    @headers({"Ocp-Apim-Subscription-Key": key})
    @retry(max_attempts=20, when=status_5xx())
    class __Tree(Consumer):
        """Interface to Sharepoint Tree resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=self._base_url, *args, **kw)

        @returns.json
        @http_get("sharepoint-tree/item-tree/{site_name}/{drive_name}")
        def get_tree(self, site_name: str, drive_name: str, include_files: Query = None):
            """Get cached item tree for the specified site and drive."""

        
        @returns.json
        @http_get("sharepoint-tree/item-tree/{site_name}/{drive_name}/children/{parent_id}")
        def get_item_children(self, site_name: str, drive_name: str, parent_id: str, include_files: Query = None):
            """Get cached item children for the specified site, drive, and parent id."""
        
        @returns.json
        @post("sharepoint-tree/item-tree/refresh")
        def refresh_tree(self, body: Body):
            """Refresh cached item tree for the specified site and drive."""

        @returns.json
        @http_get("sharepoint-tree/item-tree/status")
        def get_tree_status(self):
            """Get cached item tree status."""

        
        @returns.json
        @http_get("sharepoint-tree/item-tree/{site_name}/{drive_name}/metadata")
        def get_tree_metadata(self, site_name: str, drive_name: str):
            """Get cached item tree metadata for the specified site and drive."""
            
        @http_get("sharepoint-tree/health")
        def get_health(self):
            """Get health of the sharepoint tree."""

        @delete("sharepoint-tree/item-tree/{site_name}/{drive_name}")
        def clear_cached_tree(self, site_name: str, drive_name: str):
            """Clear cached item tree for the specified site and drive."""