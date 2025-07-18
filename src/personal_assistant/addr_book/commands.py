import inspect
import sys
from pathlib import Path
from colorama import Fore, Back, Style, init
from functools import wraps
from typing import Callable
from src.personal_assistant.addr_book import exceptions as excp
from src.personal_assistant.addr_book.classes import AddressBook, Record, Phone, Email, PhoneFactory, EmailFactory


init(autoreset=True)

COMMANDS_HELP = """Address book commands:
    add [name]                                    | add contact
    change [name]                                 | edit contact details
    search [value]                                | search contacts by name, phone, email, address
    edit [name]                                   | edit contact
    delete [name]                                 | delete contact
    birthdays [days]                              | show birthdays in coming days (default 7 days)
    all                                           | show all contacts
    help                                          | this help
    back                                          | back to main menu
    close, exit, quit                             | exit
    
"""


def input_error(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except excp.ContactBaseError as e:
            return f"{Fore.RED}{e.strerror}"
        except (ValueError, IndexError) as e:
            if func.__name__ in funcs_local:
                return f"{Fore.RED}Wrong arguments for the command. Type '?' for help."
        except Exception as e:
            return f"{Fore.RED}Error: {e}"
    return wraper


@input_error
def parse_input(line: str) -> tuple:
    """Returns a command and arguments"""
    cmd, *args = line.strip().split()
    return (cmd.strip().lower(), *args)


def contact_info_format(rec: Record) -> str:
    return f"Name: {Fore.YELLOW}{rec.name}{Fore.RESET}, birthday: {Fore.CYAN}{rec.birthday}{Fore.RESET}, phones: {Fore.GREEN}{rec.phones}{Fore.RESET}, email: {Fore.MAGENTA}{rec.emails}{Fore.RESET}"

@input_error
def cmd_add_contact(book: AddressBook, args: list[str]) -> str:
    name = args[0]
    found_contact = book.get(name)

    if found_contact: # TODO: just return error
        print()
        print(found_contact)
        print("We already have the contact. Maybe you wanna edit the contact with command: edit")
        print()
        return

    record = Record(name)

    print("Input contact info")

    phones = input("Phone (10 dig. Example: 1234567890, 0987654321): ")
    phones, errors = PhoneFactory.create(phones)
    record.phones.extend(phones)
    # TODO: show errors

    email = input("Email (Example: test@test.ua, test@test.ua): ")
    emails, errors = EmailFactory.create(email)
    record.emails.extend(emails)
    # TODO: show errors

    birthday = input("Birthday(DD.MM.YYYY): ")
    record.birthday = birthday

    book.add_record(record)

    print()
    print(record)
    print("Contact saved.")
    print()


@input_error
def cmd_search_contacts(book: AddressBook, args: list[str]):
    print()
    print("Search for a contact. You may match the name, phone numbers, emails, or address.")

    search_value = " ".join(args)
    found_contacts = book.find(search_value)

    if not found_contacts:
        print('Not Found Contacts. You can try again: "search"')
        print()
        return

    for record in found_contacts:
        print(record)

    print()


@input_error
def cmd_change_contact(book: AddressBook, args: list[str]) -> str:
    """Command: change <name> - interactive contact editing"""
    if not args:
        name = input("Enter contact name: ")
    else:
        name = args[0]

    record = book.find(name)
    if record is None:
        return f"{Fore.RED}Contact not found."

    print(f"\n{Fore.CYAN}Current contact info:")
    print(contact_info_format(record))
    print(f"\n{Fore.YELLOW}What do you want to edit?")
    print("1. Name")
    print("2. Phone")
    print("3. Email")
    print("4. Birthday")
    print("5. Address")
    print("0. Cancel")

    choice = input("Enter your choice (0-5): ")

    match choice:
        case "1":
            new_name = input("Enter new name: ")
            if new_name and new_name != record.name:
                book.delete(record.name)
                record.name = new_name
                book.add_record(record)
                return f"{Fore.GREEN}Name updated to {new_name}."
            return f"{Fore.RED}Invalid name or no changes."

        case "2":
            current_phone = record.phones[0] if record.phones else "Not set"
            print(f"Current phone: {current_phone}")
            new_phone = input("Enter new phone: ")

            if new_phone:
                record.phones.clear()
                record.phones.append(Phone(new_phone))
                return f"{Fore.GREEN}Phone updated to {new_phone}."
            else:
                return f"{Fore.RED}No phone number entered."

        case "3":
            current_email = record.emails[0] if record.emails else "Not set"
            print(f"Current email: {current_email}")
            new_email = input("Enter new email: ")

            if new_email:
                record.emails.clear()
                record.emails.append(Email(new_email))
                return f"{Fore.GREEN}Email updated to {new_email}."
            else:
                return f"{Fore.RED}No email entered."

        case "4":
            current_bd = record.birthday if record.birthday else "Not set"
            print(f"Current birthday: {current_bd}")
            new_birthday = input("Enter new birthday (DD.MM.YYYY): ")
            record.birthday = new_birthday
            return f"{Fore.GREEN}Birthday updated."

        case "5":
            current_addr = record.address if hasattr(record, 'address') and record.address else "Not set"
            print(f"Current address: {current_addr}")
            new_address = input("Enter new address: ")
            record.address = new_address
            return f"{Fore.GREEN}Address updated."

        case "0":
            return f"{Fore.BLUE}Edit cancelled."

        case _:
            return f"{Fore.RED}Invalid choice."


@input_error
def cmd_show_phones(book: AddressBook, args: list[str]) -> str:
    """Command: phone <name>"""
    name, *_ = args
    rec = book.find(name)
    if rec is None:
        raise excp.ContactNotFound("Contact not found.")
    return f"{Fore.GREEN}{rec.name}'s phones: {Fore.BLUE}{rec.phones}"


@input_error
def cmd_add_birthday(book: AddressBook, args: list[str]) -> str:
    """Command: add-birthday <name> <DD.MM.YYYY>"""
    name, bd, *_ = args
    rec = book.find(name)
    if rec is None:
        raise excp.ContactNotFound("Contact not found.")
    rec.birthday = bd
    return f"{Fore.GREEN}Birthday changed."


@input_error
def cmd_show_birthday(book: AddressBook, args: list[str]) -> str:
    """Command: show-birthday <name>"""
    name, *_ = args
    rec = book.find(name)
    if rec is None:
        raise excp.ContactNotFound("Contact not found.")
    return f"{Fore.GREEN}{rec.name}'s birthday: {Fore.BLUE}{rec.birthday}"


@input_error
def cmd_birthdays(book: AddressBook, args: list[str]) -> str:
    """Command: birthdays"""
    result = f"{Fore.GREEN}Birthdays in this week:{Fore.RESET}\n"
    records = book.get_upcoming_birthdays()
    if not records:
        return f"{Fore.GREEN}No birthdays this week."
    for rec in records:
        result += f"{contact_info_format(rec)}\n"
    return result


@input_error
def cmd_show_all(book: AddressBook, args: list[str]) -> str:
    """Command: all"""
    result = ""
    for rec in book.values():
        result += f"{contact_info_format(rec)}\n"
    return result


def get_function_names():
    current_module = sys.modules[__name__]
    return [
        name for name, obj in inspect.getmembers(current_module, inspect.isfunction)
        if obj.__module__ == current_module.__name__
    ]


funcs_local = get_function_names()
