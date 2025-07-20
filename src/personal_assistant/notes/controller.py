from colorama import Fore, Back, Style, init
from typing import cast
from personal_assistant.notes import commands
from personal_assistant.notes.classes import Notes
from personal_assistant.common import get_data_path, read_command, load_data, save_data


init(autoreset=True)

NOTES_FILE_PATH = get_data_path("notes.pkl")

def main():
    data = load_data(NOTES_FILE_PATH)
    book = cast(Notes, data) if data else Notes()
    print(f"{Fore.CYAN}Notes contains {len(book.keys())} records")

    while True:
        cmd_str = read_command("Notes command: ", commands=commands.COMMAND_LIST)
        if not cmd_str:
            command = None
            continue
        command, *args = commands.parse_input(cmd_str)

        match command:
            case "help" | "?":
                commands.cmd_show_help()
            case "add":
                print(commands.cmd_add_note(book))
            case "search":
                print(commands.cmd_search_notes(book, args))
            case "edit":
                print(commands.cmd_change_note(book, args))
            case "delete":
                print(commands.cmd_delete_note(book, args))
            case "all":
                print(commands.cmd_show_all(book))
            case "close" | "exit" | "quit" | "back":
                break
            case _:
                print(f"{Fore.RED}Invalid command.")

    save_data(book, NOTES_FILE_PATH)

    return "exit" if command in {"close", "exit", "quit"} else None


if __name__ == "__main__":
    main()
