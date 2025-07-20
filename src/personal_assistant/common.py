import pickle
from collections import UserList
from typing import Generic, TypeVar, Iterable, List, Dict, Any
from pathlib import Path
from appdirs import user_data_dir
from colorama import Fore, Back, Style, init
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from rich.console import Console
from rich.table import Table
from rich.text import Text
import rich.box as box


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


def promt_pretty(message: str, default_text: str = "", multiline: bool = False) -> str | None:
    """Read pretty user input and handle Ctrl+C"""
    try:
        message = f"{message} (Alt+Enter or Esc→Enter to end):\n" if multiline else f"{message}: "
        return prompt(HTML(f"<ansimagenta>{message}</ansimagenta>"), 
                      default=default_text, 
                      multiline=multiline
                      )
    except KeyboardInterrupt as e:
        return None


# Used for promt command
cmd_history = FileHistory(get_data_path(".command_history"))
promt_session = PromptSession(
    history=cmd_history,
    complete_style=CompleteStyle.READLINE_LIKE,
    complete_while_typing=False,
)

class FirstWordOnlyCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        if not document.text_before_cursor.strip():
            return
        if " " in document.text_before_cursor:
            return

        yield from super().get_completions(document, complete_event)


def read_command(message: str = "Command: ", commands: list[str] = [], default: str = "exit", color: str = "ansiyellow") -> str:
    """Read command and handle Ctrl+C (returns default)"""
    try:
        command_completer = FirstWordOnlyCompleter(commands , ignore_case=True, match_middle=True)
        return promt_session.prompt(HTML(f"<{color}>{message}</{color}>"),
                      completer=command_completer)
    except KeyboardInterrupt:
        return default


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


def draw_table(title: str, columns_config: List[Dict], data: List[Any]):
    console = Console()
    table = Table(
        title=title, 
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED
    )
    
    for col_config in columns_config:
        config = col_config.copy()
        config.pop('data_key', None) 
        table.add_column(config.pop('header'), **config)
    
    for i, item in enumerate(data):
        row_values = []
        for col_config in columns_config:
            data_key = col_config['data_key']
            value = getattr(item, data_key, "N/A")
            if isinstance(value, (frozenset, set)):
                value = ", ".join(map(str, value)) if value else ""
            row_values.append(str(value))
        
        table.add_row(*row_values)

        if i < len(data) - 1:
            separator_line = Text("─" * 10, style="bright_black")
            separator_row = [separator_line for _ in columns_config]
            table.add_row(*separator_row)            

    console.print(table)
