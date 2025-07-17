import pytest
from src.personal_assistant.notes.classes import NoteRecord, Notes

def test_create_note():
    rec = NoteRecord()
    rec.title = "Title"
    rec.message = "Message"
    rec.tags = set(["tag1", "tag2", "tag1"])
    assert len(rec.tags) == 2


def test_add_note():
    notes = Notes()
    note1 = NoteRecord()
    note1.title = "Title"
    note1.message = "Message"
    note1.tags = set(["tag1", "tag2", "tag1"])

    with pytest.raises(KeyError, match="Error. Use method add()"):
        notes["qwe"] = note1
    
    notes.add(note1)
    assert len(notes) == 1

    rec = notes[note1.id]
    assert rec.id == note1.id

    notes.update


