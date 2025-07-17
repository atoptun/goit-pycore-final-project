from typing import cast, Any, Generator
from src.personal_assistant.addr_book.classes import \
    Record, PhoneFactory, EmailFactory, Birthday, PostAddress


def test_record_simple():
    name = "Jonh"
    birthday = "02.02.2000"
    phones = "111111111, 222222222, 333333333"
    emails = "test1@test.com, test2@test.com"
    address = "Ukrain, Lviv, Banders str, 23"
    rec = Record(name)
    rec.birthday = birthday
    rec.phones.extend(PhoneFactory.create(phones))
    rec.emails.extend(EmailFactory.create(emails))
    rec.address = address
    assert len(rec.phones) == 3
    assert len(rec.emails) == 2
    assert str(rec.address) == address.strip()
    assert str(rec.birthday) == birthday

