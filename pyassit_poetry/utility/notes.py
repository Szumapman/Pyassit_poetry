import pickle
import csv
from pathlib import Path
from collections import UserDict

from utility.note import Note
from utility.title import Title
from utility.content import Content
from utility.invalid_csv_file_structure import InvalidCSVFileStructure


class Notes(UserDict):
    """
    The Notes class extends the UserDict class.
    The class checks whether the elements added to the dictionary are valid (keys and values based on the Note class).

    Args:
        UserDict (class): parent class
    """

    # function used as a decorator to catch errors when item is adding to notes
    def _value_error(func):
        def inner(self, note):
            if not isinstance(note, Note):
                raise ValueError
            return func(self, note)

        return inner

    # Add note to notes
    @_value_error
    def add_note(self, note: Note):
        self.data[note.title.value.lower()] = note

    # search in notes, return notes object that containing records with the query
    def search(self, query: str):
        """
        The method first looks for an exact match in the keys
        then searches the values of the individual notes and adds them to the returned Notes object
        if the fragment matches the query.

        Returns:
            Notes: a new object of class Notes with notes based on the query
        """
        query_notes = Notes()
        query = query.strip().lower()
        if query in self.keys():
            query_notes[query] = self[query]
        for note in self.values():
            if query in note.title.value.lower() or query in note.content.value.lower():
                query_notes[note.title.value] = note
            if note.tags:
                for tag in note.tags:
                    if query in tag:
                        query_notes[note.title.value] = note
        return query_notes

    def export_to_csv(self, file_path: Path):
        if len(self.data) > 0:
            with open(file_path, "w", newline="") as fh:
                field_names = ["title", "content", "tags"]
                writer = csv.DictWriter(fh, fieldnames=field_names)
                writer.writeheader()
                for note in self.data.values():
                    note_dict = {"title": note.title.value}
                    note_dict["content"] = note.content.value
                    note_dict["tags"] = "|".join(note.tags)
                    writer.writerow(note_dict)

    def import_from_csv(self, file_path: Path):
        with open(file_path, "r", newline="") as fh:
            reader = csv.DictReader(fh)
            if ["title", "content", "tags"] != reader.fieldnames:
                raise InvalidCSVFileStructure
            for row in reader:
                title = row["title"]
                content = row["content"]
                tags = set(row["tags"].split("|"))
                if title not in self.keys():
                    self.add_note(Note(Title(title), Content(content), tags))

    # method to save notes to file
    def save_notes(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

    # method to read notes from file
    def load_notes(self, filename):
        if Path.exists(Path(filename)):
            with open(filename, "rb") as fh:
                return pickle.load(fh)
        return self
