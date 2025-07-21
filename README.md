# Personal Assistant

This is a console-based personal assistant application designed to help users manage their contacts and notes efficiently. It provides functionalities to add, search, change, and delete contacts, manage phone numbers, emails, addresses, and birthdays, as well as add, search, change, and delete notes with tags.

## Features

### Address Book Module:

- Add new contacts with name, phone numbers, emails, address, and birthday.
- Search contacts by name, phone, email, or address.
- Edit existing contact details.
- Delete existing contact.
- View upcoming birthdays.
- Display all contacts.

### Notes Module:

- Add new notes with a title and text. Notes automatically extract tags prefixed with `#`.
- Search notes by title, text, or tags.
- Sorts by the number of matching tags (more matches first) and then alphabetically by title.
- Edit existing notes.
- Delete existing note.
- Display all notes.

## How to Use

1.  **Start the application:**
    Once installed, run the `personal-assistant` command in your terminal.

2.  **Navigate Modules:**
    Upon starting, you will be prompted to select a module: `book` for Address Book or `notes` for Notes.

    - Type `book` to enter the Address Book module.
    - Type `notes` to enter the Notes module.

3.  **Module Commands:**
    Inside each module, you can use specific commands:
    - Type `help` or `?` to see available commands for the current module.
    - Type `back` to return to the main module selection menu.
    - Type `close`, `exit`, or `quit` to exit the application from any menu.

## Installation

1.  **Install pipx (if you don't have it):**

    - **Linux (Debian/Ubuntu-based):**
      ```bash
      sudo apt update
      sudo apt install pipx
      pipx ensurepath
      ```
    - **macOS (using Homebrew):**
      ```bash
      brew install pipx
      pipx ensurepath
      ```
    - **Windows / Other Linux (using pip):**
      ```bash
      python3 -m pip install --user pipx
      python3 -m pipx ensurepath
      ```

2.  **Build and Install the application:**
    ```bash
    pipx install git+https://github.com/atoptun/goit-pycore-final-project
    ```

3.  **Run the application:**
    ```bash
    personal-assistant
    ```


# Uninstallation

```bash
pipx uninstall personal-assistant
```
