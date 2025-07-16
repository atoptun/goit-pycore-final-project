import pickle
from collections import UserList
from typing import Generic, TypeVar, Iterable, Any
from pathlib import Path
from appdirs import user_data_dir
from colorama import Fore, Back, Style, init


T = TypeVar('T')

class UniqueList(UserList, Generic[T]):
    def append(self, item: T) -> None:
        if item not in self.data:
            super().append(item)

    def extend(self, other: Iterable[T]) -> None:
        for item in other:
            self.append(item)

    def insert(self, i: int, item: T) -> None:
        if item not in self.data:
            super().insert(i, item)
    
    def change(self, item: T, new_item: T):
        try:
            self.data.remove(item)
            self.data.append(new_item)
        except ValueError as e:
            pass

    def __str__(self) -> str:
        return '; '.join(str(p) for p in self.data)


def is_dev_mode() -> bool:
    indicators = ["pyproject.toml", "poetry.lock", ".venv"]
    return any(Path(f).exists() for f in indicators)


def get_data_path(filename: str) -> Path:
    if is_dev_mode():
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
    else:
        data_dir = Path(user_data_dir("personal_assistant"))
        data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / filename


def read_command() -> str:
    """Read command and handle Ctrl+C"""
    try:
        return input(f"{Fore.YELLOW}Command:{Fore.RESET} ")
    except KeyboardInterrupt:
        print("\b\bexit")
        return "exit"


def save_data(book: Any, path: Path|str ="data.pkl"):
    """Save data to file"""
    with open(path, "wb") as f:
        pickle.dump(book, f)


def load_data(path: Path|str = "data.pkl") -> Any:
    """Load data from file"""
    try:
        with open(Path(path), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


class ApplicationBaseError(Exception):
    def __init__(self, msg, *args: object) -> None:
        self.strerror = msg
        super().__init__(*args)