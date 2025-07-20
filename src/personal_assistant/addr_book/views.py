from colorama import Fore, Back, Style, init
from src.personal_assistant.addr_book.classes import Record
from src.personal_assistant.addr_book.classes import Record
from src.personal_assistant.common import draw_table


def contact_info_format(rec: Record) -> str:
    return f"Name: {Fore.YELLOW}{rec.name}{Fore.RESET}," + \
        f" birthday: {Fore.CYAN}{rec.birthday}{Fore.RESET}," + \
        f" phones: {Fore.GREEN}{rec.phones}{Fore.RESET}," + \
        f" emails: {Fore.GREEN}{rec.emails}{Fore.RESET}," + \
        f" address: {Fore.GREEN}{rec.address}{Fore.RESET},"


CONTACT_TABLE_CONFIG = [
    {
        "header": "Name", 
        "data_key": "name", 
        "style": "bold yellow", 
        "width": 20, 
        "no_wrap": True,
    },
    {
        "header": "Phones", 
        "data_key": "phones", 
        # "style": "bold magenta"
        "width": 20,
    },
    {
        "header": "Emails", 
        "data_key": "emails",
        # "width": 20,
    },
    {
        "header": "Birthday", 
        "data_key": "birthday", 
        "style": "green",
        "width": 20,
    },
    {
        "header": "Address", 
        "data_key": "address", 
        "style": "green",
        "width": 20,
    }
]


def draw_contacts(caption: str, contact_list: list[Record]):
    """Print notes list"""
    draw_table(
        title = caption,
        columns_config = CONTACT_TABLE_CONFIG,
        data = contact_list
    )
