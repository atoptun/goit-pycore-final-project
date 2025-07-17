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
    return f"Name: {Fore.YELLOW}{rec.name}{Fore.RESET}, birthday: {Fore.CYAN}{rec.birthday}{Fore.RESET}, phones: {Fore.GREEN}{rec.phones}{Fore.RESET}"


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
    """Command: change <name> <old_phone> <new_phone>"""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise excp.ContactNotFound("Contact not found.")
    if record.phones.change(Phone(old_phone), Phone(new_phone)):
        return f"{Fore.GREEN}Phone number changed."
    else:
        return f"{Fore.RED}Phone number not found."


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
