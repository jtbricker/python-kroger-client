param_map = {
    'brand': 'filter.brand',
    'chain': 'filter.chain',
    'fulfillment': 'filter.fulfillment',
    'limit': 'filter.limit',
    'location_id': 'filter.locationId',
    'product_id': 'filter.product_id',
    'term': 'filter.term',
    'within_miles': 'filter.radiusInMiles',
    'zipcode': 'filter.zipCode.near',
}

def get_mapped_params(params):
    """ Maps a dictionary of parameters (ignore self) to the api's expected key value """
    return { param_map[key] : value for key, value in params.items() if key != 'self'}