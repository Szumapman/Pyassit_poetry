from utility.field import Field


class Content(Field):
    """
    class for content object

    Args:
        Field (class): parent class
    """

    def __init__(self, value: str) -> None:
        self.value = value
