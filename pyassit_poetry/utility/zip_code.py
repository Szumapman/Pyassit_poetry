from utility.field import Field


class ZipCode(Field):
    """class for zip_code object

    Args:
        Field (class): parent class
    """

    def __init__(self, value=None) -> None:
        self.value = value
