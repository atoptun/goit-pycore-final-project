import pytest
from src.personal_assistant.notes.classes import NoteRecord, Notes

def test_create_note():
    title = "Title"
    text = "Message \n asdasd\n#tag1 #tag2 tag1"
    rec = NoteRecord(title, text)
    assert len(rec.tags) == 2


def test_add_note():
    notes = Notes()

    title = "Title"
    text = "Message \n asdasd\n#tag1 #tag2 tag1"
    note1 = NoteRecord(title, text)

    with pytest.raises(KeyError, match="Error. Use method add()"):
        notes["qwe"] = note1
    
    notes.add(note1)
    assert len(notes) == 1

    rec = notes[note1.id]
    assert rec.id == note1.id

    title = "Title"
    text = "Message \n asdasd\n#tag10 #tag2 tag12"
    note2 = NoteRecord(title, text)
    notes.add(note2)
    assert len(notes) == 2


