from colorama import Fore, Back, Style, init
from typing import cast
from src.personal_assistant.addr_book.classes import AddressBook
from src.personal_assistant.addr_book import commands
from src.personal_assistant.common import get_data_path, read_command, load_data, save_data


init(autoreset=True)

ADDR_BOOK_FILENAME = get_data_path("addressbook.pkl")

def main():
    print(f"{Fore.CYAN}Welcome to the assistant bot!")

    data = load_data(ADDR_BOOK_FILENAME)
    book = cast(AddressBook, data) if data else AddressBook()
    print(f"Addressbook contains {len(book.keys())} contacts")

    while True:
        cmd_str = read_command()
        if not cmd_str:
            continue
        command, *args = commands.parse_input(cmd_str)

        match command:
            case "hello":
                print(f"{Fore.BLUE}How can I help you?")
            case "help" | "?":
                print(commands.COMMANDS_HELP)
            case "add":
                commands.cmd_add_contact(book)
            case "change":
                print(commands.cmd_change_contact(book, args))
            case "phone":
                print(commands.cmd_show_phones(book, args))
            case "add-birthday" | "add-bd":
                print(commands.cmd_add_birthday(book, args))
            case "show-birthday" | "show-bd":
                print(commands.cmd_show_birthday(book, args))
            case "birthdays" | "bds":
                print(commands.cmd_birthdays(book, args))
            case "all":
                print(commands.cmd_show_all(book, args))
            case "close" | "exit" | "quit" | "back":
                break
            case _:
                print(f"{Fore.RED}Invalid command.")

    save_data(book, ADDR_BOOK_FILENAME)
    
    return "exit" if command in {"close", "exit", "quit"} else None


if __name__ == "__main__":
    main()
