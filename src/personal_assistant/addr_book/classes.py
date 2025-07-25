from collections import UserDict, UserList
from datetime import datetime, timedelta
import re
from personal_assistant.addr_book import exceptions as excp
from personal_assistant.common import UniqueList


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """
    Field Name for address book record
    """
    def __init__(self, value: str):
         super().__init__(str(value).strip().title())

    def __eq__(self, value) -> bool:
         return str(self.value).casefold() == str(value).strip().casefold()


class Phone(Field):
    """
    Field Phone for address book record
    """
    def __init__(self, value: str):
        """
        International format phone number.
        Args:
            value (str): The phone number
        Raises:
            PhoneFormatError: when format of phone is wrong
        """
        phone = self._clear_phone(value)
        self._check_phone_format(phone)
        super().__init__(phone)
    
    @staticmethod
    def _check_phone_format(phone):
        if not(8 <= len(phone) <= 15):
            raise excp.PhoneFormatError(f"Wrong phone number format '{phone}'.")

    @staticmethod
    def _clear_phone(value) -> str:
        return "".join(ch for ch in str(value) if ch.isdigit())

    def __eq__(self, other) -> bool:
        if not isinstance(other, (Phone, str, int)):
            return NotImplemented
        if isinstance(other, Phone):
            return self.value == other.value
        try:
            return self.value == self._clear_phone(str(other))
        except:
            return False
    

class PhoneFactory:
    @staticmethod
    def create(line: str) -> tuple[list[Phone], list[str]]:
        """
        Create phones from line, separator ',' and linebreak
        Returns list of Phone and list or errors
        """
        phones = []
        errors = []
        line = str(line).replace("\n", ",")
        for item in line.split(","):
            if not item.strip():
                continue
            try:
                phone = Phone(item)
                phones.append(phone)
            except excp.PhoneFormatError as e:
                errors.append(e.strerror)
        return phones, errors

class PhoneList(UniqueList[Phone]):
    def __str__(self) -> str:
        return '\n'.join(str(p) for p in self.data)


class Email(Field):
    """
    Field Email for address book record
    """
    def __init__(self, value: str):
        """
        Email format.
        Args:
            value (str): email
        Raises:
            EmailFormatError: when format of email is wrong
        """
        email = self._clear_email(value)
        self._check_email_format(email)
        super().__init__(email)
    
    @staticmethod
    def _check_email_format(value: str):
        """
        Validates basic email format: something@domain.com
        Raises:
            EmailFormatError if invalid.
        """
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, value):
            raise excp.EmailFormatError(f"Wrong email format '{value}'.")
    
    @staticmethod
    def _clear_email(value: str) -> str:
        return str(value).strip().casefold()
         
    def __eq__(self, other) -> bool:
        if not isinstance(other, (Email, str)):
            return NotImplemented
        if isinstance(other, Email):
            return self.value == other.value
        try:
            email = self._clear_email(other)
            self._check_email_format(email)
            return self.value == email 
        except:
            return False


class EmailFactory:
    @staticmethod
    def create(line: str) -> tuple[list[Email], list[str]]:
        """
        Create emails from line, separator ',' and linebreak
        Returns list of Email and list or errors
        """
        emails = []
        errors = []
        line = str(line).replace("\n", ",")
        for item in line.split(","):
            if not item.strip():
                continue
            try:
                email = Email(item)
                emails.append(email)
            except excp.EmailFormatError as e:
                errors.append(e.strerror)
        return emails, errors


class EmailList(UniqueList[Email]):
    def __str__(self) -> str:
        return '\n'.join(str(p) for p in self.data)


class Birthday(Field):
    """
    Field Birthday for address book record. Date format DD.MM.YYYY.
    """
    def __init__(self, value=None):
        self.value = None
        try:
            if value is not None:
                self.value = datetime.strptime(str(value).strip().casefold(), "%d.%m.%Y").date()
        except ValueError:
            raise excp.BirthdayFormatError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y") if self.value is not None else ""


class PostAddress(Field):
    """
    Field Address for address book record.
    """
    def __init__(self, value: str|None = None):
        # TODO: parse address to post, country, sity, street and other
        self.value = None if value is None else value.strip()

    def __str__(self) -> str:
        return self.value if self.value is not None else "Unknown"


class Record:
    """
    Record for address book.
    """
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.__phones: PhoneList = PhoneList()
        self.__emails: EmailList = EmailList()
        self.__birthday = Birthday()
        self.__address = PostAddress()

    @property
    def phones(self) -> PhoneList:
        return self.__phones

    @property
    def emails(self) -> EmailList:
        return self.__emails

    @property
    def birthday(self) -> Birthday:
        return self.__birthday

    @birthday.setter
    def birthday(self, bd: str | None):
        self.__birthday = Birthday(bd)

    @property
    def address(self) -> PostAddress:
        return self.__address
    
    @address.setter
    def address(self, address):
        self.__address = PostAddress(address)

    def __str__(self):
        return f"Name: {self.name}, bd: {self.birthday}, phones: {self.phones}, emails: {self.emails}, address: {self.address}"


class AddressBook(UserDict[str, Record]):
    """
    Address book 
    """
    def add_record(self, record: Record):
        self.data[self._normalize_name(record.name)] = record

    def find(self, criteria: str) -> list[Record]:
        """
        Search for a contact using criteria.
        The criteria may match the name, phone numbers, emails, or address.
        """
        result = []
        criteria = criteria.casefold()
        for rec in self.values():
            if str(rec.name).casefold().find(criteria) >= 0 \
                or str(rec.phones).casefold().find(criteria) >= 0 \
                or str(rec.emails).casefold().find(criteria) >= 0 \
                or str(rec.address).casefold().find(criteria) >= 0 \
            :
                result.append(rec)
                continue

        return result

    def delete(self, name: str):
        self.data.pop(self._normalize_name(name), None)

    def get_upcoming_birthdays(self, days: int=7) -> list[Record]:
        """
        Returns a list of users whose birthdays are within the next 'days' from today.
        If 'days' is not provided, it defaults to 7 days.
        """
        today = datetime.today().date()
        result = []

        end_date = today + timedelta(days=days -1) 

        for key, user in self.data.items():
            bd = user.birthday.value
            if not bd:
                continue
            try:
                bd_this_year = bd.replace(year=today.year)
            except ValueError:
                bd_this_year = bd.replace(year=today.year, day=28)
            if today <= bd_this_year <= end_date:
                if bd_this_year.weekday() > 4: 
                    days_until_monday = (7 - bd_this_year.weekday())
                    bd_this_year += timedelta(days=days_until_monday)
                result.append((user, (bd_this_year - today).days))
        result = sorted(result, key = lambda pair: (pair[1], str(pair[0].name)))
        result = [pair[0] for pair in result]
        return result

    def _normalize_name(self, name: str | Name) -> str:
        return str(name).strip().casefold()

    def get(self, key, default=None):
        return super().get(self._normalize_name(key), default)

    def __getitem__(self, name: str) -> Record:
        return self.data[self._normalize_name(name)]
    
    def __setitem__(self, name: str, item: Record) -> None:
        raise KeyError("Error. Use method add_record()")
