from python_kroger_client.client import (
    KrogerCustomerClient,
    KrogerServiceClient,
)

from python_kroger_client.config import (
    customer_username,
    customer_password,
    encoded_client_token,
    redirect_uri,
)

def add_to_items(items, product, quantity):
    """ Adds specified item to list of items with given quantity and returns items

    Arguments:
        items {array} -- An array of items to purchase
        product {Product} -- The product we want to buy
        quantity {int} -- How much of the product we want to buy
    """
    item_to_add = {
        "upc": product.upc,
        "quantity": quantity
    }
    items.append(item_to_add)
    return items


print("==================================================")
print("============== SERVICE CLIENT ====================")
print("==================================================")
service_client = KrogerServiceClient(encoded_client_token=encoded_client_token)
products = service_client.search_products(term="Taco", limit=10, location_id='02600845')
print()
print("PRODUCTS")
print("==================================================")
print()
for p in products: print(p)
print()
locations = service_client.get_locations(37206, within_miles=10, limit=10)
print("LOCATIONS")
print("==================================================")
print()
for l in locations: print(l)
print()


print("============== CUSTOMER CLIENT ====================")
customer_client = KrogerCustomerClient(encoded_client_token=encoded_client_token, redirect_uri=redirect_uri, customer_username=customer_username, customer_password=customer_password)
products = customer_client.search_products(term="Burger", limit=1, location_id='02600845')
product = products[0]
items = add_to_items([], product, 2)
customer_client.add_items_to_cart(items)