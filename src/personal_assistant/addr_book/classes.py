from collections import UserDict, UserList
from datetime import datetime, timedelta
from src.personal_assistant.addr_book import exceptions as excp
from src.personal_assistant.common import UniqueList


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
         super().__init__(str(value).strip().capitalize())

    def __eq__(self, value) -> bool:
         return str(self.value).lower() == str(value).strip().lower()


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
        super().__init__(value)
    
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
    def create(line: str) -> list[Phone]:
        """Create phones from line, separator ',' """
        result = []
        for item in line.split(","):
            try:
                phone = Phone(item)
                result.append(phone)
            except:
                pass # silent
        return result


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
        super().__init__(value)
    
    @staticmethod
    def _check_email_format(value: str):
        # TODO: regexp
        if str(value).count("@") != 1:
            raise excp.EmailFormatError(f"Wrong email format '{value}'.")
    
    @staticmethod
    def _clear_email(value: str) -> str:
        return str(value).strip().lower()
         
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
    def create(line: str) -> list[Phone]:
        """Create emails from line, separator ',' """
        result = []
        for item in line.split(","):
            try:
                email = Phone(item)
                result.append(email)
            except:
                pass # silent
        return result
    

class Birthday(Field):
    """
    Field Birthday for address book record
    """
    def __init__(self, value):
        self.value = None
        try:
            if value is not None:
                self.value = datetime.strptime(str(value), "%d.%m.%Y").date()
        except ValueError:
            raise excp.BirthdayFormatError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y") if self.value is not None else "Unknown"


class EmailList(UniqueList[Email]): ...

class PhoneList(UniqueList[Phone]): ...


# class PhoneList(UserList):
#     def __setitem__(self, i, item):
#         obj = Phone(str(item))
#         if obj not in self.data:
#             self.data[i] = obj

#     def append(self, item: str):
#         obj = Phone(str(item))
#         if obj not in self.data:
#             self.data.append(obj)

#     def insert(self, i, item):
#         obj = Phone(str(item))
#         if obj not in self.data:
#             self.data.insert(i, obj)

#     def add(self, phone: str) -> bool:
#         phone_obj = Phone(phone)
#         count = len(self.data)
#         self.data.append(phone_obj)
#         return count != len(self.data)

#     def delete(self, phone: str) -> bool:
#         phone_obj = Phone(phone)
#         for p in self.data:
#             if p == phone_obj:
#                 self.data.remove(p)
#                 return True
#         return False
        
#     def edit(self, phone_old: str, phone_new: str) -> bool:
#         phone_old_obj = Phone(phone_old)
#         for i, p in enumerate(self.data):
#             if p == phone_old_obj:
#                 self.data[i] = Phone(phone_new)
#                 return True
#         return False
        
#     def find(self, phone: str):
#         phone_obj = Phone(phone)
#         return next((p for p in self.data if p == phone_obj), None)
    
#     def __str__(self) -> str:
#         return '; '.join(str(p) for p in self.data)


class Record:
    """
    Record for address book.
    """
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.__phones: PhoneList = PhoneList()
        self.__emails: EmailList = EmailList()
        self.__birthday = Birthday(None)

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
    def birthday(self, bd: str):
        self.__birthday = Birthday(bd)

    def __str__(self):
        return f"Name: {self.name}, bd: {self.birthday}, phones: {self.phones}"


class AddressBook(UserDict[str, Record]):
    """
    Address book 
    """
    def add_record(self, record: Record):
        self.data[self._normalize_name(record.name)] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(self._normalize_name(name))

    def delete(self, name: str):
        self.data.pop(self._normalize_name(name), None)

    def get_upcoming_birthdays(self):
        """Returns a list of users who need to be congratulated during the week."""
        today = datetime.today().date()
        result = []
        for key, user in self.data.items():
            bd = user.birthday.value
            if not bd:
                continue
            try:
                bd = bd.replace(year=today.year)
            except ValueError: 
                bd = bd.replace(year=today.year, day=28)

            if 0 <= (bd - today).days <= 6:
                if (wd := bd.weekday()) > 4:
                    bd += timedelta(7 - wd)
                result.append(user)
        return result

    def _normalize_name(self, name: str | Name) -> str:
        return str(name).strip().lower()

    def __getitem__(self, name: str) -> Record:
        return self.data[self._normalize_name(name)]
    
    def __setitem__(self, name: str, item: Record) -> None:
        self.data[self._normalize_name(name)] = item
