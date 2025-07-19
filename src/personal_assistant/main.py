from colorama import Fore, Back, Style, init
from src.personal_assistant.common import read_command
from src.personal_assistant.addr_book.controller import main as book_main
from src.personal_assistant.notes.controller import main as notes_main


COMMANDS_HELP = """Module commands:
    book                                     | address book
    notes                                    | notes
    help, ?                                  | this help
    close, exit, quit                        | exit
    
"""

def cmd_show_help():
    pass


def main():
    print(f"{Fore.CYAN}Welcome to Personal assistant!")
    print(f"{Fore.CYAN}Select module (book/notes): ")

    command = None
    while True:
        if command is None:
            command = read_command()
            if not command:
                continue
        # command, *args = commands.parse_input(cmd_str)

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