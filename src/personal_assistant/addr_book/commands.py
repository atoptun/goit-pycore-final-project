import inspect
import sys
from pathlib import Path
from colorama import Fore, Back, Style, init
from functools import wraps
from typing import Callable
from src.personal_assistant.addr_book import exceptions as excp
from src.personal_assistant.addr_book.classes import AddressBook, Record, Phone, Email


init(autoreset=True)

COMMANDS_HELP = """Address book commands:
    add [name] [phone]                      | add contact or phone
    change [name] [old phone] [new phone]   | change contact's phone
    phone [name]                            | show contatc's phones
    add-birthday [name] [birthday]          | add contact's birthday
    add-bd                                  | alias add-birthday
    show-birthday [name]                    | show contact's birthday
    show-bd                                 | alias show-birthday
    birthdays                               | show birthdays this week
    bds                                     | alias birthdays
    all                                     | show all contacts
    hello                                   | hello
    help, ?                                 | this help
    back                                    | back to main menu
    close, exit, quit                       | exit
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
    """Command: add <name> <phone>"""
    name, phone, *_ = args
    record = book.find(name)
    msg = f"{Fore.GREEN}Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = f"{Fore.GREEN}Contact added."
    if phone:
        record.phones.append(Phone(phone))
    return msg


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
