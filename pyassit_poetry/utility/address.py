from utility.city import City
from utility.country import Country
from utility.street import Street
from utility.zip_code import ZipCode


class Address:
    """class for address object"""

    def __init__(
        self, street: Street, city: City, zip_code: ZipCode, country: Country
    ) -> None:
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country

    def __repr__(self) -> str:
        return "Address:{f'\nstreet: {self.street} ' if self.street else ''}{f'city: {self.city} ' if self.city else ''}{f'\nzip code: {self.zip_code} ' if self.zip_code else ''}{f'\ncountry: {self.country} ' if self.country else ''}"
