from clients.clients import BaseClient
from clients.utils import decorate_all_methods, base_api_retry


@decorate_all_methods(base_api_retry())
class ExampleRestClient(BaseClient):
    service_name = 'example_service'
    
    def get_building(self, building_id: str):
        """ Get information about a building """
        return self.method_request('GET', f'/buildings/{building_id}')

    def get_buildings(self, page: int = 1, page_size: int = 500, **params):
        """ List existing buildings using a paginator """
        params = {'page': page, 'page_size': page_size, **params}
        return self.method_request('GET', '/buildings/all', params=params)

    def get_all_buildings(self, **params):
        """ Get all existing buildings as a generator """
        return self.iterate_through_pagination(self.get_buildings, **params)