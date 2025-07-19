from src.personal_assistant.notes.classes import NoteRecord
from src.personal_assistant.common import draw_table


## TODO: add help dict and view


NOTE_TABLE_CONFIG = [
    {
        "header": "ID", 
        "data_key": "id", 
        "style": "dim", 
        "width": 30, 
        "no_wrap": True
    },
    {
        "header": "Title", 
        "data_key": "title", 
        "style": "bold magenta"
    },
    {
        "header": "Text", 
        "data_key": "text"
    },
    {
        "header": "Tags", 
        "data_key": "tags", 
        "justify": "right", 
        "style": "green"
    }
]


def draw_notes(caption: str, notes_list: list[NoteRecord]):
    """Print notes list"""
    draw_table(
        title = caption,
        columns_config = NOTE_TABLE_CONFIG,
        data = notes_list
    )
