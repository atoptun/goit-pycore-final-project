from colorama import Fore, Back, Style, init
from typing import cast
from personal_assistant.addr_book.classes import AddressBook
from personal_assistant.addr_book import commands
from personal_assistant.common import get_data_path, read_command, load_data, save_data


init(autoreset=True)

ADDR_BOOK_FILENAME = get_data_path("addressbook.pkl")

def main():
    data = load_data(ADDR_BOOK_FILENAME)
    book = cast(AddressBook, data) if data else AddressBook()
    print(f"{Fore.CYAN}Addressbook contains {len(book.keys())} contacts")

    while True:
        cmd_str = read_command("Book command: ", commands=commands.COMMAND_LIST)
        if not cmd_str:
            command = None
            continue
        command, *args = commands.parse_input(cmd_str)

        match command:
            case "hello":
                print(f"{Fore.BLUE}How can I help you?")
            case "help" | "?":
                commands.cmd_show_help()
            case "add":
                print(commands.cmd_add_contact(book, args))
            case "search":
                print(commands.cmd_search_contacts(book, args))
            case "edit":
                print(commands.cmd_edit_contact(book, args))
            case "delete":
                print(commands.cmd_delete_contact(book, args))
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
