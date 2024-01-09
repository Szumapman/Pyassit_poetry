from utility.field import Field


class Street(Field):
    """class for street object

    Args:
        Field (class): parent class
    """

    def __init__(self, value=None) -> None:
        self.value = value
