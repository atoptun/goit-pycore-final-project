from src.personal_assistant.addr_book import commands
from src.personal_assistant.addr_book.classes import AddressBook
from src.personal_assistant.common import read_command


def test_read_command(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "add John 123456789")
    cmd = read_command()
    assert cmd == "add John 123456789"


def test_cmd_add_contact_success():
    book = AddressBook()
    result = commands.cmd_add_contact(book, ["John", "123456789"])
    assert "added" in result.lower()
    assert book.find("john") != None


def test_cmd_add_contact_fail_args():
    book = AddressBook()
    result = commands.cmd_add_contact(book, ["John"])
    assert "wrong arguments" in result.lower()


def test_cmd_add_contact_fail_phone():
    book = AddressBook()
    result = commands.cmd_add_contact(book, ["John", "1"])
    assert "wrong phone number" in result.lower()

