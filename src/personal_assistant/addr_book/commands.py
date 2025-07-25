import inspect
import sys
from pathlib import Path
import types
from colorama import Fore, Back, Style, init
from functools import wraps
from typing import Callable
from personal_assistant.addr_book import exceptions as excp
from personal_assistant.addr_book.classes import AddressBook, Record, Phone, Email, PhoneFactory, EmailFactory, Birthday
from personal_assistant.common import promt_pretty, read_command
from personal_assistant.addr_book.exceptions import ContactExist, BirthdayFormatError
from personal_assistant.addr_book import views
from personal_assistant.views import draw_help


init(autoreset=True)

ADDRESS_BOOK_COMMANDS_LIST = [
    types.SimpleNamespace(command="add <name>", cmd="add", description="add contact"),
    types.SimpleNamespace(command="search <criteria>", cmd="search", description="search contacts by name, phone, email, address"),
    types.SimpleNamespace(command="edit <name>", cmd="edit", description="edit contact"),
    types.SimpleNamespace(command="delete <name>", cmd="delete", description="delete contact"),
    types.SimpleNamespace(command="birthdays <days>", cmd="birthdays", description="show birthdays in coming days (default 7 days)"),
    types.SimpleNamespace(command="all", cmd="all", description="show all contacts"),
    types.SimpleNamespace(command="help, ?", cmd="help", description="this help"),
    types.SimpleNamespace(command="back", cmd="back", description="back to main menu"),
    types.SimpleNamespace(command="close, exit, quit", cmd="close, exit, quit", description="exit")
]

COMMAND_LIST = [cmd.strip().casefold() for item in ADDRESS_BOOK_COMMANDS_LIST for cmd in str(item.cmd).split(",")]


def input_error(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except excp.ApplicationBaseError as e:
            return f"{Fore.RED}{e.strerror}"
        except (ValueError, IndexError) as e:
            if func.__name__ in funcs_local:
                return f"{Fore.RED}Wrong arguments for the command. Type '?' for help."
        except Exception as e:
            return f"{Fore.RED}Error: {e}"
    return wraper


@input_error
def cmd_show_help():
    draw_help("Addressbook commands help", ADDRESS_BOOK_COMMANDS_LIST)


@input_error
def parse_input(line: str):
    """Returns a command and arguments"""
    cmd, *args = line.strip().split()
    return (cmd.strip().casefold(), *args)


@input_error
def cmd_add_contact(book: AddressBook, args: list[str]) -> str:
    name = " ".join(args)
    found_contact = book.get(name)

    if found_contact:
        raise ContactExist("Contact already exist!!")

    record = Record(name)
    print(f"Input contact info for {name}")

    phones_str = promt_pretty("Phones (8-15) dig", multiline=True)
    if phones_str is None:
        raise excp.CancelCommand()
    phones, errors = PhoneFactory.create(phones_str)
    record.phones.extend(phones)

    if errors:
        print(f"{Fore.RED}{", ".join(errors)}")

    email_str = promt_pretty("Emails", multiline=True)
    if email_str is None:
        raise excp.CancelCommand()
    emails, errors = EmailFactory.create(email_str)
    record.emails.extend(emails)

    if errors:
        print(f"{Fore.RED}{", ".join(errors)}")

    address = promt_pretty("Address", multiline=True)
    record.address = address

    birthday = promt_pretty("Birthday (DD.MM.YYYY)")
    if birthday is None:
        raise excp.CancelCommand()
    try:
        if birthday:
            record.birthday = birthday if birthday.casefold().strip() else None
    except BirthdayFormatError as err:
        print(f"{Fore.RED}{err.strerror}")

    book.add_record(record)

    return f"{Fore.GREEN}Contact saved."


@input_error
def cmd_search_contacts(book: AddressBook, args: list[str]):
    search_value = " ".join(args)
    found_contacts = book.find(search_value)

    if not found_contacts:
        raise excp.ContactNotFound()

    views.draw_contacts(f"🔍 Search results for: '{search_value}'", found_contacts)
    return ""


@input_error
def cmd_edit_contact(book: AddressBook, args: list[str]) -> str:
    """Command: edit <name>"""
    name = " ".join(args)
    record = book.get(name)
    if not record:
        raise excp.ContactNotFound(f"Contact '{name}' not found")

    current_phones = str(record.phones)
    new_phones = promt_pretty("Phones", current_phones, multiline=True)
    if new_phones is None:
        raise excp.CancelCommand()

    phones, errors = PhoneFactory.create(new_phones)
    if errors:
        print(f"{Fore.RED}{', '.join(errors)}")

    current_emails = str(record.emails)
    new_emails = promt_pretty("Emails", current_emails, multiline=True)
    if new_emails is None:
        raise excp.CancelCommand()

    emails, errors = EmailFactory.create(new_emails)
    if errors:
        print(f"{Fore.RED}{', '.join(errors)}")

    current_address = str(record.address)
    new_address = promt_pretty("Address", current_address, multiline=True)
    if new_address is None:
        raise excp.CancelCommand()

    current_birthday = str(record.birthday)
    new_birthday = promt_pretty("Birthday (DD.MM.YYYY)", current_birthday)
    if new_birthday is None:
        raise excp.CancelCommand()

    birthday = str(record.birthday)
    try:
        new_birthday = new_birthday.casefold().strip()
        new_birthday = new_birthday if new_birthday else None
        birthday = str(Birthday(new_birthday)) if new_birthday else None
    except BirthdayFormatError as e:
        print(f"{Fore.RED}{e.strerror}")

    answer = read_command("Save changes (yes/no): ")
    if answer.casefold() not in ("yes", "y"):
        return ""

    record.phones.clear()
    record.phones.extend(phones)
    record.emails.clear()
    record.emails.extend(emails)
    record.address = new_address
    record.birthday = birthday
    
    return f"{Fore.GREEN}Contact updated successfully!"


@input_error
def cmd_delete_contact(book: AddressBook, args: list[str]) -> str:
    """Command: delete <name>"""
    name = " ".join(args)
    record = book.get(name)
    if not record:
        raise excp.ContactNotFound(f"Contact '{name}' not found")

    views.draw_contacts(f"{Fore.RED}Contact to delete", [record])

    answer = read_command(f"Are you sure you want to delete this contact? (yes/no): ", color="ansired")
    if answer.casefold() in ("y", "yes"):
        book.delete(name)
        return f"{Fore.GREEN}Contact '{name}' deleted successfully!"
    
    return f"{Fore.RED}Contact deletion cancelled."


@input_error
def cmd_birthdays(book: AddressBook, args: list[str]) -> str:
    """Command: birthdays"""
    days = int(args[0]) if len(args) > 0 else 7

    records = book.get_upcoming_birthdays(days)

    if not records:
        return f"{Fore.GREEN}There are no birthdays in next {days} days."

    views.draw_contacts(f"There are birthdays in next {days} days:", records)

    return ""


@input_error
def cmd_show_all(book: AddressBook, args: list[str]) -> str:
    """Command: all"""
    contacts = list(book.values())
    views.draw_contacts("Contact list", contacts)
    return ""


def get_function_names():
    current_module = sys.modules[__name__]
    return [
        name for name, obj in inspect.getmembers(current_module, inspect.isfunction)
        if obj.__module__ == current_module.__name__
    ]


funcs_local = get_function_names()

