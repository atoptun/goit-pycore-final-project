from typing import Any
from src.personal_assistant.common import draw_table


HELP_TABLE_CONFIG = [
    {
        "header": "Command",
        "data_key": "command",
        "style": "bold cyan",
        "width": 20,
        "no_wrap": True
    },
    {
        "header": "Description",
        "data_key": "description",
        "style": "green"
    }
]

def draw_help(caption: str, helps_list: list[Any]):
    """Prints help table from a list of dictionaries"""
    draw_table(
        title=caption,
        columns_config=HELP_TABLE_CONFIG,
        data=helps_list 
    )