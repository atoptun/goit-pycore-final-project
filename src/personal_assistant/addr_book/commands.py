import inspect
import sys
from pathlib import Path
import types
from colorama import Fore, Back, Style, init
from functools import wraps
from typing import Callable
from src.personal_assistant.addr_book import exceptions as excp
from src.personal_assistant.addr_book.classes import AddressBook, Record, Phone, Email, PhoneFactory, EmailFactory, Birthday
from src.personal_assistant.common import promt_pretty, read_command
from src.personal_assistant.addr_book.exceptions import ContactExist, BirthdayFormatError
from personal_assistant.addr_book import views
from src.personal_assistant.views import draw_help


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

COMMAND_LIST = [cmd.strip() for item in ADDRESS_BOOK_COMMANDS_LIST for cmd in item.cmd.split(",")]


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
def cmd_show_help():
    draw_help("Addressbook commands help", ADDRESS_BOOK_COMMANDS_LIST)


@input_error
def parse_input(line: str) -> tuple:
    """Returns a command and arguments"""
    cmd, *args = line.strip().split()
    return (cmd.strip().lower(), *args)


@input_error
def cmd_add_contact(book: AddressBook, args: list[str]) -> str:
    name = args[0]
    found_contact = book.get(name)

    if found_contact:
        raise ContactExist("Contact already exist!!")

    record = Record(name)
    print("Input contact info")

    phones_str = promt_pretty("Phones (8-15) dig", multiline=True)
    if phones_str is None:
        raise excp.CancelCommand()
    phones, errors = PhoneFactory.create(phones_str)
    record.phones.extend(phones)

    if errors:
        for error in errors:
            print(error)

    email_str = promt_pretty("Email (Example: test@test.ua, test@test.ua)", multiline=True)
    if email_str is None:
        raise excp.CancelCommand()
    emails, errors = EmailFactory.create(email_str)
    record.emails.extend(emails)

    if errors:
        for error in errors:
            print(error)

    address = promt_pretty("Address", multiline=True)
    record.address = address

    birthday = promt_pretty("Birthday(DD.MM.YYYY)")
    if birthday is None:
        raise excp.CancelCommand()
    try:
        record.birthday = birthday
    except BirthdayFormatError as err:
        print(err.strerror)

    book.add_record(record)

    return "Contact saved."


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
    name = args[0]
    record = book.get(name)
    if not record:
        raise excp.ContactNotFound(f"Contact '{name}' not found")

    # print()
    # print(f"{Fore.CYAN}Editing contact: {Fore.YELLOW}{record.name}")
    # print(f"{Fore.CYAN}Current info:")
    # print(record)
    # print()

    # from src.personal_assistant.common import promt_pretty

    current_phones = str(record.phones) # if record.phones else ""
    # print(f"{Fore.GREEN}Edit phones (current: {current_phones})")
    new_phones = promt_pretty("Phones", current_phones, multiline=True)
    if new_phones is None:
        raise excp.CancelCommand()

    # if new_phones is not None and new_phones.strip() != current_phones:
    phones, errors = PhoneFactory.create(new_phones)
    if errors:
        print(f"{Fore.RED}Errors in phone numbers: {', '.join(errors)}")
    # record.phones.clear()
    # record.phones.extend(phones)
    # print(f"{Fore.GREEN}Phones updated.")

    current_emails = str(record.emails) # if record.emails else ""
    # print(f"{Fore.GREEN}Edit emails (current: {current_emails})")
    new_emails = promt_pretty("Emails", current_emails, multiline=True)
    if new_emails is None:
        raise excp.CancelCommand()

    # if new_emails is not None and new_emails.strip() != current_emails:
    emails, errors = EmailFactory.create(new_emails)
    if errors:
        print(f"{Fore.RED}Errors in emails: {', '.join(errors)}")
    # record.emails.clear()
    # record.emails.extend(emails)
    # print(f"{Fore.GREEN}Emails updated.")

    current_address = str(record.address) # if record.address.value else ""
    # print(f"{Fore.GREEN}Edit address (current: {current_address})")
    new_address = promt_pretty("Address", current_address, multiline=True)
    if new_address is None:
        raise excp.CancelCommand()

    # if new_address is not None and new_address.strip() != current_address:
    # record.address = new_address.strip()
    # print(f"{Fore.GREEN}Address updated.")

    current_birthday = str(record.birthday) # if record.birthday.value else ""
    # print(f"{Fore.GREEN}Edit birthday (current: {current_birthday})")
    new_birthday = promt_pretty("Birthday (DD.MM.YYYY)", current_birthday)
    if new_birthday is None:
        raise excp.CancelCommand()

    # if new_birthday is not None and new_birthday.strip() != current_birthday:
    birthday = str(record.birthday)
    try:
        birthday = Birthday(new_birthday) # new_birthday.strip() if new_birthday.strip() else None
        # print(f"{Fore.GREEN}Birthday updated.")
    except ValueError as e:
        print(f"{Fore.RED}Invalid birthday format: {e}")

    # print()
    # print(f"{Fore.CYAN}Updated contact:")
    # print(record)

    y_n = read_command("Save changes (yes\\no): ")
    if y_n == "no" or y_n == "n":
        return ""

    record.phones.clear()
    record.phones.extend(phones)
    record.emails.clear()
    record.emails.extend(emails)
    record.address = new_address
    record.birthday = str(birthday)
    
    return f"{Fore.GREEN}Contact updated successfully!"


@input_error
def cmd_delete_contact(book: AddressBook, args: list[str]) -> str:
    """Command: delete <name>"""
    name = args[0]
    record = book.get(name)
    if not record:
        raise excp.ContactNotFound(f"Contact '{name}' not found")

    print(f"{Fore.CYAN}Contact to delete:")
    print(record)
    print()

    y_n = read_command("Are you sure you want to delete this contact? (yes\\no): ")
    if y_n == "no" or y_n == "n":
        return f"{Fore.YELLOW}Contact deletion cancelled."

    book.delete(name)
    return f"{Fore.GREEN}Contact '{name}' deleted successfully!"


# @input_error
# def cmd_show_phones(book: AddressBook, args: list[str]) -> str:
#     """Command: phone <name>"""
#     name, *_ = args
#     rec = book.find(name)
#     if rec is None:
#         raise excp.ContactNotFound("Contact not found.")
#     return f"{Fore.GREEN}{rec.name}'s phones: {Fore.BLUE}{rec.phones}"


# @input_error
# def cmd_add_birthday(book: AddressBook, args: list[str]) -> str:
#     """Command: add-birthday <name> <DD.MM.YYYY>"""
#     name, bd, *_ = args
#     rec = book.find(name)
#     if rec is None:
#         raise excp.ContactNotFound("Contact not found.")
#     rec.birthday = bd
#     return f"{Fore.GREEN}Birthday changed."


# @input_error
# def cmd_show_birthday(book: AddressBook, args: list[str]) -> str:
#     """Command: show-birthday <name>"""
#     name, *_ = args
#     rec = book.find(name)
#     if rec is None:
#         raise excp.ContactNotFound("Contact not found.")
#     return f"{Fore.GREEN}{rec.name}'s birthday: {Fore.BLUE}{rec.birthday}"


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
        # result += f"{views.contact_info_format(rec)}\n"
        views.draw_contacts("Contact list", records)

    return result.strip()


@input_error
def cmd_show_all(book: AddressBook, args: list[str]) -> str:
    """Command: all"""
    result = ""
    contacts = list(book.values())
    views.draw_contacts("Contact list", contacts)
    return ""
    # for rec in book.values():
    #     result += f"{views.contact_info_format(rec)}\n"
    # return result


def get_function_names():
    current_module = sys.modules[__name__]
    return [
        name for name, obj in inspect.getmembers(current_module, inspect.isfunction)
        if obj.__module__ == current_module.__name__
    ]


funcs_local = get_function_names()

