from abc import abstractmethod, ABC


class AbstractAddressbookInteraction(ABC):
    @abstractmethod
    def add_name(self):
        pass

    @abstractmethod
    def add_phone(self):
        pass

    @abstractmethod
    def add_email(self):
        pass

    @abstractmethod
    def add_birthday(self):
        pass

    @abstractmethod
    def add_address(self):
        pass

    @abstractmethod
    def add_record(self):
        pass

    @abstractmethod
    def del_record(self):
        pass

    @abstractmethod
    def show(self, *args):
        pass

    @abstractmethod
    def show_upcoming_birthday(self):
        pass

    @abstractmethod
    def edit_name(self):
        pass

    @abstractmethod
    def edit_birthday(self):
        pass

    @abstractmethod
    def edit_address(self):
        pass

    @abstractmethod
    def edit_phone(self):
        pass

    @abstractmethod
    def edit_email(self):
        pass

    @abstractmethod
    def edit_record(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def export_to_csv(self):
        pass

    @abstractmethod
    def import_from_csv(self):
        pass

    @abstractmethod
    def save_addressbook(self):
        pass

    @abstractmethod
    def load_addressbook(self):
        pass
