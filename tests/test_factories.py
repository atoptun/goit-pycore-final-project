import pytest
from src.personal_assistant.addr_book.classes import EmailFactory, PhoneFactory


def test_factory_phones():
    line = "123123123, 234234234, 45654"
    phones = PhoneFactory.create(line)
    assert len(phones) == 2


def test_factory_emails():
    line = "test@test.com, test"
    emails, errors = EmailFactory.create(line)
    assert len(emails) == 1
