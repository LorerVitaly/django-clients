import logging
import requests
from clients.models import ServiceCredentials

logger = logging.getLogger(__name__)


class BaseClient:
    service_name = None
    auth_header = 'Authorization'

    def __init__(self):
        if not self.service_name:
            raise NotImplementedError('`service_name` should be defined')
        credentials = ServiceCredentials.objects.get(service=self.service_name)
        self.base_endpoint = credentials.host
        self.token = credentials.token

    def method_request(self, http_method: str, url: str, headers: dict=None, **kwargs) -> requests.Response:
        headers = headers or {
            'Content-Type': 'application/json',
            self.auth_header: self.token
        }
        response = requests.request(
            http_method,
            url,
            headers=headers,
            **kwargs
        )

        return response

    def iterate_through_pagination(self, client_method, results_field='results', next_page_field='next', **kwargs):
        response = client_method(**kwargs).json()
        entries = response.get(results_field, [])
        for entry in entries:
            yield entry

        if response.get(next_page_field):
            kwargs['page'] += 1
            yield from self.iterate_through_pagination(client_method, results_field, next_page_field, **kwargs)