import inspect
import sys
from pathlib import Path
import types
from colorama import Fore, Back, Style, init
from functools import wraps
from src.personal_assistant.notes import exceptions as excp
from src.personal_assistant.notes.classes import NoteRecord, Notes
from src.personal_assistant.common import promt_pretty, read_command
from src.personal_assistant.notes import views
from src.personal_assistant.views import draw_help


HELP_COMMANDS_LIST = [
    types.SimpleNamespace(command="add", cmd="add", description="add note"),
    types.SimpleNamespace(command="search <tags>", cmd="search", description="search notes by title or content"),
    types.SimpleNamespace(command="edit <id>", cmd="edit", description="edit note"),
    types.SimpleNamespace(command="delete <id>", cmd="delete", description="delete note"),
    types.SimpleNamespace(command="all", cmd="all", description="show all notes"),
    types.SimpleNamespace(command="help, ?", cmd="help", description="this help"),
    types.SimpleNamespace(command="back", cmd="back", description="back to main menu"),
    types.SimpleNamespace(command="close, exit, quit", cmd="close, exit, quit", description="exit")
]

COMMAND_LIST = [cmd.strip() for item in HELP_COMMANDS_LIST for cmd in item.cmd.split(",")]


def input_error(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except excp.NoteBaseError as e:
            return f"{Fore.RED}{e.strerror}"
        except (ValueError, IndexError) as e:
            if func.__name__ in funcs_local:
                return f"{Fore.RED}Wrong arguments for the command. Type '?' for help."
        except Exception as e:
            return f"{Fore.RED}Error: {e}"
    return wraper


@input_error
def parse_input(line: str) -> tuple:
    """Returns a command and arguments"""
    cmd, *args = line.strip().split()
    return (cmd.strip().lower(), *args)


@input_error
def cmd_show_help():
    draw_help("Notes commands help", HELP_COMMANDS_LIST)


@input_error
def cmd_add_note(notes: Notes):
    title = promt_pretty("Enter a title")
    if title is None:
        raise excp.CancelCommand()
    text = promt_pretty("Enter a text the note", multiline=True)
    if text is None:
        raise excp.CancelCommand()

    record = NoteRecord(title, text)

    notes.add(record)

    return "Note added."

@input_error
def cmd_show_all(notes: Notes):
    if not notes.data:
        return "No notes found."
    notes_list = list(notes.data.values())
   
    views.draw_notes("📝 All Notes", notes_list)
    return ""


@input_error
def cmd_search_notes(note: Notes, args: list[str]):
    search_value = " ".join(args)

    if not search_value.strip():
        raise ValueError()

    found_notes = note.find(search_value)

    if not found_notes:
        return "Not found a note. You look all notes with command: all"

    views.draw_notes(f"🔍 Search results for: '{search_value}'", found_notes)
    return ""


def cmd_change_note(notes: Notes, args: list[str]):
    """Command: change title, message"""
    id = args[0]

    record = notes.get(id)

    if not record:
        raise excp.NoteNotFound()

    title = promt_pretty("Title", default_text=record.title)
    if title is None:
        raise excp.CancelCommand()
    record.title = title

    text = promt_pretty("Text", default_text=record.text, multiline=True)
    if text is None:
        raise excp.CancelCommand()
    record.text = text

    return "Note updated."


@input_error
def cmd_delete_note(notes: Notes, args: list[str]) -> str:
    """Command: delete <id>"""
    note_id = args[0]
    record = notes.get(note_id)

    if not record:
        raise excp.NoteNotFound(f"Note with ID '{note_id}' not found")

    views.draw_notes(f"{Fore.RED}Note to delete", [record])

    answer = read_command(f"Are you sure you want to delete this note? (yes/no): ", color="ansired")
    if answer.lower() in ("y", "yes"):
        notes.delete(note_id)
        return f"{Fore.GREEN}Note with ID '{note_id}' deleted successfully!"
    
    return f"{Fore.RED}Note deletion cancelled."


def get_function_names():
    current_module = sys.modules[__name__]
    return [
        name for name, obj in inspect.getmembers(current_module, inspect.isfunction)
        if obj.__module__ == current_module.__name__
    ]


funcs_local = get_function_names()
