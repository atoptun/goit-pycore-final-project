import inspect
import sys
from pathlib import Path
from colorama import Fore, Back, Style, init
from functools import wraps
from typing import Callable
from src.personal_assistant.addr_book import exceptions as excp
from src.personal_assistant.addr_book.classes import AddressBook, Record, Phone, Email, PhoneFactory, EmailFactory
from src.personal_assistant.common import promt_pretty
from src.personal_assistant.addr_book.exceptions import ContactExist, BirthdayFormatError


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

    if found_contact:  # TODO: just return error
        raise ContactExist("Contact already exist!!")

    record = Record(name)
    print("Input contact info")

    phones = promt_pretty("Phone (8-15) dig. Example: 1234567890, 0987654321)")
    phones, errors = PhoneFactory.create(phones)
    record.phones.extend(phones)

    if errors:
        for error in errors:
            print(error)

    address = promt_pretty("Address")
    record.address = address
    # TODO: show errors

    email = promt_pretty("Email (Example: test@test.ua, test@test.ua)")
    emails, errors = EmailFactory.create(email)
    record.emails.extend(emails)

    if errors:
        for error in errors:
            print(error)

    birthday = promt_pretty("Birthday(DD.MM.YYYY)")
    try:
        record.birthday = birthday
    except BirthdayFormatError as err:
        print(err)

    book.add_record(record)

    print()
    print(record)
    print("Contact saved.")
    print()


@input_error
def cmd_search_contacts(book: AddressBook, args: list[str]):
    search_value = " ".join(args)
    found_contacts = book.find(search_value)

    if not found_contacts:
        raise excp.ContactNotFound()

    return "\n".join([str(record) for record in found_contacts])


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
def cmd_edit_contact(book: AddressBook, args: list[str]) -> str:
    """Command: edit <name>"""
    if not args:
        return f"{Fore.RED}Please provide contact name to edit."

    name = args[0]
    records = book.find(name)
    if not records:
        raise excp.ContactNotFound("Contact not found.")

    record = records[0]

    print()
    print(f"{Fore.CYAN}Editing contact: {Fore.YELLOW}{record.name}")
    print(f"{Fore.CYAN}Current info:")
    print(record)
    print()

    from src.personal_assistant.common import promt_pretty

    current_phones = str(record.phones) if record.phones else ""
    new_phones_input = promt_pretty("Phones (Example: 1234567890, 0987654321)", current_phones, multiline=True)

    if new_phones_input is not None and new_phones_input.strip() != current_phones:
        phones, errors = PhoneFactory.create(new_phones_input)
        if errors:
            print(f"{Fore.RED}Errors in phone numbers: {', '.join(errors)}")
        record.phones.clear()
        record.phones.extend(phones)
        print(f"{Fore.GREEN}Phones updated.")

    current_emails = str(record.emails) if record.emails else ""
    new_emails_input = promt_pretty("Emails (Example: test@test.ua, user@example.com)", current_emails, multiline=True)

    if new_emails_input is not None and new_emails_input.strip() != current_emails:
        emails, errors = EmailFactory.create(new_emails_input)
        if errors:
            print(f"{Fore.RED}Errors in emails: {', '.join(errors)}")
        record.emails.clear()
        record.emails.extend(emails)
        print(f"{Fore.GREEN}Emails updated.")

    current_address = str(record.address) if record.address.value else ""
    new_address = promt_pretty("Address", current_address, multiline=True)

    if new_address is not None and new_address.strip() != current_address:
        record.address = new_address.strip()
        print(f"{Fore.GREEN}Address updated.")

    current_birthday = str(record.birthday) if record.birthday.value else ""
    new_birthday = promt_pretty("Birthday (DD.MM.YYYY)", current_birthday)

    if new_birthday is not None and new_birthday.strip() != current_birthday:
        try:
            record.birthday = new_birthday.strip() if new_birthday.strip() else None
            print(f"{Fore.GREEN}Birthday updated.")
        except ValueError as e:
            print(f"{Fore.RED}Invalid birthday format: {e}")

    print()
    print(f"{Fore.CYAN}Updated contact:")
    print(record)

    return f"{Fore.GREEN}Contact updated successfully!"


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

    if args:
        days = int(args[0])
        header = f"{Fore.GREEN}There are birthdays in next {days} days:{Fore.RESET}\n"
        no_birthdays_msg = f"{Fore.GREEN}There are no birthdays in next {days} days."
        records = book.get_upcoming_birthdays(days)
    else:
        header = f"{Fore.GREEN}Birthdays in this week:{Fore.RESET}\n"
        no_birthdays_msg = f"{Fore.GREEN}There are no birthdays this week."
        records = book.get_upcoming_birthdays()

    if not records:
        return no_birthdays_msg

    result = header
    for rec in records:
        result += f"{contact_info_format(rec)}\n"

    return result.strip()


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
