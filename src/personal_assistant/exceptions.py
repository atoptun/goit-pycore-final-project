class ApplicationBaseError(Exception):
    def __init__(self, msg, *args: object) -> None:
        self.strerror = msg
        super().__init__(*args)


class CancelCommand(ApplicationBaseError):
    def __init__(self, msg: str = "Cancel command", *args: object) -> None:
        super().__init__(msg, args)

