from .module_imports import get_key
from uplink.retry.when import status_5xx
from uplink import (
    Consumer,
    get as http_get,
    post,
    returns,
    headers,
    retry,
    Body,
    json,
)

# Module configuration
USE_SERVICES_API = True
key = get_key(use_services_api=USE_SERVICES_API)


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=20, when=status_5xx())
class _Portal_Configurations(Consumer):
    """Inteface to portal configurations resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._services_base_url if USE_SERVICES_API else Resource._base_url
        super().__init__(base_url=self._base_url, *args, **kw)

    @returns.json
    @http_get("portal/configurations/file-resources")
    def get_file_resources(
        self,
    ):
        """This call will return portal configurations for file resources."""

    @returns.json
    @http_get("portal/configurations/parts-lookup-data-files")
    def get_parts_lookup_data_files(
        self,
    ):
        """This call will return portal configurations for parts lookup data files."""

    @returns.json
    @http_get("portal/configurations/parts-lookup-fixed-width-settings")
    def get_parts_lookup_fixed_width_settings(
        self,
    ):
        """This call will return portal configurations for parts lookup fixed width settings."""

    @returns.json
    @http_get("portal/configurations/file-type-storage-mapping")
    def list_file_type_storage_mappings(
        self,
    ):
        """This call will return portal configurations for file type storage mappings."""

    @returns.json
    @http_get("portal/configurations/file-type-storage-mapping/{file_type}")
    def get_file_type_storage_mapping(
        self,
        file_type: str,
    ):
        """This call will return the file type storage mapping for the specified file type."""

    @returns.json
    @http_get("portal/configurations/portal-search-config")
    def get_portal_search_config(
        self,
    ):
        """This call will return portal configurations for portal search config."""

    @returns.json
    @json
    @post("portal/configurations/portal-search-config-for-user")
    def get_portal_search_config_for_user(
        self,
        params: Body
    ):
        """This call will return portal configurations for portal search config for user."""

    @returns.json
    @json
    @post("portal/configurations/portal-search-options-for-user")
    def get_portal_search_options_for_user(
        self,
        params: Body
    ):
        """This call will return portal configurations for portal search options for user."""
