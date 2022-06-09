from clients.utils import get_from_json
from examples.example_client import ExampleRestClient


client = ExampleRestClient()

# Just ordinary requests
building = client.get_building(building_id='123').json()
first_page = client.get_buildings().json()

# Iterate through all items using all pages
for item in client.get_all_buildings(item_type='new'):  # `item_type` goes as a GET param
    street = get_from_json(item, 'base_info.address.street')  # extract element from json