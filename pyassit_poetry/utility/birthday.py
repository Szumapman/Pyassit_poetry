from datetime import datetime
from utility.field import Field


class FutureDateError(Exception):
    """
    Helper class to raise specyfic exception if you try to assign a future date as a birthday.

    Args:
        Exception (class): parent class
    """

    pass


class Birthday(Field):
    """
    Class for birthday object.

    The class raises ValueError if the string passed has an invalid format (from datetime)
    and FutureDateError if you try to assign a future date as a birthday.

    Args:
        Field (class): parent class
    """

    def __init__(self, value=None) -> None:
        self.value = self._set_birthdate(value)

    # helper method to check and set birthday value
    def _set_birthdate(self, value):
        if value is None:
            return None
        birthday = datetime.strptime(
            value.strip()
            .replace(".", " ")
            .replace("/", " ")
            .replace("-", " ")
            .replace(".", " "),
            "%d %m %Y",
        ).date()
        if birthday is not None and birthday > datetime.now().date():
            raise FutureDateError
        return birthday

    # overridden method __repr__
    def __repr__(self) -> str:
        return self.value.strftime("%A %d-%m-%Y")
