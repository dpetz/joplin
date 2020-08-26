async def ping_me():
    await joplin.ping()
    print("ping successful")

async def new_note():
    # 1 - create a folder
    res = await joplin.create_folder(folder='MY FOLDER 2')
    data = res.json()
    parent_id = data['id']
    # 2 - create a note with tag
    body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
    assert type(body) is str
    kwargs = {'tags': 'tag1, tag2'}
    await joplin.create_note(title="MY NOTE", body=body,
                             parent_id=parent_id, **kwargs)
    print("Folder and Note created")