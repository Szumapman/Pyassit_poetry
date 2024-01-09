from utility.field import Field


class City(Field):
    """class for city object

    Args:
        Field (class): parent class
    """

    def __init__(self, value=None) -> None:
        self.value = value
