from colorama import Fore, Back, Style, init
from typing import cast
from src.personal_assistant.notes import commands
from src.personal_assistant.notes.classes import Notes
from src.personal_assistant.common import get_data_path, read_command, load_data, save_data


init(autoreset=True)

NOTES_FILE_PATH = get_data_path("notes.pkl")

def main():
    print(f"{Fore.CYAN}Welcome to the Notes!")

    data = load_data(NOTES_FILE_PATH)
    book = cast(Notes, data) if data else Notes()
    print(f"Notes contains {len(book.keys())} records")

    while True:
        cmd_str = read_command()
        if not cmd_str:
            continue
        command, *args = commands.parse_input(cmd_str)

        match command:
    #         case "hello":
    #             print(f"{Fore.BLUE}How can I help you?")
            case "help" | "?":
                print(commands.COMMANDS_HELP)
    #         case "add":
    #             print(commands.cmd_add_contact(book, args))
    #         case "change":
    #             print(commands.cmd_change_contact(book, args))
    #         case "phone":
    #             print(commands.cmd_show_phones(book, args))
    #         case "add-birthday" | "add-bd":
    #             print(commands.cmd_add_birthday(book, args))
    #         case "show-birthday" | "show-bd":
    #             print(commands.cmd_show_birthday(book, args))
    #         case "birthdays" | "bds":
    #             print(commands.cmd_birthdays(book, args))
    #         case "all":
    #             print(commands.cmd_show_all(book, args))
    #         case "close" | "exit" | "quit":
    #             print(f"{Fore.GREEN}Have a nice day!")
    #             break
            case _:
                print(f"{Fore.RED}Invalid command.")

    # commands.save_data(book, NOTES_FILE_PATH)


if __name__ == "__main__":
    main()
