from utility.field import Field


class Title(Field):
    """
    class for title object

    Args:
        Field (class): parent class
    """

    def __init__(self, value: str) -> None:
        self.value = value
