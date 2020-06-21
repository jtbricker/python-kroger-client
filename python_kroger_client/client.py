import json

import requests

from auth_service import (
    get_client_access_token,
    get_customer_access_token,
)
from api_params import get_mapped_params
from models.product import Product
from models.location import Location

API_URL = 'https://api.kroger.com/v1'

class KrogerClient:
    def _make_get_request(self, endpoint, params=None):
        url = API_URL + endpoint
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)

    def search_products(self, term=None, location_id=None, product_id=None, brand=None, fulfillment='csp', limit=5):
        params = get_mapped_params(locals())
        endpoint = '/products'
        
        results = self._make_get_request(endpoint, params=params)
        data = results.get('data')
        return [Product.from_json(product) for product in data]


    def get_locations(self, zipcode, within_miles=10, limit=5, chain='Kroger'):
        params = get_mapped_params(locals())
        endpoint = '/locations'

        results = self._make_get_request(endpoint, params=params)
        data = results.get('data')
        return [Location.from_json(location) for location in data]


class KrogerServiceClient(KrogerClient):
    """ A kroger api client authenticated with the service credentials
        Has limited functionality:
            - Search for products
            - Search for store details
    """
    def __init__(self, encoded_client_token):
        self.token = get_client_access_token(encoded_client_token)


class KrogerCustomerClient(KrogerClient):
    """ A kroger api client authenticated with an authorized user 
        Can:
            - Search for products
            - Search for store details
            - Add items to authorized user's cart
    """

    def __init__(self, encoded_client_token, redirect_uri, customer_username, customer_password):
        self.token = get_customer_access_token(encoded_client_token, redirect_uri, customer_username, customer_password)  

    def add_items_to_cart(self, items):
        """ Adds specified items to users shopping cart

        Arguments:
            items {array[dict]} -- Array of item dictionaries with keys "upc" and "quantity"
        """
        url = API_URL + '/cart/add'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        data = {'items': items}

        response = requests.put(url, headers=headers, data=json.dumps(data))
        if 200 <= response.status_code < 300:
            print("Successfully added items to cart")
        else:
            print("Something went wrong, items may not have been added to card (status code: %s)" %response.status_code)
