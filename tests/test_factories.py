import pytest
from src.personal_assistant.addr_book.classes import EmailFactory, PhoneFactory


def test_factory_phones():
    line = "123123123, 234234234, \n 45654"
    phones, errors = PhoneFactory.create(line)
    assert len(phones) == 2


def test_factory_emails():
    line = "test@test.com, \n test2@test.com \n tra"
    emails, errors = EmailFactory.create(line)
    assert len(emails) == 2
