from abc import ABC, abstractmethod


class Field(ABC):
    """
    abstract class defining the basic properties of a field
    """

    @abstractmethod
    def __init__(self, value=None) -> None:
        self.value = value

    # overridden method __repr__
    def __repr__(self) -> str:
        return f"{self.value}"
