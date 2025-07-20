from collections import UserDict
import ulid


class NoteRecord(object):
    def __init__(self, title: str, text: str, id: str | None = None) -> None:
        self.__id = str(id or ulid.new().str).upper()
        self.__tags = frozenset()
        self.title = title
        self.text = text

    @property
    def id(self):
        return self.__id

    @property
    def tags(self):
        """Note tags"""
        return self.__tags

    @property
    def title(self):
        """Note title"""
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def text(self):
        """Note text"""
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
        self.__tags = self.extract_tags(text)

    @staticmethod
    def extract_tags(text: str) -> frozenset[str]:
        words = text.replace("\n", " ").split()
        return frozenset([word.strip("#") for word in words if word.startswith("#")])
    
    def __str__(self) -> str:
        return f"id: {self.id}, title: {self.title}, message: {self.text}, tags: {self.tags}"


class Notes(UserDict[str, NoteRecord]):

    def __normalize_key(self, key: str) -> str:
        return str(key).upper()
    
    def add(self, note: NoteRecord) -> None:
        """
        Add note. 
        Raises:
            KeyError: if duplicate note ID
        """
        if note.id in self.data:
            raise KeyError(f"Note with id {note.id} already exists.")
        self.data[note.id] = note

    def delete(self, key: str) -> NoteRecord | None:
        """
        Delete note.
        Returns deleted note or None if not found
        """
        return self.data.pop(self.__normalize_key(key), None)

    def get(self, key, default=None) -> NoteRecord | None:
        """Returns note by ID or None if not found"""
        return super().get(self.__normalize_key(key), default)

    def __setitem__(self, key: str, item: NoteRecord) -> None:
        raise KeyError("Error. Use method add()")

    def __getitem__(self, key: str) -> NoteRecord:
        return super().__getitem__(self.__normalize_key(key))

    def __contains__(self, key: object) -> bool:
        try:
            return self.__normalize_key(str(key)) in self.data
        except Exception:
            return False

    def find(self, criteria: str) -> list[NoteRecord]:
        """
        Find notes that have matching tags.
        Returns notes sorted by: 
            number of matching tags, 
            alphabetical order of matching tags, 
            title
        """
        result = []
        search_tags = set(criteria.casefold().split())

        for rec in self.values():
            rec_tags = set(tag.casefold() for tag in rec.tags)
            matched_tags = rec_tags & search_tags
            if matched_tags:
                result.append((rec, matched_tags))

        result.sort(key=lambda pair: (-len(pair[1]), sorted(pair[1]), pair[0].title.casefold()))
        return [rec for rec, _ in result]
