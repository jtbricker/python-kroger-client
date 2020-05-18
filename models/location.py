class Location:
    """ Represents a single kroger location """

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __str__(self):
        description = f"{self.name} ({self.id})"
        description += f" - {self.address}"
        return description

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, obj):
        id = obj.get("locationId")
        name = obj.get("name")
        address = _get_address(obj.get("address"))
        
        return Location(id, name, address)


def _get_address(address):
    line1 = address.get("addressLine1")
    city = address.get("city")
    state = address.get("state")
    zipcode = address.get("zipCode")

    return f"{line1}, {city}, {state}, {zipcode}"

