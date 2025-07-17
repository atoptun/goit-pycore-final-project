from collections import UserDict
import ulid 


class NoteRecord:
    def __init__(self) -> None:
        self.__id = ulid.new().str
        self.title = ""
        self.message = ""
        self.__tags = set()

    @property
    def id(self):
        return self.__id

    @property
    def tags(self):
        return self.__tags
    
    @tags.setter
    def tags(self, tags: set):
        self.__tags = tags

    def __str__(self) -> str:
        return f"id: {self.id}, title: {self.title}, message: {self.message}, tags: {self.tags}"
    

class Notes(UserDict[str, NoteRecord]):
    
    def add(self, note: NoteRecord):
        self.data[note.id] = note
    
    def delete(self, id: str):
        self.data.pop(str(id).upper())

    def __setitem__(self, key: str, item: NoteRecord) -> None:
        raise KeyError("Error. Use method add()")
    
    def __getitem__(self, key: str) -> NoteRecord:
        return super().__getitem__(str(key).upper())
    
