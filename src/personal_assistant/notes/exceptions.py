from personal_assistant.exceptions import ApplicationBaseError, CancelCommand

class NoteBaseError(ApplicationBaseError): ...

class NoteNotFound(ApplicationBaseError):
    def __init__(self, msg: str = "Note not found", *args: object) -> None:
        super().__init__(msg, args)
