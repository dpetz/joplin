from dataclasses import dataclass

@dataclass
class NoteLink:
    id:str
    text:str

    def markdown(self) -> str:
        return f"[{self.text}](:/{self.id})"

@dataclass
class Edit:
    original:str
    revision:str = None

def lines_changed(edit):
    pass

def diff(edit):
    pass