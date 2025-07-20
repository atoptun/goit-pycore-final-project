import pytest
from personal_assistant.notes.classes import NoteRecord, Notes

def test_create_note():
    title = "Title"
    text = "Message \n asdasd\n#tag1 #tag2 tag1"
    rec = NoteRecord(title, text)
    assert len(rec.tags) == 2


def test_add_note():
    notes = Notes()

    note = notes.get("123123")
    assert note is None

    title = "Title"
    text = "Message \n asdasd\n#tag1 #tag2 tag1"
    note1 = NoteRecord(title, text)

    with pytest.raises(KeyError, match="Error. Use method add()"):
        notes["qwe"] = note1
    
    notes.add(note1)
    assert len(notes) == 1

    rec = notes[note1.id]
    assert rec is note1

    title = "Title"
    text = "Message \n asdasd\n#tag10 #tag2 tag12"
    note2 = NoteRecord(title, text)
    notes.add(note2)
    assert len(notes) == 2

    note = notes.get(note2.id)
    assert note is note2


def test_delete_note():
    notes = Notes()

    title = "Title"
    text = "Message \n asdasd\n#tag1 #tag2 tag1"
    note1 = NoteRecord(title, text)

    notes.add(note1)
    assert len(notes) == 1

    title = "Title"
    text = "Message \n asdasd\n#tag10 #tag2 tag12"
    note2 = NoteRecord(title, text)
    notes.add(note2)
    assert len(notes) == 2

    note = notes.delete("123213")
    assert note is None

    note = notes.delete(note1.id)
    assert note == note1


def test_find_tags():
    notes = Notes()

    notes_list = [
        ["Title 2", "Message 2 \n #tag10 #tag2 tag12"],
        ["Title 3", "Message 3 \n #tag1 #tag21 tag2"],
        ["Title 4", "Message 5 \n #tag12 #tag21 tag3"],
        ["Title 5", "Message 5 \n #tag2 #tag12 tag3"],
        ["Title 1", "Message 1 \n #tag1 #tag2 tag1"],
    ]

    for note in notes_list:
        note_rec = NoteRecord(note[0], note[1])
        notes.add(note_rec)

    res = notes.find("tag1")
    assert len(res) == 2 \
        and res[0].title == "Title 1" \
        and res[1].title == "Title 3"

    res = notes.find("tag1 tag2")
    assert len(res) == 4 \
        and res[0].title == "Title 1" \
        and res[1].title == "Title 3" \
        and res[2].title == "Title 2" \
        and res[3].title == "Title 5"


