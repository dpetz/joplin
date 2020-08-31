from util import api
from asyncio import run
from dataclasses import dataclass

@dataclass
class NoteLink:
    id:str
    text:str

    def markdown(self) -> str:
        return f"[{self.text}](:/{self.id})"

INTRO = "\n\n---\nBacklinks\n"

async def backlinks(id):
    linking_notes = (await api().search(id)).json()
    links = [NoteLink(n['id'],n['title']) for n in linking_notes if n['id'] != id]
    
    note = (await api().get_note(id)).json()
    body = note['body']

    insertion = "\n".join([l.markdown() for l in links if l.id not in body])

    if len(insertion) > 2:
        if INTRO in body:
            body += '\n'
        else:
            body += INTRO
        
        body += insertion
        
        await api().update_note(note['id'],note['title'],body, note['parent_id'])

async def backlinks_all():
    notes = (await api().get_notes()).json()
    for  note in notes:
        await backlinks(note['id'])


if __name__ == '__main__':
    #run(backlinks('124cd8bca0e44859bbdeaf2f99147298'))
    run(backlinks_all())