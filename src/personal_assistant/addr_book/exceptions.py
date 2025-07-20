from personal_assistant.exceptions import ApplicationBaseError, CancelCommand

class ContactBaseError(ApplicationBaseError): ...

class ContactNotFound(ContactBaseError):
    def __init__(self, msg: str = "Contact not found", *args: object) -> None:
        super().__init__(msg, args)


class ContactExist(ContactBaseError):
    def __init__(self, msg: str = "Contact exist", *args: object) -> None:
        super().__init__(msg, args)


class PhoneFormatError(ContactBaseError):
    def __init__(self, msg: str = "Phone format error", *args: object) -> None:
        super().__init__(msg, args)


class EmailFormatError(ContactBaseError):
    def __init__(self, msg: str = "Email format error", *args: object) -> None:
        super().__init__(msg, args)


class BirthdayFormatError(ContactBaseError):
    def __init__(self, msg: str = "Date format error", *args: object) -> None:
        super().__init__(msg, args)
