from os.path import join, splitext
from os import stat, listdir
from PIL import Image
from util import api
from asyncio import run
from io import BytesIO

res_dir = '/Users/dpetzoldt/.config/joplin-desktop/resources'
png_big = 'accd72f8f52f49988ad8341ad1db7238.png' # 8M
jpg_big = '55087622c67b77904a2a01316393cf72.jpg' # 1.9M
tmp_folder = './tmp'


async def report_mimes():
    res = (await api().get_resources()).json()
    mimes = {}
    for r in res:
        mime = r.get('mime','unknown')

        mimes[mime] = mimes.get(mime,0) + 1
    print(mimes)
    # {'image/png': 228, 'application/octet-stream': 1, 'image/jpeg': 133, 'image/gif': 9, 
    # application/pdf': 16, 'image/jpg': 2, 'image/svg+xml': 1, 'image/webp': 1}

async def resize_and_replace_big(kb=500):
    """List of all resources bigger than ``kb`` kilobytes"""
    res = (await api().get_resources()).json()
    ids = [r['id'] for r in res if r.get('size',0) > kb * 1024]
    for id in ids:
        await resize_and_replace(id)


async def resize_and_replace(id,factor=.5):
    # {'id': '7d01ddbe8a37351f6ba6d1ed3ce513ec', 'title': '', 'mime': 'image/png', 'filename': '',
    # 'created_time': 1598440403780, 'updated_time': 1598641722907, 'user_created_time': 1598440403781,
    # 'user_updated_time': 1598641722907, 'file_extension': '', 'encryption_cipher_text': '', 'encryption_applied': 0,
    # 'encryption_blob_encrypted': 0, 'size': 105794, 'is_shared': 0, 'type_': 4}

    try:
        res_old = (await api().get_resource(id)).json()
        mime_type, mime_sub = res_old['mime'].split('/')

        # Only rescale for certain mime types
        if mime_sub in 'gif jpeg jpg png'.split():

            #download resource as binary content
            binary = (await api().download_resources(id))

            # save to tmp folder with mime subtype as suffix
            fname = f"{id}.{mime_sub}"
            tmp_file = join(tmp_folder,fname)
            with open(tmp_file, 'wb') as f:
                f.write(bytes(binary._content))

            # rescale image
            img = Image.open(tmp_file)
            img = img.resize((round(img.size[0]*factor), round(img.size[1]*factor)))
            img.save(tmp_file)
        
            # delete orginal resource and upload new one
            await api().delete_resources(id)
            await api().create_resource(tmp_file,title=fname)

            # find notes with links to image and replace with new links
            id_new = (await api().search(fname, item_type='resource')).json()[0]['id']
            n = await replace_in_notes(id,id_new)

            print(f"Rescaled: {id_new}. Updated notes: {n}")

    except Exception:
        print(f"Resizing failed: {id}")


async def replace_in_notes(source, target):
    """ Find notes containing `source` and replace all occurrences w/ `target` """
    notes = (await api().search(source, item_type='note')).json()
    for note in notes:
        body = (await api().get_note(note['id'])).json()['body']
        body =  body.replace(source,target)  
        await api().update_note(note['id'],note['title'],body, note['parent_id'])
    return len(notes)


if __name__ == "__main__":
    #run(resize_and_replace('afd0fa1c7785ca6c474307de4eb9279b'))
    run(resize_and_replace_big())