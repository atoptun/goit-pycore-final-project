from collections import UserDict
import ulid


class NoteRecord(object):
    def __init__(self, title: str, text: str) -> None:
        self.__id = ulid.new().str
        self.__tags = set()
        self.title = title
        self.text = text

    @property
    def id(self):
        return self.__id

    @property
    def tags(self):
        return self.__tags

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
        words = text.replace("\n", " ").split(" ")
        tags = set([word.strip("#") for word in words if word.startswith("#")])
        self.__tags = tags

    def __str__(self) -> str:
        return f"id: {self.id}, title: {self.title}, message: {self.text}, tags: {self.tags}"


class Notes(UserDict[str, NoteRecord]):

    def add(self, note: NoteRecord):
        self.data[note.id] = note

    def delete(self, id: str):
        self.data.pop(str(id).upper())

    def __setitem__(self, key: str, item: NoteRecord) -> None:
        raise KeyError("Error. Use method add()")

    def __getitem__(self, key: str) -> NoteRecord:
        return super().__getitem__(str(key).upper())

    def find(self, criteria: str) -> list[NoteRecord]:
        """
        Search for a note using criteria.
        The criteria may match the title, text, or tags.
        """
        result = []
        criteria = criteria.lower()
        criteria_words = set(criteria.split(" "))

        for rec in self.values():
            if str(rec.title).lower().find(criteria) >= 0 \
                    or str(rec.text).lower().find(criteria) >= 0 \
                    or bool(rec.tags & criteria_words):
                result.append(rec)

        return result
