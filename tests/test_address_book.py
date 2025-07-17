import pytest
from typing import cast, Any, Generator
from src.personal_assistant.addr_book.classes import \
    AddressBook, Record, PhoneFactory, EmailFactory
from src.personal_assistant.common import load_data, save_data

TEST_ADDR_BOO_FILENAME = "./data/test_addr_book.pkl"

@pytest.fixture
def fresh_addr_book() -> Generator[AddressBook, Any, None]:
    book = AddressBook()
    yield book


@pytest.fixture
def dirty_addr_book() -> Generator[AddressBook, Any, None]:
    data = load_data(TEST_ADDR_BOO_FILENAME)
    book = cast(AddressBook, data) if data else AddressBook()
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

def test_find_contacts(fresh_addr_book):
    book = fresh_addr_book

    rec1 = Record("John")
    rec1.birthday = "02.02.2000"
    phones, errors = PhoneFactory.create("111111111, 222222222, 333333333")
    rec1.phones.extend(phones)
    emails, errors = EmailFactory.create("test1@test.com, test2@test.com")
    rec1.emails.extend(emails)
    rec1.address = "Ukrain, Lviv, Smith str, 23"
    book.add_record(rec1)

    rec2 = Record("John Smith")
    rec2.birthday = "02.02.2000"
    phones, errors = PhoneFactory.create("123123123, 234234234, 345345345")
    rec2.phones.extend(phones)
    emails, errors = EmailFactory.create("test1@test.ua, test2@test.ua")
    rec2.emails.extend(emails)
    rec2.address = "Ukrain, Chernihiv, S.Bandera str, 23"
    book.add_record(rec2)

    res = book.find("kiyv")
    assert len(res) == 0

    res = book.find("john")
    assert len(res) == 2

    res = book.find("smith")
    assert len(res) == 2

    res = book.find("1111111")
    assert len(res) == 1

    res = book.find("test.ua")
    assert len(res) == 1

    res = book.find("test.com")
    assert len(res) == 1
