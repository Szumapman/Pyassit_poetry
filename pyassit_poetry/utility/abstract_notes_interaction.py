from abc import abstractmethod, ABC


class AbstractNotesInteraction(ABC):
    @abstractmethod
    def show_notes(self):
        pass

    @abstractmethod
    def create_note(self):
        pass

    @abstractmethod
    def edit_note(self):
        pass

    @abstractmethod
    def delete_note(self):
        pass

    @abstractmethod
    def sort_notes_by_tag(self):
        pass

    @abstractmethod
    def search_notes(self):
        pass
