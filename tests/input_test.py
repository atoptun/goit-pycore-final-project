from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from src.personal_assistant.common import get_data_path
from src.personal_assistant.common import read_command as common_read_command



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


def read_command(message: str, commands: list[str] = [], default: str = "exit") -> str:
    """Read command and handle Ctrl+C (returns default)"""
    try:
        history = FileHistory(get_data_path(".command_history"))
        command_completer = WordCompleter(commands, ignore_case=True, match_middle=True) 
        return prompt(HTML(f"<ansiyellow>{message}</ansiyellow>"),
                      completer=command_completer, history=history)
    except KeyboardInterrupt:
        return default
    

def promt_autocomlite():
    commands = ["add", "edit", "delete", "list", "exit"]
    command_completer = WordCompleter(commands, ignore_case=True)    
    user_input = prompt("Command: ", completer=command_completer)
    print(f"You typed: {user_input}")


if __name__ == "__main__":
    # text = promt_pretty("Enter text", "qweqwe\nasdsad", multiline=True)
    # text = read_command("Command: ", commands=["add", "edit", "del"])
    text = common_read_command("Command: ", commands=["add", "edit", "del"])
    print("text:" , text)

