from validator_collection import validators  # pip install validator-collection
from utility.field import Field


class Email(Field):
    """
    class for email object

    class raise a ValueError if email is invalid

    Args:
        Field (class): parent class
    """

    def __init__(self, value: str) -> None:
        self.value = validators.email(value, allow_empty=True)
