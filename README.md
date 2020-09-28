# Zettel

Python scripts to turn [Joplin](https://joplinapp.org/) into a [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten)


## Installation

```sh
pip install -r requirements.txt
```

To run tests
```
pip install -r requirements-dev.txt
```

## Usage

```sh
python resize_resources.py 
python replace_links.py
python related.py 
```


## Backlog

- Report: Note w/ links to modified notes and diffs.
- refactor inline links to link references
- mark edits w/ emjois, eg. successful or failed rescaling
- trigger script from note ('Emoji Markup Language')

## Log

Create  [conda]([:/42dde63a39754b0283fe7fc48892de23](https://docs.conda.io/en/latest/)) python environment:

```sh
conda create --name joplin python
conda activate joplin
conda env list
```

Install dependencies incl. Joplin [API](https://joplinapp.org/api/)'s [Python client](https://pypi.org/project/joplin-api/) as descibed above.


Add [.gitignore](https://github.com/foxmask/joplin-api/blob/master/.gitignore) and [requirements.txt](https://github.com/foxmask/joplin-api/blob/master/requirements.txt)

[Add](https://code.visualstudio.com/docs/python/environments) new interpreter's path to [Visual Studio Code](:/65f1ab69c32b4e5087552d6a2f3a4c89): 

If *VS Code* [test discovery]((https://code.visualstudio.com/docs/python/testing#_enable-a-test-framework)) fails run ` pytest --collect-only ` to debug.


***
In `terminal.integrated.env.*` add
```sh
"PYTHONPATH" : "${workspaceFolder}:${env:PYTHONPATH}"
```
as explained [here](https://code.visualstudio.com/docs/python/environments)

***