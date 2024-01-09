import difflib
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from pathlib import Path

from utility.abstract_notes_interaction import AbstractNotesInteraction
from utility.notes import Notes
from utility.note import Note
from utility.title import Title
from utility.content import Content
from utility.exit_interrupt import ExitInterrupt
from utility.invalid_csv_file_structure import InvalidCSVFileStructure


class CliNotesInteraction(AbstractNotesInteraction):
    # function to handle with errors
    def _error_handler(func):
        def wrapper(*args):
            while True:
                try:
                    return func(*args)
                except FileNotFoundError:
                    return "Error: Unable to handle with the specified file. Please try again."
                except InvalidCSVFileStructure:
                    return "Error: unable to import, invalid file structure."
                except Exception as e:
                    return f"Error: {e}. Please try again."

        return wrapper

    def __init__(self, notes: Notes) -> None:
        self.notes = notes

    def show_notes(self, arg):
        return self._display_notes(self.notes, "Your notes:")

    def _display_notes(self, notes: Notes, arg: str) -> str:
        if notes:
            notes_to_show = arg
            i = 1
            for note in notes.values():
                notes_to_show += f'\nNote {i}:\n{note}\n{"═"*30}'
                i += 1
            return notes_to_show
        return "Nothing to show."

    def _set_title_str(self, arg: str) -> str:
        title_completer = FuzzyWordCompleter(self.notes.keys())
        if arg:
            return arg.strip().lower()
        return (
            prompt(
                "Type note title or <<< if you want to cancel: ",
                completer=title_completer,
            )
            .strip()
            .lower()
        )

    def _add_title(self, arg):
        title = self._set_title_str(arg)
        while True:
            if title not in self.notes.keys() or title == "<<<" or title == "":
                return title
            print(f"Note with title {title} already exists. Choose another title.")
            title = self._set_title_str("")

    def create_note(self, arg):
        title = self._add_title(arg)
        if title == "" or title == "<<<":
            return "Operation canceled."
        content = input("Enter note content: ")
        tags = set(input("Tags (separated by space): ").strip().split())
        self.notes.add_note(Note(Title(title), Content(content), tags))
        return f'Note with title: "{title}", created successfully.'

    def _edit_title(self, note: Note):
        title = self._add_title("")
        if title == "" or title == "<<<":
            return "Operation canceled."
        old_note_title = note.title.value
        note.title = Title(title)
        self.notes[note.title.value] = note
        self.notes.pop(old_note_title)
        return f'Note title chcanged from" "{old_note_title} to "{note.title}'

    def _edit_content(self, note: Note):
        note.content = input("Type new content: ")
        return f"Note content changed"

    def _add_tag(self, note: Note):
        new_tags = set(input("Type new tags (separated by space): ").strip().split())
        for tag in new_tags:
            note.add_tag(tag)
        return f"Tags: {', '.join(new_tags)} added to the note."

    def _del_tag(self, note: Note):
        tag_completer = FuzzyWordCompleter(note.tags)
        tags_to_delete = set(
            prompt(
                "Type tags you want to delete (separated by space): ",
                completer=tag_completer,
            )
            .strip()
            .split()
        )
        for tag in tags_to_delete:
            note.delete_tag(tag)
        return f"Tags: {', '.join(tags_to_delete)} deleted from the note."

    NOTE_EDIT_COMMANDS = {
        "title": _edit_title,
        "content": _edit_content,
        "addtag": _add_tag,
        "deltag": _del_tag,
    }

    def edit_note(self, arg):
        title = self._set_title_str(arg)
        if title == "" or title == "<<<":
            return "Operation canceled."
        if title in self.notes.keys():
            note = self.notes[title]
            command_completer = FuzzyWordCompleter(self.NOTE_EDIT_COMMANDS)
            command = prompt(
                f"Type what you want to change in note (title, content, add tag, delete tag): ",
                completer=command_completer,
            )
            return self._execute_command(self.NOTE_EDIT_COMMANDS, command, note)
        return f"Note with title {title} dosen't exist, operation canceled."

    def delete_note(self, arg):
        title = self._set_title_str(arg)
        if title == "" or title == "<<<":
            return "Operation canceled."
        if title in self.notes.keys():
            self.notes.pop(title)
            return f"Note with title: {title} deleted"
        return f"Note with title {title} dosen't exist, operation canceled."

    def sort_notes_by_tag(self, tag: str):
        if tag:
            tags_to_show = set(tag.strip())
        else:
            tags_to_show = set()
            for note in self.notes.values():
                tags_to_show = tags_to_show | note.tags

        notes_sorted_by_tags = "Notes sorted by tag: "
        for tag in tags_to_show:
            notes_with_tag = Notes()
            for note in self.notes.values():
                if tag in note.tags:
                    notes_with_tag.add_note(note)
            notes_sorted_by_tags += self._display_notes(
                notes_with_tag, f"\n{'-'*4} {tag} {'-'*4}"
            )
        return notes_sorted_by_tags

    def search_notes(self, query: str):
        if query:
            query = query.strip().lower()
        else:
            query = input("Type a query to search for in note: ")
        return self._display_notes(
            self.notes.search(query), f'Notes containing: "{query}":'
        )

    @_error_handler
    def _import_export_prepare(self, file_name):
        if not file_name:
            file_name = input(
                "Type the filename (e.g., output.csv) or <<< to cancel: "
            ).strip()
        if file_name == "<<<" or file_name == "":
            return None
        program_dir = Path(__file__).parent.parent
        return program_dir.joinpath("data/" + file_name)

    @_error_handler
    def export_to_csv(self, file_name: str):
        full_path = self._import_export_prepare(file_name)
        if full_path:
            self.notes.export_to_csv(full_path)
            return f"Data exported successfully to {full_path}."
        return "Export cancelled."

    @_error_handler
    def import_from_csv(self, file_name: str):
        full_path = self._import_export_prepare(file_name)
        if full_path:
            self.notes.import_from_csv(full_path)
            return f"Data imported successfully from {full_path}."
        return "Import cancelled."

    @_error_handler
    def save_notes(self, filename):
        self.notes.save_notes(filename)
        return "Notes saved."

    @_error_handler
    def load_notes(self, filename):
        self.notes = self.notes.load_notes(filename)
        return f"Notes loaded from file {filename}"

    def exit_program(self, argument):
        raise ExitInterrupt

    def help(self, arg):
        width = 75
        help = f'╔{"═"*width}╗\n'
        help += "║ {:>22} - {:<48} ║\n".format(
            "command", "description <optional argument>"
        )
        help += f'╠{"═"*width}╣\n'
        for command, description in self.COMMANDS_HELP.items():
            help += "║ {:>22} - {:<48} ║\n".format(command, description)
        help += f'╚{"═"*width}╝'
        return help

    # dict for addressbook menu
    NOTES_MENU_COMMANDS = {
        "add": create_note,
        "edit": edit_note,
        "show": show_notes,
        "delete": delete_note,
        "sort": sort_notes_by_tag,
        "export": export_to_csv,
        "import": import_from_csv,
        "search": search_notes,
        "save": save_notes,
        "up": "up",
        "exit": exit_program,
        "help": help,
    }

    COMMANDS_HELP = {
        "add <title>": "add new note <title>",
        "edit <title>": "edit note <title>",
        "show": "show all notes",
        "show <title>": "show specific note",
        "delete <title>": "delete note <title>",
        "sort <tag>": "sort notes by tags or show notes with <tag>",
        "export <file name>": "export notes to csv file <file name>",
        "import <file name>": "import notes from csv file <file name>",
        "search <query>": "search in notes <query>",
        "save": "save notes",
        "up": "back tu main menu",
        "exit": "exit from the program",
        "help": "show this menu",
    }

    def _execute_command(self, commands_dict: dict, cmd: str, argument):
        """Function to execute user commands

        Args:
            cmd (str): user command
            argument: argument to process
        """
        if cmd not in commands_dict:
            matches = difflib.get_close_matches(cmd, commands_dict)
            info = f'\nmaybe you meant: {" or ".join(matches)}' if matches else ""
            return f"Command {cmd} is not recognized" + info
        cmd = commands_dict[cmd]
        return cmd(self, argument)

    # function that parses user input commands
    def _parse_command(self, user_input: str) -> (str, str):
        """
        Parse user input command

        Args:
            user_input (str): user input command

        Returns:
            str: command
            str: argument
        """
        tokens = user_input.split()
        command = tokens[0].lower()
        argument = "".join(tokens[1:])
        return command, argument

    # receiving a command from a user
    def _user_command_input(self):
        commands_completer = FuzzyWordCompleter(self.NOTES_MENU_COMMANDS.keys())
        user_input = prompt(
            f"PyAssist  notes >>> ", completer=commands_completer
        ).strip()
        if user_input:
            return self._parse_command(user_input)
        return "", ""

    def cli_notes_menu(self):
        while True:
            cmd, argument = self._user_command_input()
            if cmd == "up":
                return "back to main menu"
            print(self._execute_command(self.NOTES_MENU_COMMANDS, cmd, argument))
