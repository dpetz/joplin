# Zettel

Python scripts to turn [Joplin](https://joplinapp.org/) into a [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten)


## Installation

Create Python environment

```sh
pip install conda
conda create -f environment.yml
conda activate zettel
```

## Usage

```sh
python resize_resources.py 
python replace_links.py
python related.py 
```

Or 
```sh
chmod +x zettel.py
./zettel.py
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

Make runnable via
```sh
chmod +x zettel.py
```

# Example

Note:
```json
{'id': '736ab59b113e4ea4b09b24293dc2cba9',
 'parent_id': '2a5c0c38dca14ae0bf66d4defcc06251',
 'title': 'Test 2',
 'body': '[Test 3](:9e830bc6530c416e950105834689cd63',
 'created_time': 1600180476986,
 'updated_time': 1601129403735,
 'is_conflict': 0,
 'latitude': '0.00000000',
 'longitude': '0.00000000',
 'altitude': '0.0000',
 'author': '',
 'source_url': '',
 'is_todo': 0,
 'todo_due': 0,
 'todo_completed': 0,
 'source': 'joplin-desktop',
 'source_application': 'net.cozic.joplin-desktop',
 'order': 0,
 'application_data': '',
 'user_created_time': 1600180476986,
 'user_updated_time': 1601129403735,
 'encryption_cipher_text': '',
 'encryption_applied': 0,
 'type_': 1}
``

# Interactive

```python
import os.chdir('/Users/dpetzoldt/git/home/zettel')
from zettel.util import api
res = await api().get_note('4083d03c95e042fb8da9176f9bb2a051')

