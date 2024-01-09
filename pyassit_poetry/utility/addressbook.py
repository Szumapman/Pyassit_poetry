from collections import UserDict

import pickle
import csv
from pathlib import Path

from utility.record import Record
from utility.name import Name
from utility.phone import Phone
from utility.email import Email
from utility.birthday import Birthday
from utility.address import Address
from utility.street import Street
from utility.city import City
from utility.zip_code import ZipCode
from utility.country import Country
from utility.invalid_csv_file_structure import InvalidCSVFileStructure


class AddressBook(UserDict):
    """
    The AddresBook class extends the UserDict class.
    The class checks whether the elements added to the dictionary are valid (keys and values based on the Record class).

    Args:
        UserDict (class): parent class
    """

    # function used as a decorator to catch errors when item is adding to addresbook
    def _value_error(func):
        def inner(self, record):
            if not isinstance(record, Record):
                raise ValueError
            return func(self, record)

        return inner

    # Add record to addresbook
    @_value_error
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # search in addressbook, return addressbook object that containing records with the query
    def search(self, query: str):
        """
        The method first looks for an exact match in the keys
        then searches the values of the individual records and adds them to the returned Addresbook object if the fragment matches the query.

        Returns:
            Addresbook: a new object of class Addresbook with records based on the query
        """
        query_addresbook = AddressBook()
        query = query.strip()
        key_query = query.title()
        if key_query in self.keys():
            query_addresbook[key_query] = self[key_query]
        query = query.lower()
        for record in self.values():
            if query in record.name.value.lower() or key_query in record.name.value:
                query_addresbook[record.name.value] = record
            for phone in record.phones:
                if query in phone.value:
                    query_addresbook[record.name.value] = record
            for email in record.emails:
                if query in email.value:
                    query_addresbook[record.name.value] = record
            if record.birthday is not None:
                if query in str(record.birthday.value):
                    query_addresbook[record.name.value] = record
            if record.address and (
                query in record.address.street.lower()
                or query in record.address.city.lower()
                or query in record.address.zip_code.lower()
                or query in record.address.country.lower()
            ):
                query_addresbook[record.name.value] = record
        return query_addresbook

    # method to save addresbook to file
    def save_addresbook(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

    # method to read addresbook from file
    def load_addresbook(self, filename):
        if Path.exists(Path(filename)):
            with open(filename, "rb") as fh:
                return pickle.load(fh)
        return self

    # export records form addresbook to csv file
    """
    The method exports the data to a csv file. Phones and emails are separated by the '|' char.
    """

    def export_to_csv(self, filename):
        if len(self.data) > 0:
            with open(filename, "w", newline="") as fh:
                field_names = [
                    "name",
                    "phones",
                    "emails",
                    "birthday",
                    "street",
                    "city",
                    "zip_code",
                    "country",
                ]
                writer = csv.DictWriter(fh, fieldnames=field_names)
                writer.writeheader()
                for record in self.data.values():
                    record_dict = {"name": record.name.value}
                    phones = []
                    for phone in record.phones:
                        phones.append(phone.value)
                    record_dict["phones"] = "|".join(phones)
                    emails = []
                    for email in record.emails:
                        emails.append(email.value)
                    record_dict["emails"] = "|".join(emails)
                    if record.birthday is not None:
                        record_dict["birthday"] = record.birthday.value.strftime(
                            "%d %m %Y"
                        )
                    if record.address:
                        record_dict["street"] = record.address.street.value
                        record_dict["city"] = record.address.city.value
                        record_dict["zip_code"] = record.address.zip_code.value
                        record_dict["country"] = record.address.country.value
                    writer.writerow(record_dict)

    # import from csv file
    """
    The method imports data into a csv file. 
    
    Data structures in the file:
    name,phones,emails,birthsday
    
    Phones and emails are separated (if there is more than one phone or email) with "|".
    Birthday should be written as: day month year e.g. 21 12 1999 or 30-01-2012 or 09/01/1987
    """

    def import_from_csv(self, filename):
        with open(filename, "r", newline="") as fh:
            reader = csv.DictReader(fh)
            if [
                "name",
                "phones",
                "emails",
                "birthday",
                "street",
                "city",
                "zip_code",
                "country",
            ] != reader.fieldnames:
                raise InvalidCSVFileStructure
            for row in reader:
                name = row["name"]
                phones = row["phones"].split("|")
                phones_to_add = []
                for phone in phones:
                    if phone != "":
                        phones_to_add.append(Phone(phone))
                emails = row["emails"].split("|")
                emails_to_add = []
                for email in emails:
                    if email != "":
                        emails_to_add.append(Email(email))
                birthday = row["birthday"]
                if birthday != "":
                    birthday = Birthday(birthday)
                else:
                    birthday = None
                street = row["street"]
                city = row["city"]
                zip_code = row["zip_code"]
                country = row["country"]
                if street or city or zip_code or country:
                    address = Address(
                        Street(street), City(city), ZipCode(zip_code), Country(country)
                    )
                else:
                    address = None
                self.add_record(
                    Record(Name(name), phones_to_add, emails_to_add, birthday, address)
                )
