# Joplin Zettel

My scripts to turn Joplin into a Zelda style Zettelkasten

## Install

Create  [conda]([:/42dde63a39754b0283fe7fc48892de23](https://docs.conda.io/en/latest/)) python environment:

```sh
conda create --name joplin python
conda activate joplin
```

Install dependencies incl. [Joplin API](https://joplinapp.org/api/)'s [Python client](https://pypi.org/project/joplin-api/):

```sh
pip install -r requirements.txt
conda env list
```


## run
```
python resize_resources.py 
python replace_links.py
python related.py 
```

# Backlog

- Report: Note w/ links to modified notes and diffs.
- refactor inline links to link references
- mark edits w/ emjois, eg. successful or failed rescaling
- trigger script from note ('Emoji Markup Language')