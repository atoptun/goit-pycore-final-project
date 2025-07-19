import inspect
import sys
from pathlib import Path
from colorama import Fore, Back, Style, init
from functools import wraps
from src.personal_assistant.notes import exceptions as excp
from src.personal_assistant.notes.classes import NoteRecord, Notes
from src.personal_assistant.common import promt_pretty
from src.personal_assistant.notes import views



COMMANDS_HELP = """Notes commands:
    add                                     | add note
    search [value]                          | search notes by title or content
    edit [id]                               | edit note
    delete [id]                             | delete note
    all                                     | show all notes
    help                                    | this help
    back                                    | back to main menu
    close, exit, quit                       | exit
    
"""


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
    # show help from common view
    pass


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

    return "\n".join([str(record) for record in found_notes])


def get_function_names():
    current_module = sys.modules[__name__]
    return [
        name for name, obj in inspect.getmembers(current_module, inspect.isfunction)
        if obj.__module__ == current_module.__name__
    ]


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


funcs_local = get_function_names()
