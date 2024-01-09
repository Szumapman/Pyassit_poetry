import difflib
import pyfiglet
import cowsay
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from pathlib import Path

from utility.addressbook import AddressBook
from utility.notes import Notes
from utility.cli_addressbook_interaction import CliAddressBookInteraction
from utility.sorter import FileSorter
from utility.cli_notes_interaction import CliNotesInteraction
from utility.exit_interrupt import ExitInterrupt
from abstract_pyassist import AbstractPyassist


class CliPyassist(AbstractPyassist):
    # function to handle with errors
    def _error_handler(func):
        def wrapper(self, *args):
            while True:
                try:
                    return func(self, *args)
                except (ExitInterrupt, KeyboardInterrupt):
                    self.cli_pyassist_exit("")
                except Exception as e:
                    return f"Error: {e}. Please try again."

        return wrapper

    def __init__(
        self,
        cli_addressbook_interaction: CliAddressBookInteraction,
        cli_notes_interaction: CliNotesInteraction,
    ) -> None:
        self.cli_addressbook_interaction = cli_addressbook_interaction
        self.cli_notes_interaction = cli_notes_interaction

    def addressbook_interaction(self, *args):
        return self.cli_addressbook_interaction.cli_addressbook_menu()

    def notes_interaction(self, *args):
        return self.cli_notes_interaction.cli_notes_menu()

    def sort_init(self, folder_path=None):
        if not folder_path:
            folder_path = input(
                "Type the path to the folder whose contents you want to sort: "
            ).strip()
        sorter = FileSorter()
        return sorter.sort(folder_path)

    # exit / close program
    def cli_pyassist_exit(self, argument):
        # for the time being, the path to the addressbook and notes files are hardcoded
        program_dir = Path(__file__).parent
        addressbook_filename = program_dir.joinpath("data/addressbook.dat")
        notes_filename = program_dir.joinpath("data/notes.dat")
        self.cli_addressbook_interaction.save_addressbook(addressbook_filename)
        self.cli_notes_interaction.save_notes(notes_filename)
        cowsay.cow("Your data has been saved.\nGood bye!")
        sys.exit()

    # show help
    def help(self, argument):
        width = 60
        help_table = f'╔{"═" * width}╗\n'
        help_table += "║ {:>12} - {:<43} ║\n".format("command", "description")
        help_table += f'╠{"═" * width}╣\n'
        for command, description in self.COMMANDS_HELP.items():
            help_table += "║ {:>12} - {:<43} ║\n".format(command, description)
        help_table += f'╚{"═" * width}╝'
        return help_table

    COMMANDS = {
        "addressbook": addressbook_interaction,
        "notes": notes_interaction,
        "sort": sort_init,
        "exit": cli_pyassist_exit,
        "help": help,
    }

    COMMANDS_HELP = {
        "addressbook": "open addressbook",
        "notes": "open notes",
        "sort <folder path>": "sort files <in given folder>",
        "exit": "exit from the program",
        "help": "show this menu",
    }

    # a function that parses user input commands
    @staticmethod
    def _parse_command(user_input: str) -> (str, str):
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
        return command, tuple(argument)

    # receiving a command from a user
    def _user_command_input(self):
        commands_completer = FuzzyWordCompleter(self.COMMANDS.keys())
        user_input = prompt(f"main menu >>> ", completer=commands_completer).strip()
        if user_input:
            return self._parse_command(user_input)
        return "", ""

    def _execute_commands(self, cmd: str, argument: str):
        """Function to execute user commands

        Args:
            cmd (str): user command
            argument (str): argument from user input

        Returns:
            func: function with data_ti_use and arguments
        """
        if cmd not in self.COMMANDS:
            matches = difflib.get_close_matches(cmd, self.COMMANDS)
            info = f"\nmaybe you meant: {' or '.join(matches)}" if matches else ""
            return f"Command {cmd} is not recognized" + info
        cmd = self.COMMANDS[cmd]
        return cmd(self, argument)

    @_error_handler
    def main_menu(self):
        while True:
            cmd, argument = self._user_command_input()
            print(self._execute_commands(cmd, argument))


def main():
    print(pyfiglet.figlet_format("PyAssist", font="slant"))
    cli_pyassist = CliPyassist(
        CliAddressBookInteraction(AddressBook()), CliNotesInteraction(Notes())
    )
    # for the time being, the path to the addressbook and notes files are hardcoded
    program_dir = Path(__file__).parent
    addressbook_filename = program_dir.joinpath("data/addressbook.dat")
    notes_filename = program_dir.joinpath("data/notes.dat")
    cli_pyassist.cli_addressbook_interaction.load_addressbook(addressbook_filename)
    cli_pyassist.cli_notes_interaction.load_notes(notes_filename)
    cli_pyassist.main_menu()


if __name__ == "__main__":
    main()
