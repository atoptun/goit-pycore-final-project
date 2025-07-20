import types
from colorama import Fore, Back, Style, init
from src.personal_assistant.common import read_command
from src.personal_assistant.addr_book.controller import main as book_main
from src.personal_assistant.notes.controller import main as notes_main
from src.personal_assistant.views import draw_help


init(autoreset=True)


MAIN_MENU_COMMANDS_LIST = [
    types.SimpleNamespace(command="book", cmd="book", description="address book"),
    types.SimpleNamespace(command="notes", cmd="notes", description="notes"),
    types.SimpleNamespace(command="help, ?", cmd="help", description="this help"),
    types.SimpleNamespace(command="close, exit, quit", cmd="close, exit, quit", description="exit")
]

COMMAND_LIST = [cmd.strip() for item in MAIN_MENU_COMMANDS_LIST for cmd in item.cmd.split(",")]

def cmd_show_help():
    draw_help("main commands help", MAIN_MENU_COMMANDS_LIST)


def main():
    print(f"{Fore.CYAN}Welcome to Personal assistant!")
    print(f"{Fore.CYAN}Select module (book/notes): ")

    command = None
    while True:
        if command is None:
            command = read_command("Command: ", commands=COMMAND_LIST)
            if not command:
                continue

        match command:
            case "hello":
                print(f"{Fore.BLUE}How can I help you?")
            case "help" | "?":
                cmd_show_help()
            case "book":
                command = book_main()
            case "notes":
                command = notes_main()
            case "close" | "exit" | "quit":
                break
            case _:
                print(f"{Fore.RED}Invalid command.")

        command = command if command in {"close", "exit", "quit"} else None
        
    print(f"{Fore.GREEN}Have a nice day!")


if __name__ == "__main__":
    main()