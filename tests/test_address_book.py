import pytest
from src.personal_assistant.addr_book.classes import AddressBook, Record
from src.personal_assistant.addr_book.commands import load_data, save_data

TEST_ADDR_BOO_FILENAME = "./data/test_addr_book.pkl"

@pytest.fixture
def fresh_addr_book():
    book = AddressBook()
    yield book


@pytest.fixture
def dirty_addr_book():
    book = load_data(TEST_ADDR_BOO_FILENAME)
    yield book
    save_data(book, TEST_ADDR_BOO_FILENAME)


def test_add_record(fresh_addr_book):
    # book = AddressBook()
    record = Record("John")
    fresh_addr_book.add_record(record)
    assert fresh_addr_book.find("john") != None

def test_exist_add_record(dirty_addr_book):
    book = dirty_addr_book
    record = Record("John")
    book.add_record(record)
