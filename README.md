# python-kroger-client

A simple wrapper around the kroger api.

## Table of Contents

* [python-kroger-client](#python-kroger-client)
  * [Features](#features)
  * [Usage](#usage)
    * [Set environment variables](#set-environment-variables)
    * [Import the config module](#import-the-config-module)
    * [Initialize the client](#initialize-the-client)
    * [Methods](#methods)
  * [Example](#example)
  * [TODOS](#todos)

## Features

Provides utilities to:
    - Search for products
    - Search for locations
    - Add a product to a users card (requires customer authorization)

## Usage

### Set environment variables

You must create a developer account (https://developer.kroger.com/) and register an application.

To use the `ServiceKrogerClient`, 2 environment variables from your application configuration are required:

1. KROGER_CLIENT_ID
1. KROGER_CLIENT_SECRET

In addition, to use the `CustomerKrogerClient`, you must set 3 additional environment variables:
> WARNING: This should only be used for testing.  You should never request a user's username/password.  In the future, this feature will be removed.

1. KROGER_REDIRECT_URI
1. KROGER_USERNAME
1. KROGER_PASSWORD

### Import the config module

The config module contains all the variables needed to intialize the client.  In addition to the environment variables defined above, it includes a helper variable `encoded_client_token`, a base64 encoded combination of `client_id` and `client_secret` used in client authentication.

### Initialize the client

> Note: Clients use TTL caching (as stored `access_token.cache` pickle file) to prevent unnecessary calls to authenticate.

```python
# Service Client
import config
client = KrogerServiceClient(config.encoded_client_token)
```

```python
# Customer Client
import config
client = KrogerServiceClient(config.encoded_client_token, config.redirect_uri, config.customer_username, config.customer_password)
```

### Methods

`KrogerServiceClient` has two methods:

* `search_products(term=None, location_id=None, product_id=None, brand=None, fulfillment='csp', limit=5)` - returns a list of [Products](./models/product.py)
* `get_locations(zipcode, within_miles=10, limit=5, chain='Kroger')` - returns a list of [Locations](./models/location.py)

`KrogerCustomerClient` contains the same methods as `KrogerServiceClient` and one additional method:

### Models

[Products](./models/product.py) - Full api response not implemented.  See full response returned by api [here](./docs/api_responses/products.json)

[Locations](./models/location.py) - Full api response not implemented.  See full response returned by api [here](./docs/api_responses/locations.json)

* `add_items_to_cart(items)`

## Example

```python
import config

client = KrogerServiceClient(config.encoded_client_token, config.redirect_uri, config.customer_username, config.customer_password)

products = customer_client.search_products(term="milk", limit=1, location_id='02600845')

items = [{'upc': products[0].upc, 'quantity':3}]
customer_client.add_items_to_cart(items)
```

There is a full example in [example.py](./example.py)

## TODOS

* Remove crawler that authorizes customer client and replace it with and api around the standard authorization path (using the redirect_uri)
* Add functionality to refresh customer client token
* Add customer client function to get coupons
* Figure out a less clunky version of cacheing
