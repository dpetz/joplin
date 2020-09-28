from dataclasses import dataclass
import commonmark

def html(md):
    parser = commonmark.Parser()
    return commonmark.HtmlRenderer().render(parser.parse(md))

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