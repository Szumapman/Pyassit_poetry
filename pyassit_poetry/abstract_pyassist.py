from abc import abstractmethod, ABC


class AbstractPyassist(ABC):
    @abstractmethod
    def addressbook_interaction(self):
        pass

    @abstractmethod
    def notes_interaction(self):
        pass

    @abstractmethod
    def sort_init(self):
        pass

    @abstractmethod
    def main_menu(self):
        pass
